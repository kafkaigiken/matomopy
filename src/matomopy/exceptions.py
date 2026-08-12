"""Exception hierarchy for the Matomo client.

All exceptions raised by this library inherit from :class:`MatomoError`, so a
single ``except MatomoError`` clause can catch every failure mode.
"""

from __future__ import annotations

from typing import Optional


class MatomoError(Exception):
    """Base class for every error raised by this library."""


class MatomoConfigError(MatomoError):
    """Raised when the client is configured incorrectly (e.g. a bad URL)."""


class MatomoHTTPError(MatomoError):
    """Raised when the Matomo server returns a non-success HTTP status code.

    Attributes:
        status_code: The HTTP status code returned by the server.
        response_text: The raw body of the response, useful for debugging.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class MatomoAPIError(MatomoError):
    """Raised when Matomo returns a logical error inside a ``200 OK`` response.

    The Matomo Reporting API frequently signals failures with an HTTP 200
    status and a JSON body such as ``{"result": "error", "message": "..."}``.
    This exception surfaces that ``message``.

    Attributes:
        message: The human readable error message returned by Matomo.
        method: The API method that produced the error, if known.
    """

    def __init__(self, message: str, method: Optional[str] = None) -> None:
        self.message = message
        self.method = method
        full = f"[{method}] {message}" if method else message
        super().__init__(full)


class MatomoAuthenticationError(MatomoAPIError):
    """Raised when Matomo rejects the request because authentication failed.

    This is a specialised :class:`MatomoAPIError` detected from the error
    message (e.g. an invalid or missing ``token_auth``).
    """
