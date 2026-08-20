# matomopy

A small, dependency-light Python client for the two public HTTP APIs of
[Matomo](https://matomo.org):

- the **Reporting API** — read your analytics data (`MatomoClient`)
- the **Tracking API** — send visits, events, goals and ecommerce data
  (`MatomoTracker`)

It works with any self-hosted Matomo instance or Matomo Cloud. The only runtime dependency is [`requests`](https://pypi.org/project/requests/).

> Full guides live in [`docs/`](docs/): the [Reporting API guide](docs/reporting-api.md), the [Tracking API guide](docs/tracking-api.md), and a complete
> [API method reference](docs/api-reference.md) covering every module.

## Installation

```bash
pip install matomopy
```

Or, from a checkout of this directory:

```bash
pip install .
# for development (tests, linters):
pip install -e ".[dev]"
```

Requires Python 3.8+.

## Quick start — reading data

```python
from matomopy import MatomoClient

matomo = MatomoClient(
    "https://analytics.example.org",   # your Matomo URL
    token_auth="YOUR_AUTH_TOKEN",      # Administration > Personal > Security > Auth tokens
    default_id_site=1,                  # optional default site
)

# Core visit metrics for today:
summary = matomo.VisitsSummary.get(period="day", date="today")
print(summary["nb_visits"], "visits")

# Top 10 page URLs last month:
pages = matomo.Actions.getPageUrls(
    period="month", date="2024-01-01", filter_limit=10
)
for row in pages:
    print(row["label"], row["nb_hits"])
```

### Three ways to call the API

Every Matomo method is `Module.action`. You can reach all of them:

```python
# 1. Ergonomic attribute access (works for ANY module/method):
matomo.Referrers.getReferrerType(period="day", date="today")

# 2. The generic call() — handy when the method name is dynamic:
matomo.call("Referrers.getReferrerType", period="day", date="today")

# 3. Helpers that do more than a passthrough:
for row in matomo.paginate("Actions.getPageUrls", page_size=500):
    ...                     # streams every row, paging automatically
```

Because attribute access maps straight onto the HTTP method name, the client automatically supports plugins and methods added in future Matomo versions — nothing in this library needs to change.

### Parameters

Common parameters are first-class keyword arguments (`id_site`, `period`,
`date`, `segment`, `filter_limit`, `filter_offset`, `flat`, `expanded`).
Any other Matomo parameter is passed through using **its exact Matomo name**:

```python
matomo.Actions.getPageUrls(
    period="range",
    date="2024-01-01,2024-01-31",
    segment="deviceType==desktop",
    flat=True,
    filter_sort_column="nb_visits",   # exact Matomo param name
    hideColumns=["nb_hits", "sum_time_spent"],  # list -> comma-joined
)
```

- `bool` → `1`/`0`
- `list`/`tuple` → comma-joined (`idSites=[1,2]` → `idSites=1,2`)
- `dict` → PHP-style brackets (`filter[a]=1`)
- `None` → the parameter is omitted

### Output formats

`format="json"` (the default) is parsed into Python objects. Ask for another format to get the raw text, or `raw=True` for bytes (images, PDF exports):

```python
csv_text = matomo.VisitsSummary.get(period="day", date="today", format="csv")
png_bytes = matomo.ImageGraph.get(
    apiModule="VisitsSummary", apiAction="get",
    period="day", date="last30", raw=True,
)
```

### Batching

Run many reports in a single HTTP round-trip:

```python
results = matomo.bulk_request([
    {"method": "VisitsSummary.get", "idSite": 1, "period": "day",
     "date": "today"},
    {"method": "Actions.get", "idSite": 1, "period": "day",
     "date": "today"},
])
```

## Quick start — sending data

```python
from matomopy import MatomoTracker, generate_visitor_id

tracker = MatomoTracker(
    "https://analytics.example.org",
    id_site=1,
    token_auth="YOUR_TOKEN",   # only needed for privileged params
)
tracker.set_visitor_id(generate_visitor_id())

tracker.track_page_view("Checkout", url="https://shop.example/checkout")
tracker.track_event("Cart", "Add", name="SKU-123", value=1)
tracker.track_ecommerce_order(
    order_id="ORDER-42",
    grand_total=59.90,
    items=[["SKU-123", "Blue Shirt", "Apparel", 29.95, 2]],
)
```

### Converting a goal

A goal you set to trigger **manually** in Matomo (*Goals → Goal is triggered: manually*) is converted with `track_goal` — the Python equivalent of the JavaScript tracker's `_paq.push(['trackGoal', idGoal])`. Pass the goal's numeric ID, and optionally a revenue that overrides its configured default:

```python
tracker.track_goal(id_goal=1)                 # goal #1 ("New Registrations") converted
tracker.track_goal(id_goal=1, revenue=49.90)  # ...with a custom revenue for this conversion
```

See the [Tracking API guide](docs/tracking-api.md#goals) for a full server-side example (and how to create the manual goal from Python).

Queue events and send them in one request with bulk tracking:

```python
tracker.enable_bulk_tracking()
for path in ("/", "/pricing", "/signup"):
    tracker.track_page_view(path, url=f"https://shop.example{path}")
tracker.flush()   # single HTTP POST
```

## Authentication

Create a token in Matomo under **Administration → Personal → Security → Auth tokens**. The client never puts the token in the URL: by default it is sent in the POST body (`auth_method="post"`), or you can send it as a `Authorization: Bearer` header with `auth_method="bearer"`.

Give the token only the access it needs — a view-only user is enough for reporting.

## Errors

All exceptions subclass `MatomoError`:

| Exception | Raised when |
|-----------|-------------|
| `MatomoHTTPError` | The server returns a non-2xx status (has `.status_code`). |
| `MatomoAPIError` | Matomo returns `{"result": "error"}` in a 200 response. |
| `MatomoAuthenticationError` | A `MatomoAPIError` whose message indicates the token was rejected. |
| `MatomoConfigError` | The client was configured incorrectly. |

```python
from matomopy import MatomoError

try:
    matomo.VisitsSummary.get(period="day", date="today")
except MatomoError as exc:
    print("Matomo call failed:", exc)
```

## Testing

```bash
pip install -e ".[dev]"
pytest
```

The tests mock HTTP with `unittest.mock`, so they need no live server.

## License

MIT. See [LICENSE](LICENSE).
