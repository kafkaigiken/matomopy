"""Client for the Matomo Tracking (HTTP) API.

The Tracking API is the endpoint that Matomo's JavaScript tracker and mobile
SDKs talk to (``matomo.php``). It records visits, page views, events, goals,
ecommerce orders and more by issuing simple HTTP requests. This module lets a
Python program send the same requests -- useful for tracking server-side
events, importing data, or instrumenting backend jobs.

Some parameters (overriding the visitor IP, the timestamp, or the geolocation)
are only honoured when a ``token_auth`` with write access is supplied.
"""

from __future__ import annotations

import json
import random
import secrets
import string
from typing import Any, Dict, List, Optional, Sequence, Union

import requests

from ._http import (
    SessionContextMixin,
    normalize_endpoint,
    raise_for_status,
    send,
)
from .exceptions import MatomoConfigError
from .params import encode_params, encode_query

EcommerceItem = Union[Sequence[Any], Dict[str, Any]]


def generate_visitor_id() -> str:
    """Return a random 16-character hex visitor id, as Matomo expects."""
    return secrets.token_hex(8)


class MatomoTracker(SessionContextMixin):
    """Sends tracking requests to a Matomo instance's ``matomo.php``.

    A tracker carries per-visitor state (visitor id, user id, current URL,
    resolution, custom dimensions, ...) that is reused across calls, mirroring
    how the JavaScript tracker behaves within a page.

    Args:
        base_url: The Matomo installation URL, or a full path ending in
            ``matomo.php`` / ``piwik.php``.
        id_site: The site ID that visits are recorded against.
        token_auth: Optional auth token. Required only for privileged
            parameters such as overriding the visitor IP, geolocation, or the
            event timestamp when it is older than a few hours.
        timeout: Per-request timeout in seconds.
        verify_ssl: Whether TLS certificates are verified.
        user_agent: The ``User-Agent`` reported for the visitor. Defaults to
            a library identifier; set it to the real client's agent when
            proxying tracking on someone's behalf.
        accept_language: The ``Accept-Language`` reported for the visitor
            (drives language reports).
        session: An optional pre-configured :class:`requests.Session`.
    """

    def __init__(
        self,
        base_url: str,
        id_site: Union[int, str],
        token_auth: Optional[str] = None,
        *,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        user_agent: Optional[str] = None,
        accept_language: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.endpoint = normalize_endpoint(base_url, "matomo.php")
        self.id_site = id_site
        self.token_auth = token_auth
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent or "matomo-pylib"
        self.accept_language = accept_language
        self.session = session or requests.Session()

        # Per-visitor state reused across tracking calls.
        self.visitor_id: Optional[str] = None
        self.user_id: Optional[str] = None
        self.ip: Optional[str] = None
        self.url: Optional[str] = None
        self.url_referrer: Optional[str] = None
        self.resolution: Optional[str] = None
        self.custom_timestamp: Optional[int] = None
        self.new_visit: bool = False
        self.custom_dimensions: Dict[int, Any] = {}

        self._bulk_mode: bool = False
        self._queue: List[str] = []

    def __repr__(self) -> str:
        return f"<MatomoTracker {self.endpoint} idSite={self.id_site}>"

    # -- per-visitor state ----------------------------------------------

    def set_visitor_id(self, visitor_id: str) -> "MatomoTracker":
        """Pin the visitor id (must be exactly 16 hexadecimal characters)."""
        if len(visitor_id) != 16 or any(character not in string.hexdigits for character in visitor_id):
            raise MatomoConfigError(
                "visitor_id must be a 16-character hex string; use generate_visitor_id() to create one."
            )
        self.visitor_id = visitor_id
        return self

    def set_user_id(self, user_id: str) -> "MatomoTracker":
        """Associate all following requests with a known user id."""
        self.user_id = user_id
        return self

    def set_ip(self, ip: str) -> "MatomoTracker":
        """Override the visitor IP (requires ``token_auth``)."""
        self.ip = ip
        return self

    def set_url(self, url: str) -> "MatomoTracker":
        """Set the current page URL used by later tracking calls."""
        self.url = url
        return self

    def set_url_referrer(self, url: str) -> "MatomoTracker":
        """Set the referrer URL used by later tracking calls.

        Like the other visit-context setters, this persists until it is
        changed; only :meth:`set_force_new_visit` is one-shot.
        """
        self.url_referrer = url
        return self

    def set_resolution(self, width: int, height: int) -> "MatomoTracker":
        """Set the visitor's screen resolution, e.g. ``1920x1080``."""
        self.resolution = f"{width}x{height}"
        return self

    def set_custom_dimension(self, dimension_id: int, value: Any) -> "MatomoTracker":
        """Set a custom dimension value (sent as ``dimension<ID>``)."""
        self.custom_dimensions[int(dimension_id)] = value
        return self

    def set_custom_timestamp(self, epoch_seconds: int) -> "MatomoTracker":
        """Record the action at a past time (requires ``token_auth``)."""
        self.custom_timestamp = int(epoch_seconds)
        return self

    def set_force_new_visit(self, force: bool = True) -> "MatomoTracker":
        """Force the next request to start a brand new visit.

        The flag is one-shot: it is cleared once a tracking request has
        carried it, so only the very next request starts a new visit.
        """
        self.new_visit = force
        return self

    # -- tracking actions -----------------------------------------------

    def track_page_view(
        self,
        action_name: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Any:
        """Track a page view.

        Args:
            action_name: The page title / action name shown in reports.
            url: The page URL. Defaults to the tracker's current URL.
        """
        params: Dict[str, Any] = {}
        if action_name is not None:
            params["action_name"] = action_name
        return self._track(url=url, extra=params)

    def track_event(
        self,
        category: str,
        action: str,
        name: Optional[str] = None,
        value: Optional[float] = None,
        url: Optional[str] = None,
    ) -> Any:
        """Track a custom event (category / action / name / value)."""
        params: Dict[str, Any] = {"e_c": category, "e_a": action}
        if name is not None:
            params["e_n"] = name
        if value is not None:
            params["e_v"] = value
        return self._track(url=url, extra=params)

    def track_goal(
        self,
        id_goal: Union[int, str],
        revenue: Optional[float] = None,
        url: Optional[str] = None,
    ) -> Any:
        """Track a manual goal conversion, optionally with revenue."""
        params: Dict[str, Any] = {"idgoal": id_goal}
        if revenue is not None:
            params["revenue"] = revenue
        return self._track(url=url, extra=params)

    def track_site_search(
        self,
        keyword: str,
        category: Optional[str] = None,
        count_results: Optional[int] = None,
        url: Optional[str] = None,
    ) -> Any:
        """Track an internal site search."""
        params: Dict[str, Any] = {"search": keyword}
        if category is not None:
            params["search_cat"] = category
        if count_results is not None:
            params["search_count"] = count_results
        return self._track(url=url, extra=params)

    def track_action(self, action_url: str, action_type: str = "link") -> Any:
        """Track a download or an outlink click.

        The ``url`` of the request stays the page the action happened on (the
        tracker's current URL), matching Matomo's official trackers; the
        downloaded/clicked URL is reported in ``download``/``link``. When no
        page URL has been set, the action URL is used for both.

        Args:
            action_url: The URL that was downloaded or clicked.
            action_type: ``"download"`` or ``"link"`` (outlink).
        """
        if action_type not in ("download", "link"):
            raise MatomoConfigError("action_type must be 'download' or 'link'.")
        page_url = self.url if self.url is not None else action_url
        return self._track(url=page_url, extra={action_type: action_url})

    def track_content_impression(
        self,
        name: str,
        piece: str = "Unknown",
        target: Optional[str] = None,
    ) -> Any:
        """Track a content impression (a content block being shown)."""
        return self._track_content(name, piece, target)

    def track_content_interaction(
        self,
        interaction: str,
        name: str,
        piece: str = "Unknown",
        target: Optional[str] = None,
    ) -> Any:
        """Track an interaction (e.g. a click) with a content block."""
        return self._track_content(name, piece, target, interaction)

    def _track_content(
        self,
        name: str,
        piece: str,
        target: Optional[str],
        interaction: Optional[str] = None,
    ) -> Any:
        """Build and dispatch a content impression or interaction request."""
        params: Dict[str, Any] = {"c_n": name, "c_p": piece}
        if interaction is not None:
            params["c_i"] = interaction
        if target is not None:
            params["c_t"] = target
        return self._track(extra=params)

    def track_ecommerce_order(
        self,
        order_id: str,
        grand_total: float,
        sub_total: Optional[float] = None,
        tax: Optional[float] = None,
        shipping: Optional[float] = None,
        discount: Optional[float] = None,
        items: Optional[Sequence[EcommerceItem]] = None,
    ) -> Any:
        """Track a completed ecommerce order.

        Args:
            order_id: Your unique order identifier.
            grand_total: The order total (revenue).
            sub_total, tax, shipping, discount: Optional order breakdown.
            items: The purchased items. Each item is ``[sku, name, category,
                price, quantity]`` (trailing fields may be omitted) or a dict
                with those keys.
        """
        params: Dict[str, Any] = {
            "idgoal": 0,
            "ec_id": order_id,
            "revenue": grand_total,
        }
        if sub_total is not None:
            params["ec_st"] = sub_total
        if tax is not None:
            params["ec_tx"] = tax
        if shipping is not None:
            params["ec_sh"] = shipping
        if discount is not None:
            params["ec_dt"] = discount
        if items is not None:
            params["ec_items"] = self._encode_items(items)
        return self._track(extra=params)

    def track_ecommerce_cart_update(
        self,
        grand_total: float,
        items: Optional[Sequence[EcommerceItem]] = None,
    ) -> Any:
        """Track the current state of a shopping cart."""
        params: Dict[str, Any] = {"idgoal": 0, "revenue": grand_total}
        if items is not None:
            params["ec_items"] = self._encode_items(items)
        return self._track(extra=params)

    def track_ping(self, url: Optional[str] = None) -> Any:
        """Send a heartbeat to extend the visit's recorded duration."""
        return self._track(url=url, extra={"ping": 1})

    # -- bulk tracking --------------------------------------------------

    def enable_bulk_tracking(self) -> "MatomoTracker":
        """Queue requests instead of sending them until :meth:`flush`."""
        self._bulk_mode = True
        return self

    def flush(self) -> Optional[Any]:
        """Send all queued requests in a single bulk HTTP POST.

        Returns ``None`` if nothing is queued, otherwise the decoded server
        response. The queue is cleared only once the batch has been accepted,
        so a failed flush (transport error or HTTP error) leaves the events
        queued and the caller can retry.
        """
        if not self._queue:
            return None

        payload: Dict[str, Any] = {"requests": list(self._queue)}
        if self.token_auth:
            payload["token_auth"] = self.token_auth

        response = send(
            lambda: self.session.post(
                self.endpoint,
                json=payload,
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
                verify=self.verify_ssl,
            ),
            context="Bulk tracking request",
        )
        raise_for_status(response)
        self._queue.clear()
        return self._maybe_json(response)

    # -- internals ------------------------------------------------------

    @staticmethod
    def _encode_items(items: Sequence[EcommerceItem]) -> str:
        """JSON-encode ecommerce items into Matomo's ``ec_items`` format."""
        encoded: List[List[Any]] = []
        for item in items:
            if isinstance(item, dict):
                encoded.append(
                    [
                        item.get("sku", ""),
                        item.get("name", ""),
                        item.get("category", ""),
                        item.get("price", 0),
                        item.get("quantity", 1),
                    ]
                )
            else:
                encoded.append(list(item))
        return json.dumps(encoded)

    def _base_params(self) -> Dict[str, Any]:
        """Build the parameters common to every tracking request."""
        params: Dict[str, Any] = {
            "idsite": self.id_site,
            "rec": 1,
            "apiv": 1,
            "rand": random.getrandbits(31),
            "send_image": 0,
        }
        if self.visitor_id:
            params["_id"] = self.visitor_id
            params["cid"] = self.visitor_id
        if self.user_id is not None:
            params["uid"] = self.user_id
        if self.url_referrer is not None:
            params["urlref"] = self.url_referrer
        if self.resolution is not None:
            params["res"] = self.resolution
        if self.accept_language is not None:
            params["lang"] = self.accept_language
        if self.new_visit:
            params["new_visit"] = 1
        for dimension_id, value in self.custom_dimensions.items():
            params[f"dimension{dimension_id}"] = value
        if self.token_auth:
            params["token_auth"] = self.token_auth
        if self.ip is not None:
            params["cip"] = self.ip
        if self.custom_timestamp is not None:
            params["cdt"] = self.custom_timestamp
        return params

    def _track(
        self,
        url: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Assemble and dispatch (or queue) one tracking request."""
        params = self._base_params()
        effective_url = url if url is not None else self.url
        if effective_url is not None:
            params["url"] = effective_url
        if extra:
            params.update(extra)

        # "Force a new visit" applies to a single request only; clear it so
        # that following requests do not each start another visit.
        self.new_visit = False

        if self._bulk_mode:
            self._queue.append("?" + encode_query(params))
            return None
        return self._send(params)

    def _send(self, params: Dict[str, Any]) -> Any:
        """Issue a single tracking GET request."""
        response = send(
            lambda: self.session.get(
                self.endpoint,
                params=encode_params(params),
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
                verify=self.verify_ssl,
            ),
            context="Tracking request",
        )
        raise_for_status(response)
        return response

    @staticmethod
    def _maybe_json(response: requests.Response) -> Any:
        """Return parsed JSON when possible, otherwise the raw text."""
        try:
            return response.json()
        except ValueError:
            return response.text
