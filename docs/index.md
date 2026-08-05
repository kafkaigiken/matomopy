# Matomo HTTP API — documentation

Matomo exposes two public HTTP APIs. This documentation explains both and how
to use them from the accompanying Python library, `matomo-pylib`.

| API | Purpose | Library entry point |
|-----|---------|---------------------|
| **Reporting API** | Read analytics data (visits, pages, referrers, goals, ...). | `MatomoClient` |
| **Tracking API** | Send data in (page views, events, goals, ecommerce). | `MatomoTracker` |

## Start here

- **[Reporting API guide](reporting-api.md)** — the endpoint, authentication, the parameters shared by every report (`idSite`, `period`, `date`, `segment`, `filter_*`), output formats, pagination, batching and errors.
- **[Tracking API guide](tracking-api.md)** — recording page views, events, goals and ecommerce from server-side code.
- **[Full method reference](api-reference.md)** — all 366 methods across 47 modules, with parameters, required access and return values.

## Install the library

```bash
pip install matomo-pylib
```

Requires Python 3.8+. The only dependency is `requests`.

## 60-second example

```python
from matomo_pylib import MatomoClient

matomo = MatomoClient(
    "https://analytics.example.org",
    token_auth="YOUR_TOKEN",
    default_id_site=1,
)

# Visit metrics for today:
summary = matomo.VisitsSummary.get(period="day", date="today")
print(summary["nb_visits"], "visits,", summary["nb_uniq_visitors"], "unique")

# Top 10 pages this month:
for row in matomo.Actions.getPageUrls(period="month", date="today",
                                      filter_limit=10):
    print(row["nb_hits"], row["label"])
```

Any Matomo method is reachable as `matomo.<Module>.<action>(...)` — browse the
[method reference](api-reference.md) to see what's available.

## How this documentation was produced

The [method reference](api-reference.md) is generated directly from the Matomo plugin source (`plugins/*/API.php`), so the method names, parameters and access requirements reflect this exact Matomo version. When in doubt, the live instance is authoritative: call `matomo.get_report_metadata(id_site=1)` to see what a specific server offers, including third-party plugins.

## Authentication in one line

Create a `token_auth` in Matomo under **Administration → Personal → Security →
Auth tokens**, and give it to the client. Use a **view-only** user for reporting. The token is never placed in the URL — it goes in the POST body (or an `Authorization: Bearer` header). See the
[Reporting API guide](reporting-api.md#authentication) for details.
