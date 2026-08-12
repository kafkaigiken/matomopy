# The Matomo Tracking API

The **Tracking API** is the endpoint Matomo's JavaScript tracker and mobile SDKs use to record data (`matomo.php`). You can call it from Python to track things that happen outside a browser — backend jobs, server-to-server events, purchases confirmed by a payment webhook, IoT devices, or importing historical data.

This library wraps it in `MatomoTracker`. For reading data back out, see the [Reporting API guide](reporting-api.md).

---

## The endpoint

Tracking requests go to `matomo.php` at the root of your install:

```
https://analytics.example.org/matomo.php?idsite=1&rec=1&...
```

Two parameters are always required: `idsite` (the site) and `rec=1` (record this request). The library adds them for you:

```python
from matomopy import MatomoTracker, generate_visitor_id

tracker = MatomoTracker(
    "https://analytics.example.org",   # or .../matomo.php
    id_site=1,
    token_auth="YOUR_TOKEN",           # optional; see "Privileged parameters"
)
```

## Identifying the visitor

A **visitor ID** is a 16-character hex string that ties multiple actions to one visitor. Generate one and reuse it for everything that belongs to the same visitor/session:

```python
tracker.set_visitor_id(generate_visitor_id())
```

If you know *who* the person is (a logged-in account), also set a **user ID** — Matomo links visits that share it, even across devices:

```python
tracker.set_user_id("customer-4815162342")
```

Visitor state set on the tracker (`set_url`, `set_resolution`, `set_url_referrer`, custom dimensions, ...) persists across calls, just like the JavaScript tracker within a page.

---

## What you can track

Every method below issues one tracking request (or queues it — see [Bulk tracking](#bulk-tracking)).

### Page views

```python
tracker.track_page_view("Checkout", url="https://shop.example/checkout")
```

`action_name` is the page title shown in reports; `url` is the page address. Set a default URL once with `tracker.set_url(...)` if many calls share it.

### Events

Category / action / optional name / optional numeric value:

```python
tracker.track_event("Cart", "Add", name="SKU-123", value=1)
tracker.track_event("Video", "Play", name="Intro")
```

### Goals

A goal configured to be triggered **manually** (in Matomo: **Websites → Manage → Goals**, with *Goal is triggered* set to `manually`) converts only when your code explicitly says so — there is no URL, title or event for Matomo to match on. `track_goal` is the Python equivalent of the JavaScript tracker's [`trackGoal`](https://developer.matomo.org/guides/tracking-javascript-guide#manually-trigger-goal-conversions): `_paq.push(['trackGoal', 1])` becomes `tracker.track_goal(1)`.

Pass the numeric **goal ID** shown on the Goals management screen (or returned by `Goals.getGoals` — see the [Reporting API guide](reporting-api.md)):

```python
tracker.track_goal(id_goal=1)
```

Override the goal's default revenue for this one conversion — the same as `_paq.push(['trackGoal', 1, 49.90])`:

```python
tracker.track_goal(id_goal=1, revenue=49.90)
```

A complete server-side conversion — for example recording the "New Registrations" goal (ID `1`) after a signup finishes on your backend:

```python
from matomopy import MatomoTracker, generate_visitor_id

tracker = MatomoTracker("https://analytics.example.org", id_site=1)
tracker.set_visitor_id(generate_visitor_id())
tracker.set_user_id("customer-4815162342")   # optional: tie it to the account

tracker.track_goal(id_goal=1)                 # goal "New Registrations" converted
```

If the person is a **known visitor**, reuse *their* existing 16-character visitor ID (or set their user ID) so the conversion is attributed to the right visit instead of starting a brand new one.

> **Tip — create the manual goal from Python too.** You don't have to click through the UI. The [Reporting API](reporting-api.md) can create it with `matchAttribute="manually"`:
> 
> ```python
>from matomopy import MatomoClient
> 
> matomo = MatomoClient("https://analytics.example.org", token_auth="YOUR_TOKEN")
>id_goal = matomo.Goals.addGoal(
>  id_site=1,
>  name="New Registrations",
>     matchAttribute="manually",   # the "triggered manually" goal type
>     pattern="",                  # ignored for manual goals
>     patternType="",              # ignored for manual goals
>     description="How many of our visitors register for a new account",
>    )
>    # id_goal is then what you pass to tracker.track_goal(id_goal=...)
> ```

### Site search

```python
tracker.track_site_search("blue shoes", category="Footwear",
                          count_results=42)
```

### Downloads and outlinks

```python
tracker.track_action("https://cdn.example/report.pdf",
                     action_type="download")
tracker.track_action("https://partner.example", action_type="link")
```

The request's `url` stays the page the action happened on (whatever `set_url()`
holds), and the downloaded or clicked URL is reported separately — set the page
URL first so downloads and outlinks are attributed to the right page.

### Content impressions and interactions

```python
tracker.track_content_impression("Promo banner", piece="summer-sale",
                                 target="https://shop.example/sale")
tracker.track_content_interaction("click", "Promo banner",
                                  piece="summer-sale")
```

### Ecommerce

Track a completed order (items are
`[sku, name, category, price, quantity]`, trailing fields optional, or dicts):

```python
tracker.track_ecommerce_order(
    order_id="ORDER-42",
    grand_total=59.90,
    sub_total=49.90,
    tax=6.00,
    shipping=4.00,
    discount=0.00,
    items=[
        ["SKU-123", "Blue Shirt", "Apparel", 29.95, 2],
        {"sku": "SKU-9", "name": "Cap", "category": "Apparel",
         "price": 9.90, "quantity": 1},
    ],
)

# Or record the current cart state (no order id):
tracker.track_ecommerce_cart_update(grand_total=39.85, items=[...])
```

### Keeping a visit alive

A **ping** extends the recorded visit duration without logging a new action:

```python
tracker.track_ping()
```

---

## Custom dimensions

Attach [custom dimension](https://matomo.org/docs/custom-dimensions/) values by their configured slot ID. They stay set until you change them:

```python
tracker.set_custom_dimension(1, "premium-plan")
tracker.set_custom_dimension(2, "eu-west")
tracker.track_page_view("Dashboard")
```

## Visit context

```python
tracker.set_resolution(1920, 1080)
tracker.set_url_referrer("https://google.com/search?q=...")
tracker.set_force_new_visit()   # force the next request to start a new visit
```

`User-Agent` and `Accept-Language` — which drive Matomo's device, browser and language reports — are set on the constructor when you proxy tracking for a real client:

```python
tracker = MatomoTracker(
    url, id_site=1,
    user_agent="Mozilla/5.0 (...) Chrome/120 ...",
    accept_language="en-GB,en;q=0.9",
)
```

---

## Privileged parameters (require `token_auth`)

Some parameters are only honoured when the tracker has a `token_auth` with at
least write access to the site. Without it, Matomo ignores them (it will not error):

| Method | Overrides | Notes |
|--------|-----------|-------|
| `set_ip("203.0.113.7")` | The visitor IP (`cip`) | Drives geolocation; use for server-side tracking. |
| `set_custom_timestamp(epoch)` | The event time (`cdt`) | Needed for importing historical events (older than a few hours requires the token). |

```python
import time

tracker.set_ip("203.0.113.7")
tracker.set_custom_timestamp(int(time.time()) - 86_400)  # yesterday
tracker.track_page_view("Imported page")
```

---

## Bulk tracking

For high volume or batch imports, queue requests and send them in a single HTTP POST instead of one request each:

```python
tracker.enable_bulk_tracking()
for path in ("/", "/pricing", "/signup"):
    tracker.track_page_view(path, url=f"https://shop.example{path}")

tracker.flush()   # one HTTP POST containing all queued requests
```

Bulk requests are sent as a JSON body. If the tracker has a `token_auth`, it authenticates the whole batch (required if any queued request uses a privileged parameter).

## Errors

Tracking methods raise `MatomoHTTPError` if the server returns a non-2xx status; transport failures raise it too. Successful tracking returns the `requests.Response` (Matomo replies with `204 No Content` because the library sends `send_image=0`).

```python
from matomopy import MatomoHTTPError

try:
    tracker.track_page_view("Home")
except MatomoHTTPError as exc:
    print("tracking failed:", exc.status_code)
```

## Reference: parameter mapping

For readers who want to correlate with the raw HTTP API, the main parameters this library sends:

| Concept | Matomo parameter(s) |
|---------|---------------------|
| Site / record | `idsite`, `rec=1`, `apiv=1` |
| Page view | `action_name`, `url` |
| Visitor / user | `_id`, `cid`, `uid` |
| Event | `e_c`, `e_a`, `e_n`, `e_v` |
| Goal | `idgoal`, `revenue` |
| Site search | `search`, `search_cat`, `search_count` |
| Content | `c_n`, `c_p`, `c_t`, `c_i` |
| Ecommerce | `idgoal=0`, `ec_id`, `ec_items`, `revenue`, `ec_st`, `ec_tx`, `ec_sh`, `ec_dt` |
| Download / outlink | `download`, `link` |
| Custom dimensions | `dimension<ID>` |
| Context | `res`, `urlref`, `lang`, `new_visit` |
| Privileged | `cip`, `cdt`, `token_auth` |

The [official tracking parameter list](https://developer.matomo.org/api-reference/tracking-api) documents every possible parameter if you need one not wrapped here — pass it through by extending the tracker or using a raw request.
