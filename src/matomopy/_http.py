"""Internal HTTP plumbing shared by the reporting and tracking clients.

Both :class:`~matomopy.client.MatomoClient` and
:class:`~matomopy.tracking.MatomoTracker` talk to Matomo over HTTP and
need the same low-level pieces: normalising the base URL into an endpoint,
mapping transport failures onto :class:`MatomoHTTPError`, raising on 4xx/5xx
responses, and session/context-manager lifecycle. Keeping that plumbing here
means there is a single place to change how HTTP failures surface.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar

import requests

from .exceptions import MatomoConfigError, MatomoHTTPError

_Self = TypeVar("_Self", bound="SessionContextMixin")


def normalize_endpoint(base_url: str, default_filename: str) -> str:
    """Return the HTTP endpoint for ``base_url``.

    Accepts a root URL, a root with a trailing slash, or a full path already
    ending in ``.php`` (in which case it is used as-is). Otherwise
    ``default_filename`` (e.g. ``index.php`` or ``matomo.php``) is appended.

    Raises:
        MatomoConfigError: if ``base_url`` is empty or blank.
    """
    if not base_url or not str(base_url).strip():
        raise MatomoConfigError("base_url must be a non-empty string.")
    url = str(base_url).strip().rstrip("/")
    if url.lower().endswith(".php"):
        return url
    return f"{url}/{default_filename}"


def send(request_call: Callable[[], requests.Response], context: str) -> requests.Response:
    """Run ``request_call`` and map transport failures to ``MatomoHTTPError``.

    Args:
        request_call: A zero-argument callable that performs the HTTP request
            and returns the response (e.g. a ``lambda`` wrapping
            ``session.post(...)``).
        context: Names the operation for the error message, e.g.
            ``"Request to Matomo"``.
    """
    try:
        return request_call()
    except requests.RequestException as exc:
        raise MatomoHTTPError(f"{context} failed: {exc}") from exc


def raise_for_status(response: requests.Response) -> None:
    """Raise ``MatomoHTTPError`` if ``response`` has a 4xx/5xx status code."""
    if response.status_code >= 400:
        raise MatomoHTTPError(
            f"Matomo returned HTTP {response.status_code}.",
            status_code=response.status_code,
            response_text=response.text[:2000],
        )


class SessionContextMixin:
    """Adds ``close()`` and context-manager support over ``self.session``."""

    session: requests.Session

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self: _Self) -> _Self:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()
