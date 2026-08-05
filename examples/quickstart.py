"""Runnable example: read data and (optionally) send a tracking event.

Set MATOMO_URL, MATOMO_TOKEN and MATOMO_SITE_ID in your environment, then::

    python examples/quickstart.py

Without any configuration it falls back to Matomo's public read-only demo
instance, so it works out of the box.
"""

import os

from matomo_pylib import MatomoClient, MatomoError

BASE_URL = os.environ.get("MATOMO_URL", "https://demo.matomo.cloud/")
TOKEN = os.environ.get("MATOMO_TOKEN")  # None => anonymous access
SITE_ID = int(os.environ.get("MATOMO_SITE_ID", "1"))


def main() -> None:
    matomo = MatomoClient(BASE_URL, token_auth=TOKEN, default_id_site=SITE_ID)

    print("Matomo version:", matomo.get_matomo_version())

    summary = matomo.VisitsSummary.get(period="day", date="today")
    print("\nToday so far:")
    print("  visits        :", summary.get("nb_visits"))
    print("  unique visitors:", summary.get("nb_uniq_visitors"))
    print("  actions       :", summary.get("nb_actions"))

    print("\nTop 5 pages this month:")
    pages = matomo.Actions.getPageUrls(period="month", date="today", filter_limit=5)
    for row in pages:
        print(f"  {row.get('nb_hits', 0):>6}  {row.get('label')}")

    print("\nReferrer types:")
    referrers = matomo.Referrers.getReferrerType(period="month", date="today")
    for row in referrers:
        print(f"  {row.get('nb_visits', 0):>6}  {row.get('label')}")


if __name__ == "__main__":
    try:
        main()
    except MatomoError as exc:
        raise SystemExit(f"Matomo request failed: {exc}")
