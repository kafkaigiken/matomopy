# The Matomo Reporting API

The **Reporting API** is how you read analytics data out of Matomo over HTTP. It is a single endpoint that dispatches to hundreds of methods named `Module.action` (for example `VisitsSummary.get` or `Actions.getPageUrls`).
This guide explains the request structure, authentication, the parameters shared by every method, output formats, and pagination — the things you need to know once, that then apply everywhere.

For the catalogue of every method, see the [full method reference](api-reference.md). For sending data *into* Matomo, see the [Tracking API guide](tracking-api.md).

---

## The endpoint

Every reporting call goes to `index.php` at the root of your Matomo install with `module=API`:

```
https://analytics.example.org/index.php?module=API&method=<Module.action>&...
```

With this library you never build that URL by hand — you point the client at the base URL and it derives the endpoint:

```python
from matomo_pylib import MatomoClient

matomo = MatomoClient(
    "https://analytics.example.org",   # any of: root, root/, .../index.php
    token_auth="YOUR_TOKEN",
    default_id_site=1,
)
```

## Authentication

API calls run as a Matomo user and return only what that user is allowed to see. You authenticate with a **`token_auth`** created in Matomo under **Administration → Personal → Security → Auth tokens**.

Security notes:

- Prefer a token belonging to a **view-only** user for reporting. Give it no more access than it needs.
- Never put `token_auth` in a URL/query string — it can leak into logs. This library always sends it in the **POST body** (`auth_method="post"`, the default) or as an **`Authorization: Bearer` header** (`auth_method="bearer"`).
- Without a token, calls are anonymous and only return data for sites that allow anonymous view access.

```python
# Bearer-header authentication instead of the POST body:
matomo = MatomoClient(url, token_auth=TOKEN, auth_method="bearer")
```

## Choosing the method

The `method` is always `Module.action`. All three of these are equivalent:

```python
matomo.VisitsSummary.get(period="day", date="today")   # attribute access
matomo.call("VisitsSummary.get", period="day", date="today")
# raw HTTP: ?module=API&method=VisitsSummary.get&period=day&date=today
```

Attribute access (`matomo.<Module>.<action>`) works for **every** method in the reference — and for any method added by future Matomo versions or third-party plugins — because it maps directly onto the HTTP method name.

---

## Shared parameters

These parameters apply to (almost) every reporting method. In the library the most common ones are keyword arguments; the rest are passed through using their exact Matomo names.

### `idSite` — which site(s)

| Value | Meaning |
|-------|---------|
| `1` | A single site. |
| `1,2,3` (or `id_sites=[1,2,3]`) | Several sites (methods that support it, e.g. `MultiSites.getAll`). |
| `all` | Every site the token can access. |

```python
matomo.VisitsSummary.get(id_site=1, period="day", date="today")
```

`default_id_site` on the client is used whenever a call omits `id_site`.

### `period` and `date` — the time frame

`period` is one of `day`, `week`, `month`, `year`, or `range`. `date` selects
which period(s):

| `date` value | With `period` | Meaning |
|--------------|---------------|---------|
| `today` / `yesterday` | any | Relative single period. |
| `2024-01-31` | `day`/`week`/`month`/`year` | The period containing that date. |
| `last7` / `previous12` | any | A *series* of the N most recent periods (great for charts). |
| `2024-01-01,2024-01-31` | `range` | An explicit date range. |

```python
# One month:
matomo.VisitsSummary.get(period="month", date="2024-01-01")

# A daily time series for the last 30 days (returns {date: metrics}):
series = matomo.VisitsSummary.get(period="day", date="last30")

# An arbitrary range:
matomo.VisitsSummary.get(period="range", date="2024-01-01,2024-03-31")
```

When `date` selects multiple periods (e.g. `last30`), the response is keyed by period label instead of a single row.

### `segment` — filter the audience

A [segment](https://matomo.org/docs/segmentation/) restricts a report to a subset of visits. Pass a segment definition string:

```python
matomo.VisitsSummary.get(
    period="day", date="today",
    segment="deviceType==desktop;countryCode==us",
)
```

`;` means AND, `,` means OR. Discover available segment dimensions with
`matomo.get_segments_metadata()` (`API.getSegmentsMetadata`).

### `format` — the output format

| `format` | Returned by this library |
|----------|--------------------------|
| `json` (default) | Parsed `dict`/`list`. |
| `csv`, `tsv` | Decoded text. |
| `xml`, `rss` | Decoded text. |
| `original` | Text (PHP-serialised — rarely useful from Python). |

```python
csv_text = matomo.VisitsSummary.get(period="day", date="today", format="csv")
```

Binary endpoints (the `ImageGraph.get` PNG, PDF report exports) are fetched with `raw=True`, which returns `bytes`:

```python
png = matomo.ImageGraph.get(
    apiModule="VisitsSummary", apiAction="get",
    period="day", date="last30", raw=True,
)
open("visits.png", "wb").write(png)
```

---

## Shaping report rows

Report getters accept a family of parameters that sort, filter, limit and reshape the returned table. Pass them by their exact Matomo names.

### Limiting and paging

| Parameter | Effect |
|-----------|--------|
| `filter_limit` | Max rows to return. **`-1` returns all rows.** Over HTTP the default is 100. |
| `filter_offset` | Skip this many rows (manual paging). |

```python
# First 10 rows:
matomo.Actions.getPageUrls(period="month", date="today", filter_limit=10)

# Every row, streamed one page at a time (recommended for large reports):
for row in matomo.paginate("Actions.getPageUrls", period="month",
                           date="today", page_size=500):
    ...
```

### Sorting

| Parameter | Effect |
|-----------|--------|
| `filter_sort_column` | Metric/column to sort by, e.g. `nb_visits`. |
| `filter_sort_order` | `desc` (default) or `asc`. |

### Searching / filtering

| Parameter | Effect |
|-----------|--------|
| `filter_pattern` | Keep only rows whose label matches this pattern. |
| `filter_column` | Column the pattern applies to (default: the label). |
| `filter_excludelowpop` | Column used to drop low-traffic rows. |
| `filter_excludelowpop_value` | Threshold for the above. |
| `filter_truncate` | Group everything beyond N rows into an "Others" row. |

```python
matomo.Actions.getPageUrls(
    period="month", date="today",
    filter_pattern="blog", filter_sort_column="nb_hits",
)
```

### Hierarchy and columns

| Parameter | Effect |
|-----------|--------|
| `expanded` (`bool`) | Include subtables inline in the response. |
| `flat` (`bool`) | Flatten a hierarchical report into one level. |
| `idSubtable` | Fetch only the subtable of a specific row. |
| `columns` | Restrict the response to these metrics (comma list). |
| `hideColumns` / `showColumns` | Drop / keep specific columns. |

```python
matomo.Actions.getPageUrls(
    period="month", date="today",
    flat=True,                        # bool -> 1
    columns=["nb_visits", "nb_hits"], # list -> comma-joined
)
```

### Human-friendly output

| Parameter | Effect |
|-----------|--------|
| `format_metrics` | `1`/`0` — format metrics (e.g. times, percentages) for display. |
| `translateColumnNames` | `1`/`0` — return human-readable column names. |
| `language` | Locale for translated labels, e.g. `en`, `de`, `ja`. |

---

## Discovering reports at runtime

Matomo is self-documenting. These calls describe what a given instance offers, including third-party plugins:

```python
# Every report available for a site, with its metrics and metadata:
reports = matomo.get_report_metadata(id_site=1)

# A single report, already processed into human-readable rows + metrics:
processed = matomo.call(
    "API.getProcessedReport",
    id_site=1, period="day", date="today",
    apiModule="Actions", apiAction="getPageUrls",
)

# All segment dimensions you can use in `segment=`:
segments = matomo.get_segments_metadata(id_sites=[1])
```

## Batching many calls

`API.getBulkRequest` runs several methods in a single HTTP round-trip — far faster than issuing them one by one:

```python
visits, pages = matomo.bulk_request([
    {"method": "VisitsSummary.get", "idSite": 1, "period": "day",
     "date": "today"},
    {"method": "Actions.getPageUrls", "idSite": 1, "period": "day",
     "date": "today", "filter_limit": 5},
])
```

Each entry may also be a pre-built query string. One `token_auth` (the
client's) authorises the whole batch.

---

## Error handling

The Reporting API often signals a *logical* error with an HTTP `200` and a body like `{"result": "error", "message": "..."}`. This library detects that and raises, so you never have to inspect the payload yourself:

```python
from matomo_pylib import (
    MatomoError, MatomoAPIError, MatomoAuthenticationError, MatomoHTTPError,
)

try:
    matomo.VisitsSummary.get(period="day", date="today")
except MatomoAuthenticationError:
    ...  # token missing / rejected
except MatomoAPIError as exc:
    ...  # Matomo returned result=error; exc.message has the detail
except MatomoHTTPError as exc:
    ...  # non-2xx transport error; exc.status_code
except MatomoError:
    ...  # catch-all base class
```

## Performance & good citizenship

- Ask only for what you need: set a sensible `filter_limit`, use `columns` to trim metrics, and add a `segment` rather than pulling everything and filtering in Python.
- Use `bulk_request()` to combine calls.
- Requesting very recent data may trigger on-the-fly archiving on the server; historical periods are usually pre-archived and faster.
- Reuse one `MatomoClient` (it keeps an HTTP connection pool) rather than constructing a new one per call.

## Common metrics glossary

A handful of metric names appear across many reports:

| Metric | Meaning |
|--------|---------|
| `nb_visits` | Number of visits. |
| `nb_uniq_visitors` | Distinct visitors. |
| `nb_users` | Distinct logged-in user IDs. |
| `nb_actions` | Actions (page views, downloads, outlinks, searches). |
| `nb_actions_per_visit` | Average actions per visit. |
| `bounce_rate` | Share of single-action visits. |
| `avg_time_on_site` | Average visit duration. |
| `nb_hits` | Page/action hits (in Actions reports). |
| `nb_conversions`, `revenue` | Goal/ecommerce conversions and revenue. |

Matomo returns metric names verbatim in `format=json`; use `translateColumnNames=1` for human-readable labels.
