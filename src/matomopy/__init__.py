"""A Python client for the Matomo Reporting and Tracking HTTP APIs.

Typical usage::

    from matomopy import MatomoClient

    matomo = MatomoClient(
        "https://analytics.example.org",
        token_auth="YOUR_TOKEN",
        default_id_site=1,
    )

    # Ergonomic, dynamic access to any module/method:
    summary = matomo.VisitsSummary.get(period="day", date="today")

    # ...or the explicit generic call:
    pages = matomo.call(
        "Actions.getPageUrls", period="month", date="2024-01-01"
    )

See the ``docs/`` directory for the full reporting and tracking guides.
"""

from ._version import __version__
from .client import MatomoClient
from .exceptions import (
    MatomoAPIError,
    MatomoAuthenticationError,
    MatomoConfigError,
    MatomoError,
    MatomoHTTPError,
)
from .tracking import MatomoTracker, generate_visitor_id

__all__ = [
    "MatomoClient",
    "MatomoTracker",
    "generate_visitor_id",
    "MatomoError",
    "MatomoConfigError",
    "MatomoHTTPError",
    "MatomoAPIError",
    "MatomoAuthenticationError",
    "__version__",
]
