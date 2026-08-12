"""Client for the Matomo Reporting (HTTP) API.

The Reporting API is a single HTTP endpoint (``index.php``) that dispatches
to hundreds of methods named ``Module.action`` (for example
``VisitsSummary.get`` or ``Actions.getPageUrls``). Every method shares a
common set of parameters (``idSite``, ``period``, ``date``, ``segment``,
``format`` and the ``filter_*`` family).

:class:`MatomoClient` exposes three ways to call the API:

* :meth:`MatomoClient.call` -- the generic escape hatch that can invoke any
  method by name.
* Attribute access -- ``client.VisitsSummary.get(...)`` is sugar for
  ``client.call("VisitsSummary.get", ...)`` and works for *every* module and
  method, including ones added in future Matomo versions.
* A few high-level helpers (:meth:`bulk_request`, :meth:`paginate`,
  :meth:`get_report_metadata`, ...) that do more than a plain passthrough.
"""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Sequence, Union

import requests
from requests.adapters import HTTPAdapter

try:  # urllib3 is a transitive dependency of requests.
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover - extremely unlikely.
    Retry = None  # type: ignore[assignment]

from ._http import (
    SessionContextMixin,
    normalize_endpoint,
    raise_for_status,
    send,
)
from .exceptions import (
    MatomoAPIError,
    MatomoAuthenticationError,
    MatomoConfigError,
)
from .params import encode_params, encode_query

# The parameters that :meth:`MatomoClient.call` accepts as first-class
# keyword arguments. Everything else is forwarded verbatim using Matomo's
# exact parameter names.
JSON = Union[Dict[str, Any], List[Any]]

_AUTH_HINTS = ("token_auth", "authenticate", "not authorized", "no access")


class MatomoClient(SessionContextMixin):
    """A configured connection to one Matomo instance's Reporting API.

    Args:
        base_url: The URL of the Matomo installation. Accepts any of
            ``https://analytics.example.org``,
            ``https://analytics.example.org/`` or a full path ending in
            ``index.php``. The reporting endpoint is derived from it.
        token_auth: The ``token_auth`` secret used to authenticate. Create
            one in Matomo under *Administration > Personal > Security > Auth
            tokens*. If omitted, requests are made anonymously and only
            public data is returned.
        default_id_site: An ``idSite`` used whenever a call does not specify
            one. Convenient when a client only ever talks to a single site.
        default_format: The output format for calls that do not override it.
            Defaults to ``"json"`` (parsed into Python objects).
        timeout: Per-request timeout in seconds.
        verify_ssl: Whether TLS certificates are verified. Leave ``True`` in
            production.
        auth_method: ``"post"`` (default) sends ``token_auth`` in the POST
            body; ``"bearer"`` sends it as an ``Authorization: Bearer``
            header instead. Both keep the token out of the URL.
        max_retries: Number of automatic retries for transient network and
            5xx errors. Ignored when ``session`` is supplied, so that a
            shared session's own adapters are left untouched.
        session: An optional pre-configured :class:`requests.Session`.
    """

    def __init__(
        self,
        base_url: str,
        token_auth: Optional[str] = None,
        *,
        default_id_site: Optional[Union[int, str]] = None,
        default_format: str = "json",
        timeout: float = 30.0,
        verify_ssl: bool = True,
        auth_method: str = "post",
        max_retries: int = 2,
        session: Optional[requests.Session] = None,
    ) -> None:
        if auth_method not in ("post", "bearer"):
            raise MatomoConfigError("auth_method must be 'post' or 'bearer'.")

        self.endpoint = normalize_endpoint(base_url, "index.php")
        self.token_auth = token_auth
        self.default_id_site = default_id_site
        self.default_format = default_format
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.auth_method = auth_method

        # Only a session we created may have its transport adapters replaced;
        # a caller-supplied session may be shared with unrelated HTTP calls.
        self._owns_session = session is None
        self.session = session or requests.Session()
        if max_retries and Retry is not None and self._owns_session:
            retry = Retry(
                total=max_retries,
                backoff_factor=0.5,
                status_forcelist=(500, 502, 503, 504),
                allowed_methods=frozenset(["GET", "POST"]),
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)

    def __repr__(self) -> str:
        authed = "authenticated" if self.token_auth else "anonymous"
        return f"<MatomoClient {self.endpoint} ({authed})>"

    # -- the generic call -----------------------------------------------

    def call(
        self,
        method: str,
        *,
        id_site: Optional[Union[int, str]] = None,
        period: Optional[str] = None,
        date: Optional[str] = None,
        segment: Optional[str] = None,
        format: Optional[str] = None,
        filter_limit: Optional[int] = None,
        filter_offset: Optional[int] = None,
        flat: Optional[bool] = None,
        expanded: Optional[bool] = None,
        raw: bool = False,
        **params: Any,
    ) -> Any:
        """Call any Reporting API method and return its result.

        Args:
            method: The API method, e.g. ``"VisitsSummary.get"``.
            id_site: The site ID (``idSite``). Falls back to
                ``default_id_site``. Some methods accept several sites via
                the ``id_sites`` keyword (a list is comma-joined).
            period: One of ``day``, ``week``, ``month``, ``year`` or
                ``range``.
            date: A date (``today``, ``yesterday``, ``2024-01-31``),
                a keyword (``last7``, ``previous30``) or a range
                (``2024-01-01,2024-01-31``) when ``period="range"``.
            segment: An optional segment definition string.
            format: Output format. ``"json"`` (default) is parsed to Python
                objects; ``"csv"``, ``"tsv"``, ``"xml"`` and ``"rss"`` are
                returned as text.
            filter_limit: Maximum number of rows. Use ``-1`` for no limit.
            filter_offset: Row offset, for manual pagination.
            flat: If true, flatten hierarchical reports into a single level.
            expanded: If true, include subtables inline in the response.
            raw: If true, return the raw response bytes (use for the
                ``ImageGraph.get`` PNG endpoint or PDF exports).
            **params: Any other Matomo parameter, using its exact name
                (e.g. ``idGoal``, ``filter_sort_column``, ``columns``,
                ``hideColumns``, ``idDimension``). Lists become
                comma-separated values; dicts become bracketed arrays;
                booleans become ``1``/``0``; ``None`` values are dropped.

        Returns:
            Parsed JSON (``dict``/``list``) for ``format="json"``, the
            decoded text for other formats, or ``bytes`` when ``raw=True``.

        Raises:
            MatomoAPIError: Matomo returned a logical error.
            MatomoAuthenticationError: Authentication was rejected.
            MatomoHTTPError: The server returned a non-2xx status.
        """
        resolved_format = format or self.default_format
        resolved_site = id_site if id_site is not None else self.default_id_site

        data: Dict[str, Any] = {
            "method": method,
            "format": resolved_format,
            "idSite": resolved_site,
            "period": period,
            "date": date,
            "segment": segment,
            "filter_limit": filter_limit,
            "filter_offset": filter_offset,
            "flat": flat,
            "expanded": expanded,
        }
        data.update(params)

        if self.auth_method == "post" and self.token_auth and "token_auth" not in params:
            data["token_auth"] = self.token_auth

        headers = {}
        if self.auth_method == "bearer" and self.token_auth:
            headers["Authorization"] = f"Bearer {self.token_auth}"

        response = self._request(data, headers)
        return self._parse(response, method, resolved_format, raw)

    def _request(self, data: Dict[str, Any], headers: Dict[str, str]) -> requests.Response:
        """Perform the HTTP POST and surface transport-level failures."""
        response = send(
            lambda: self.session.post(
                self.endpoint,
                params={"module": "API"},
                data=encode_params(data),
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            ),
            context="Request to Matomo",
        )
        raise_for_status(response)
        return response

    def _parse(
        self,
        response: requests.Response,
        method: str,
        fmt: str,
        raw: bool,
    ) -> Any:
        """Decode a response body and raise on Matomo-level errors."""
        if raw:
            return response.content

        if fmt.lower() != "json":
            return response.text

        try:
            data = response.json()
        except ValueError as exc:
            raise MatomoAPIError(
                f"Response was not valid JSON: {response.text[:500]}",
                method=method,
            ) from exc

        if isinstance(data, dict) and data.get("result") == "error":
            message = data.get("message", "Unknown Matomo error.")
            lowered = message.lower()
            if any(hint in lowered for hint in _AUTH_HINTS):
                raise MatomoAuthenticationError(message, method=method)
            raise MatomoAPIError(message, method=method)
        return data

    # -- ergonomic attribute access -------------------------------------

    def __getattr__(self, name: str) -> "_ModuleProxy":
        """Return a proxy so ``client.Module.method(...)`` works.

        Only reached for attributes that are not real members of the
        instance. A leading uppercase letter marks a Matomo module name
        (all Matomo modules are capitalised), which avoids hijacking
        private/dunder lookups.
        """
        if name.startswith("_") or not name[:1].isupper():
            raise AttributeError(name)
        return _ModuleProxy(self, name)

    # -- high-level helpers ---------------------------------------------

    def get_matomo_version(self) -> str:
        """Return the Matomo version string of the target instance."""
        result = self.call("API.getMatomoVersion")
        if isinstance(result, dict):
            return str(result.get("value", result))
        return str(result)

    def get_report_metadata(
        self,
        id_site: Optional[Union[int, str]] = None,
        **params: Any,
    ) -> JSON:
        """Return metadata describing every available report for a site.

        This is Matomo's self-documenting ``API.getReportMetadata`` call and
        is the best way to discover, at runtime, which reports exist on a
        given instance (including those added by third-party plugins).
        """
        return self.call("API.getReportMetadata", id_site=id_site, **params)

    def get_segments_metadata(
        self,
        id_sites: Optional[Sequence[Union[int, str]]] = None,
        **params: Any,
    ) -> JSON:
        """Return the list of segments that can be used against the API."""
        return self.call("API.getSegmentsMetadata", idSites=id_sites, **params)

    def paginate(
        self,
        method: str,
        *,
        page_size: int = 500,
        start_offset: int = 0,
        max_rows: Optional[int] = None,
        **params: Any,
    ) -> Iterator[Any]:
        """Yield rows from a report, fetching one page at a time.

        Repeatedly calls ``method`` with an increasing ``filter_offset``
        until Matomo returns fewer rows than ``page_size`` (the last page)
        or ``max_rows`` have been yielded. Only meaningful for methods that
        return a flat list of rows.

        Args:
            method: The API method to page through.
            page_size: Rows requested per page (``filter_limit``).
            start_offset: Initial ``filter_offset``.
            max_rows: Optional hard cap on the number of rows yielded.
            **params: Any other parameters forwarded to :meth:`call`.

        Yields:
            Individual report rows (usually ``dict`` objects).
        """
        if "filter_limit" in params or "filter_offset" in params:
            raise MatomoConfigError(
                "paginate() controls filter_limit/filter_offset itself; use page_size and start_offset instead."
            )

        offset = start_offset
        yielded = 0
        while True:
            page = self.call(
                method,
                filter_limit=page_size,
                filter_offset=offset,
                **params,
            )
            if not isinstance(page, list):
                raise MatomoAPIError(
                    f"{method} did not return a list of rows; paginate() only works on flat reports.",
                    method=method,
                )
            if not page:
                return
            for row in page:
                yield row
                yielded += 1
                if max_rows is not None and yielded >= max_rows:
                    return
            if len(page) < page_size:
                return
            offset += page_size

    def bulk_request(self, requests_list: Sequence[Union[str, Dict[str, Any]]]) -> List[Any]:
        """Run several API calls in a single HTTP request.

        Wraps ``API.getBulkRequest``. Each entry may be a pre-built query
        string (``"method=VisitsSummary.get&idSite=1&period=day&..."``) or a
        mapping of parameters (which is URL-encoded for you). A single
        ``token_auth`` (the client's) authenticates the whole batch.

        Args:
            requests_list: The individual requests to batch.

        Returns:
            A list with one decoded result per input request, in order.
        """
        urls: List[str] = []
        for entry in requests_list:
            if isinstance(entry, str):
                urls.append(entry)
            else:
                urls.append(encode_query(entry))

        indexed = {f"urls[{i}]": url for i, url in enumerate(urls)}
        return self.call("API.getBulkRequest", **indexed)


class _ModuleProxy:
    """Bound to a module name; turns attribute access into API calls."""

    __slots__ = ("_client", "_module")

    def __init__(self, client: MatomoClient, module: str) -> None:
        self._client = client
        self._module = module

    def __getattr__(self, action: str) -> Any:
        if action.startswith("_"):
            raise AttributeError(action)
        method = f"{self._module}.{action}"

        def _call(**params: Any) -> Any:
            return self._client.call(method, **params)

        _call.__name__ = action
        _call.__qualname__ = method
        _call.__doc__ = f"Call the Matomo API method ``{method}``. Accepts the same kwargs as MatomoClient.call()."
        return _call

    def __repr__(self) -> str:
        return f"<Matomo module '{self._module}'>"
