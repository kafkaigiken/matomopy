# Matomo Reporting API — full method reference

This reference documents **366 HTTP API methods** across **47 modules**, extracted directly from the Matomo source. Every method is callable over HTTP as `?module=API&method=Module.action` and from this library as `client.Module.action(...)`.

> New to the API? Start with the [Reporting API guide](reporting-api.md), which explains authentication, the shared parameters (`idSite`, `period`, `date`, `segment`, `filter_*`, ...), output formats and pagination that apply to **every** method below.

## How to read this reference

- **Type** — *Report getter* methods return a table of metrics for an `idSite`/`period`/`date` (and accept the shared reporting parameters). *Action* methods create, update, delete or read configuration.
- **Access** — the permission the authenticating token needs. Report getters generally need *view* access to the site; write and admin operations need more.
- **Parameters** — only the parameters specific to the method are listed. Report getters also accept every shared reporting parameter documented in the [Reporting API guide](reporting-api.md).
- **Returns** — the shape of the data Matomo sends back.
- Methods marked *(internal)* or *(deprecated)* are callable but not part of the stable public contract — avoid depending on them.

## Modules by category

**Metadata & cross-report API**  
[API](#api) (20)

**Visits & visitor overview**  
[VisitsSummary](#visitssummary) (10) · [VisitFrequency](#visitfrequency) (1) · [VisitTime](#visittime) (3) · [VisitorInterest](#visitorinterest) (4) · [Live](#live) (7)

**Visitor attributes**  
[UserId](#userid) (1) · [UserCountry](#usercountry) (8) · [UserLanguage](#userlanguage) (2) · [Resolution](#resolution) (2) · [DevicesDetection](#devicesdetection) (8) · [DevicePlugins](#deviceplugins) (1)

**Content & behaviour**  
[Actions](#actions) (18) · [Contents](#contents) (2) · [PagePerformance](#pageperformance) (1) · [Events](#events) (9) · [Transitions](#transitions) (5) · [Insights](#insights) (5)

**Goals & ecommerce**  
[Goals](#goals) (12)

**Acquisition & referrers**  
[Referrers](#referrers) (23) · [MultiSites](#multisites) (3) · [SEO](#seo) (1)

**Bots & AI traffic**  
[BotTracking](#bottracking) (9) · [AIAgents](#aiagents) (1)

**Custom dimensions**  
[CustomDimensions](#customdimensions) (7)

**Segments & annotations**  
[SegmentEditor](#segmenteditor) (9) · [Annotations](#annotations) (7)

**Graphs, exports & scheduled reports**  
[ImageGraph](#imagegraph) (1) · [ScheduledReports](#scheduledreports) (7) · [MobileMessaging](#mobilemessaging) (12)

**Site management**  
[SitesManager](#sitesmanager) (55)

**Users, permissions & login**  
[UsersManager](#usersmanager) (32) · [TwoFactorAuth](#twofactorauth) (1) · [Login](#login) (1)

**Privacy & GDPR**  
[PrivacyManager](#privacymanager) (17)

**Dashboards & personal settings**  
[Dashboard](#dashboard) (5) · [LanguagesManager](#languagesmanager) (9) · [Feedback](#feedback) (3) · [Tour](#tour) (3)

**Instance administration**  
[CoreAdminHome](#coreadminhome) (13) · [CorePluginsAdmin](#corepluginsadmin) (5) · [DBStats](#dbstats) (11) · [Marketplace](#marketplace) (5) · [ProfessionalServices](#professionalservices) (1)

**Tracker & installation helpers**  
[CustomJsTracker](#customjstracker) (1) · [JsTrackerInstallCheck](#jstrackerinstallcheck) (2) · [Overlay](#overlay) (3)

---

## API

_The Metadata API: gives information about all other available API methods and returns human-readable, processed versions of any report._

### API.getMatomoVersion

**Type:** Action
**Access:** Some view access (at least one site)
**Description:** Returns the current Matomo version.

**Parameters:**

_None._

**Returns:** string — Matomo's version string.

### API.getPhpVersion

**Type:** Action
**Access:** Super user
**Description:** Returns information about the PHP runtime version.

**Parameters:**

_None._

**Returns:** array with keys `version`, `major`, `minor`, `release`, `versionId`, `extra`.

### API.getPiwikVersion

**Type:** Action
**Access:** Some view access (inherited via getMatomoVersion; no direct check)
**Description:** Returns the current Matomo version. _(Deprecated — kept for backward compatibility.)_

**Parameters:**

_None._

**Returns:** string — Matomo's version string.

### API.getIpFromHeader

**Type:** Action
**Access:** Some view access (at least one site)
**Description:** Returns the most accurate IP address available for the current user, in IPv4 format (may be the proxy client's IP address).

**Parameters:**

_None._

**Returns:** string — IP address in presentation format.

### API.getSettings

**Type:** Action
**Access:** None (public)
**Description:** Returns the `[APISettings]` section from `config.ini.php`. _(Deprecated — may be removed in a future major release.)_

**Parameters:**

_None._

**Returns:** array — the `APISettings` config section.

### API.getAvailableMeasurableTypes

**Type:** Action
**Access:** Some view access (at least one site)
**Description:** Returns all available measurable types. _(Marked `@internal` — not shown on the API page.)_

**Parameters:**

_None._

**Returns:** list of measurable types, each with `id`, `name`, `description`, `longDescription`, `howToSetupUrl`, `settings`.

### API.getSegmentsMetadata

**Type:** Action
**Access:** Some view access if no site given; otherwise view access to the given site(s)
**Description:** Returns metadata for all available segments.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSites | int[]\|int\|string | no | `array()` (empty) | One or more site IDs; if empty, returns metadata visible to the current user. |
| _hideImplementationData | bool | no | `true` | Whether internal implementation details should be omitted. |
| _showAllSegments | bool | no | `false` | Whether to include segments that are normally hidden. |

**Returns:** array of segment metadata.

### API.getMetadata

**Type:** Action
**Access:** View access to site
**Description:** Returns metadata for a specific API method.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID to use when loading metadata. |
| apiModule | string | yes | — | API module name. |
| apiAction | string | yes | — | API method name without the module prefix. |
| apiParameters | array | no | `[]` | Additional API parameters used to resolve metadata variants. |
| language | string\|false | no | `false` | Optional language code used to localize the response. |
| period | string\|false | no | `false` | Optional period used to resolve period-dependent metadata. |
| date | string\|false | no | `false` | Optional date or date range used to resolve metadata. |
| hideMetricsDoc | bool | no | `false` | Whether metric documentation should be omitted. |
| showSubtableReports | bool | no | `false` | Whether subtable reports should be included. |

**Returns:** array of metadata for the requested method.

### API.getReportMetadata

**Type:** Action
**Access:** View access to site
**Description:** Returns metadata for all available reports.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSites | int[]\|int\|string | no | `''` | Deprecated fallback for specifying one or more site IDs. |
| period | string\|false | no | `false` | Optional period used to resolve report metadata. |
| date | string\|false | no | `false` | Optional date or date range used to resolve report metadata. |
| hideMetricsDoc | bool | no | `false` | Whether metric documentation should be omitted. |
| showSubtableReports | bool | no | `false` | Whether subtable reports should be included. |
| idSite | int\|string\|false | no | `false` | Preferred site ID parameter (at least one site ID is required overall). |

**Returns:** array of report metadata.

### API.getProcessedReport

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a processed report with metadata, formatting, and processed metrics (e.g. conversion rate, time on site) applied.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID to query. |
| period | string | yes | — | Report period. |
| date | string | yes | — | Date or date range to query. |
| apiModule | string | yes | — | API module name. |
| apiAction | string | yes | — | API method name without the module prefix. |
| segment | string\|false | no | `false` | Optional segment expression. |
| apiParameters | array\|false | no | `false` | Additional API parameters forwarded to the target report. |
| idGoal | int\|string\|false | no | `false` | Optional goal ID. |
| language | string\|false | no | `false` | Optional language code for the response. |
| showTimer | bool | no | `true` | Whether processing time information should be included. |
| hideMetricsDoc | bool | no | `false` | Whether metric documentation should be omitted. |
| idSubtable | int\|string\|false | no | `false` | Optional subtable ID to load. |
| showRawMetrics | bool | no | `false` | Whether raw metrics should be included alongside formatted metrics. |
| format_metrics | string\|null | no | `null` | Optional metrics formatting mode. |
| idDimension | int\|string\|false | no | `false` | Optional dimension ID. |

**Returns:** array — processed report data (metadata plus the report DataTable).

### API.getReportPagesMetadata

**Type:** Action
**Access:** View access to site
**Description:** Returns page metadata for the Matomo UI, including the widgets shown on each page.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID used for the access check. |

**Returns:** array of page metadata.

### API.getWidgetMetadata

**Type:** Action
**Access:** View access to site
**Description:** Returns metadata for all widgets that can be displayed in the UI.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID used for the access check. |

**Returns:** array of widget metadata.

### API.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a combined report built by merging the `*.get` API methods of other plugins into a single DataTable.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID to query. |
| period | string | yes | — | Report period. |
| date | string | yes | — | Date or date range to query. |
| segment | string\|false | no | `false` | Optional segment expression. |
| columns | string[]\|string\|false | no | `false` | Optional metric names to keep in the combined result. |

**Returns:** DataTable — the merged report.

### API.getRowEvolution

**Type:** Report getter
**Access:** View access to site
**Description:** Returns an evolution series over time for a specific report row or metric label.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID to query. |
| period | string | yes | — | Period to calculate the evolution for. |
| date | string | yes | — | Date or date range to query. |
| apiModule | string | yes | — | API module name. |
| apiAction | string | yes | — | API method name without the module prefix. |
| label | string\|false | no | `false` | Optional row label to track. |
| segment | string\|false | no | `false` | Optional segment expression. |
| column | string\|false | no | `false` | Optional metric column to use. |
| language | string\|false | no | `false` | Optional language code for the response. |
| idGoal | int\|string\|false | no | `false` | Optional goal ID. |
| legendAppendMetric | bool\|string | no | `true` | Whether to append the metric name to the legend. |
| labelUseAbsoluteUrl | bool\|string | no | `true` | Whether URL labels should be normalized to absolute URLs. |
| idDimension | int\|string\|false | no | `false` | Optional dimension ID. |
| labelSeries | string\|false | no | `false` | Optional custom series label. |
| showGoalMetricsForGoal | int\|string\|false | no | `false` | Optional goal ID whose goal metrics should be included. |

**Returns:** array — evolution series data.

### API.getBulkRequest

**Type:** Action
**Access:** None directly (each sub-request enforces its own access); `API.getBulkRequest` calls are skipped to prevent recursion
**Description:** Performs multiple API requests at once and returns every result.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| urls | string[] | yes | — | API query strings to execute. |

**Returns:** array — one decoded JSON result per requested URL.

### API.isPluginActivated

**Type:** Action
**Access:** Some view access (at least one site)
**Description:** Returns whether a plugin is currently activated.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pluginName | string | yes | — | Plugin name to check. |

**Returns:** bool.

### API.getSuggestedValuesForSegment

**Type:** Action
**Access:** View access to site
**Description:** Returns top suggested values for a segment based on recent visitor data or a segment-specific callback.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| segmentName | string | yes | — | Segment name to suggest values for. |
| idSite | int\|string | yes | — | Site ID to query, or `'all'` for all sites where supported. |

**Returns:** array of suggested segment values.

### API.getPagesComparisonsDisabledFor

**Type:** Action
**Access:** None (public)
**Description:** Returns category/subcategory pairs (as `"CategoryId.SubcategoryId"`) for which comparison features should be disabled.

**Parameters:**

_None._

**Returns:** string[] — page identifiers with comparison disabled.

### API.getGlossaryReports

**Type:** Action
**Access:** None (public)
**Description:** Returns glossary entries for all reports.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID used to build the reports glossary. |

**Returns:** array of report glossary entries.

### API.getGlossaryMetrics

**Type:** Action
**Access:** None (public)
**Description:** Returns glossary entries for all metrics.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID used to build the metrics glossary. |

**Returns:** array of metric glossary entries.

## VisitsSummary

_Access the core web analytics metrics: visits, unique visitors, actions, time on site, bounces and converted visits._

### VisitsSummary.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the VisitsSummary overview report for the requested period — the primary reporting method for core visit metrics.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |
| columns | string\|string[]\|false | no | false | Specific metrics to include, or false for the default set |

**Returns:** DataTable|DataTable\Map of VisitsSummary metrics for the requested period.

### VisitsSummary.getVisits

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of visits in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the number of visits.

### VisitsSummary.getUniqueVisitors

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of unique visitors in the requested period (fails if unique visitors are not enabled for the period).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the number of unique visitors.

### VisitsSummary.getUsers

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of users in the requested period (fails if unique visitors are not enabled for the period).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the number of users.

### VisitsSummary.getActions

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of actions in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the number of actions.

### VisitsSummary.getMaxActions

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the maximum number of actions in a single visit for the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the maximum actions value.

### VisitsSummary.getBounceCount

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of bounces in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the bounce count.

### VisitsSummary.getVisitsConverted

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of converted visits in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with converted visits.

### VisitsSummary.getSumVisitsLength

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the total visit duration in seconds for the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with total visit duration.

### VisitsSummary.getSumVisitsLengthPretty

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the total visit duration formatted as human-readable text.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with human-readable visit duration values.

## VisitFrequency

_Lets you access a list of metrics related to Returning Visitors._

### VisitFrequency.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit summary metrics split between new and returning visitors, with `_new` and `_returning` column suffixes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment appended to the visitor type filters |
| columns | list<string>\|string\|null | no | null | Metrics to include; comma-separated list or array |

**Returns:** DataTable\DataTableInterface — visit summary metrics with `_new` and `_returning` column suffixes.

## VisitTime

_Access reports by hour (server time) and by hour local time of visitors, plus day of week._

### VisitTime.getVisitInformationPerLocalTime

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit counts grouped by each visitor's local hour at the start of the visit.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — visit counts grouped by each visitor's local hour.

### VisitTime.getVisitInformationPerServerTime

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit counts grouped by the queried site's hour at the start of the visit.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| hideFutureHoursWhenToday | bool | no | false | Omit hours later than the current hour (site timezone) when querying today |

**Returns:** DataTable|DataTable\Map — visit counts grouped by hour in the queried site's timezone.

### VisitTime.getByDayOfWeek

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit counts grouped by day of the week. Does not support multiple sites or multiple dates (unless period is 'range').

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query (single site only) |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable — visit counts grouped into day-of-week rows for the requested period.

## VisitorInterest

_Lets you access visitor engagement distribution reports, including visits by pages viewed, visit duration, days since last visit, and visit count._

### VisitorInterest.getNumberOfVisitsPerVisitDuration

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit-duration distribution metrics (visit counts grouped by visit duration ranges) for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — visit counts grouped by visit duration ranges.

### VisitorInterest.getNumberOfVisitsPerPage

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page-depth distribution metrics (visit counts grouped by pages-per-visit ranges) for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — visit counts grouped by pages-per-visit ranges.

### VisitorInterest.getNumberOfVisitsByDaysSinceLast

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the distribution of visits by days since the previous visit.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — visit counts grouped by days since the last visit.

### VisitorInterest.getNumberOfVisitsByVisitCount

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the distribution of visits by lifetime visit count.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — visit counts grouped by visit count ranges.

## Live

_Access complete visit-level (raw) data about visitors, real-time counters and visitor profiles, filterable by segment._

### Live.getCounters

**Type:** Report getter
**Access:** View access to site
**Description:** Returns simple live counters (visits, actions, visitors, converted visits) for the last N minutes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|int[] | yes | — | Website ID or IDs to query |
| lastMinutes | int | yes | — | Number of minutes to look back (1 to 2880) |
| segment | string\|null\|false | no | false | Segment to filter the counters |
| showColumns | string\|string[] | no | [] | Columns to include (e.g. visits, actions) |
| hideColumns | string\|string[] | no | [] | Columns to omit from the response |

**Returns:** A single-row array containing the requested counters.

### Live.isVisitorProfileEnabled

**Type:** Report getter
**Access:** None (public)
**Description:** Returns whether the visitor profile feature is enabled for the given site selection.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID or site selection to query |

**Returns:** bool — whether visitor profiles are enabled.

### Live.getLastVisitsDetails

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the most recent visit details (extensive raw data per visit) for one or more websites, filterable by segment. Key method for pulling raw visit data.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | 'day'\|'week'\|'month'\|'year'\|'range'\|false | no | false | Period restriction |
| date | string\|false | no | false | Date or date-range restriction |
| segment | string\|null\|false | no | false | Segment to filter the visits |
| countVisitorsToFetch | int\|false | no | false | Deprecated explicit row limit; prefer filter_offset/filter_limit |
| minTimestamp | int\|false | no | false | Minimum timestamp for incremental refreshes/pagination |
| flat | bool | no | false | Whether to flatten action details into visit rows |
| doNotFetchActions | bool | no | false | Whether to skip fetching action details for performance |
| enhanced | bool | no | false | Whether plugins should enrich the returned visit details |

**Returns:** DataTable of recent visit details.

### Live.getVisitorProfile

**Type:** Report getter
**Access:** View access to site
**Description:** Builds and returns a visitor profile from a visitor's recent visits. Key method for pulling raw visit data.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| visitorId | string\|false | no | false | Visitor ID; if omitted, the most recent visitor is used |
| segment | string\|null\|false | no | false | Segment to filter the profile lookup |
| limitVisits | int\|false | no | false | Maximum number of visits to include in the profile |

**Returns:** Array of visitor profile data, or an empty array if no visitor is found.

### Live.getMostRecentVisitorId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the visitor ID of the most recent matching visit (searching last 7 days, then 1 year, then all logs).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| segment | string\|null\|false | no | false | Segment to filter the lookup |

**Returns:** string visitor ID of the most recent matching visit, or false if none is found.

### Live.getFirstVisitForVisitorId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the very first visit for the given visitor ID. (Internal.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|int[] | yes | — | Website ID or IDs |
| visitorId | string\|false | yes | — | Visitor ID to look up |

**Returns:** DataTable with the first matching visit, or an empty table if no visitor ID is provided.

### Live.getMostRecentVisitsDateTime

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the most recent UTC datetime when an action was performed for the given website(s).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|int[] | yes | — | Website ID or IDs to query |
| period | 'day'\|'week'\|'month'\|'year'\|'range'\|null | no | null | Period restriction |
| date | string\|null | no | null | Date or date-range restriction |

**Returns:** string — most recent visit datetime in UTC, or an empty string if none exists.

## UserId

_Provides API methods for User ID reports._

### UserId.getUsers

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the User ID report (metrics per user ID) for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Site ID(s): single, array, comma-separated list, or 'all' |
| period | string | yes | — | day/week/month/year/range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable (or DataTable\Map) of User ID metrics.

## UserCountry

_Lets you access reports about your visitors' countries, continents, regions, and cities._

### UserCountry.getCountry

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by country, with translated labels and flag metadata.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — country rows with translated labels and flag metadata.

### UserCountry.getContinent

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by continent, with translated labels and continent codes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — continent rows with translated labels and continent codes.

### UserCountry.getRegion

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information for every region with at least one visit, with country, region, and flag metadata.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — region rows with country, region, and flag metadata.

### UserCountry.getCity

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information for every city with at least one visit, with city, region, country, and flag metadata.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — city rows with city, region, country, and flag metadata.

### UserCountry.getCountryCodeMapping

**Type:** Action
**Access:** None (public)
**Description:** Returns a mapping from ISO country code to translated country name.

_None._

**Returns:** array<string, string> — country names keyed by lowercase ISO country code.

### UserCountry.getLocationFromIP

**Type:** Action
**Access:** View access to at least one site (checkUserHasSomeViewAccess)
**Description:** Uses a location provider to find/guess the location of an IP address.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| ip | string\|false | no | false | IP address to geolocate, or false to use the current request IP |
| provider | string\|false | no | false | Provider ID to use, or false for the currently configured provider |

**Returns:** array — location data returned by the selected provider.

### UserCountry.setLocationProvider

**Type:** Action
**Access:** Super user
**Description:** Sets the active geolocation provider (throws if geolocation admin is disabled in config).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| providerId | string | yes | — | Provider ID to activate (e.g. `default` or `geoip2_php`) |

**Returns:** void.

### UserCountry.getNumberOfDistinctCountries

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct countries in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — numeric archive result with the number of distinct countries.

## UserLanguage

_Access reports about your visitors' language settings._

### UserLanguage.getLanguage

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visitor language metrics grouped by base language code.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of visitor language metrics grouped by language code.

### UserLanguage.getLanguageCode

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visitor language metrics grouped by full locale code.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of visitor language metrics grouped by locale code.

## Resolution

_API methods for screen resolution and device configuration reports._

### Resolution.getResolution

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visitor screen resolution metrics for the requested site and period (sites with resolution detection disabled by compliance policy are filtered out).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of screen resolution metrics.

### Resolution.getConfiguration

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visitor device configuration metrics (OS + browser + resolution) for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of device configuration metrics.

## DevicesDetection

_Lets you access reports about your visitors' device types, brands, models, operating systems, and browsers._

### DevicesDetection.getType

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by device type; always includes every detectable device type, even those with zero visits.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — device type report with segment metadata for each device type.

### DevicesDetection.getBrand

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by device brand (mostly available for non-desktop devices).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — device brand report with segment metadata for each detected brand.

### DevicesDetection.getModel

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by device model; unavailable when model detection is disabled by compliance policy.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — device model report with segment metadata for each brand/model pair.

### DevicesDetection.getOsFamilies

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by operating system family (falls back to OS version data for legacy archives).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — OS family report with grouped family labels and logos.

### DevicesDetection.getOsVersions

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by operating system version, with segment metadata for OS code and version.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — OS version report with segment metadata and logos.

### DevicesDetection.getBrowsers

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by browser family without version numbers (falls back to browser version data for legacy archives).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — browser family report with grouped browser names and logos.

### DevicesDetection.getBrowserVersions

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by browser version, with segment metadata for browser code and detected version.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — browser version report with rewritten labels and logos.

### DevicesDetection.getBrowserEngines

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit information grouped by browser engine, with labels normalized to detected engine names.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — browser engine report with grouped engine names.

## DevicePlugins

_Lets you access reports about device plugins such as browser plugins._

### DevicePlugins.getPlugin

**Type:** Report getter
**Access:** View access to site
**Description:** Returns metrics for detected browser plugins on the requested site, adding a visits-percentage metric (excluding Internet Explorer users, for which plugin detection does not work).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — browser plugin metrics with visit percentages.

## Actions

_Request visitor action reports: page URLs, page titles, downloads, outlinks, site search, entry/exit pages._

### Actions.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns aggregated action metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| columns | list<string>\|string\|false | no | false | Metrics to include (comma-separated list or array of metric names) |

**Returns:** DataTable\|DataTable\Map — action metrics for the selected site, period, and segment.

### Actions.getPageUrls

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URL metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| depth | int\|null\|false | no | false | Maximum subtable depth when expanding results |
| flat | bool | no | false | Flatten the hierarchical URL report into a single table |

**Returns:** DataTable\|DataTable\Map — page URL metrics for the requested action rows.

### Actions.getPageUrlsFollowingSiteSearch

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URL metrics for pages viewed immediately after an internal site search.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |

**Returns:** DataTable\|DataTable\Map — page URLs that followed an internal search.

### Actions.getPageTitlesFollowingSiteSearch

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page title metrics for pages viewed immediately after an internal site search.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |

**Returns:** DataTable\|DataTable\Map — page titles that followed an internal search.

### Actions.getEntryPageUrls

**Type:** Report getter
**Access:** View access to site
**Description:** Returns analytics information for every unique entry page URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical URL report into a single table |

**Returns:** DataTable\|DataTable\Map — entry page URL metrics.

### Actions.getExitPageUrls

**Type:** Report getter
**Access:** View access to site
**Description:** Returns analytics information for every unique exit page URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical URL report into a single table |

**Returns:** DataTable\|DataTable\Map — exit page URL metrics.

### Actions.getPageUrl

**Type:** Report getter
**Access:** View access to site
**Description:** Returns metrics for a specific page URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pageUrl | string | yes | — | The URL-encoded page URL to look up |
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — metrics for the requested page URL, or an empty table if not found.

### Actions.getPageTitles

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page title metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical title report into a single table |

**Returns:** DataTable\|DataTable\Map — page title metrics for the requested action rows.

### Actions.getEntryPageTitles

**Type:** Report getter
**Access:** View access to site
**Description:** Returns analytics information for every unique entry page title.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical title report into a single table |

**Returns:** DataTable\|DataTable\Map — entry page title metrics.

### Actions.getExitPageTitles

**Type:** Report getter
**Access:** View access to site
**Description:** Returns analytics information for every unique exit page title.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical title report into a single table |

**Returns:** DataTable\|DataTable\Map — exit page title metrics.

### Actions.getPageTitle

**Type:** Report getter
**Access:** View access to site
**Description:** Returns metrics for a specific page title.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pageName | string | yes | — | The URL-encoded page title to look up |
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — metrics for the requested page title, or an empty table if not found.

### Actions.getDownloads

**Type:** Report getter
**Access:** View access to site
**Description:** Returns download metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical download report into a single table |

**Returns:** DataTable\|DataTable\Map — download metrics for the requested action rows.

### Actions.getDownload

**Type:** Report getter
**Access:** View access to site
**Description:** Returns metrics for a specific download URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| downloadUrl | string | yes | — | The URL-encoded download URL to look up |
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — metrics for the requested download URL, or an empty table if not found.

### Actions.getOutlinks

**Type:** Report getter
**Access:** View access to site
**Description:** Returns outlink metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Expand all rows and include their subtables |
| idSubtable | int\|null\|false | no | false | Subtable ID to fetch instead of the top-level report |
| flat | bool | no | false | Flatten the hierarchical outlink report into a single table |

**Returns:** DataTable\|DataTable\Map — outlink metrics for the requested action rows.

### Actions.getOutlink

**Type:** Report getter
**Access:** View access to site
**Description:** Returns metrics for a specific outlink URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| outlinkUrl | string | yes | — | The URL-encoded outlink URL to look up |
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — metrics for the requested outlink URL, or an empty table if not found.

### Actions.getSiteSearchKeywords

**Type:** Report getter
**Access:** View access to site
**Description:** Returns internal search keywords that produced search results.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — site search keywords that returned at least one result.

### Actions.getSiteSearchNoResultKeywords

**Type:** Report getter
**Access:** View access to site
**Description:** Returns internal search keywords that produced no results.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — site search keywords that returned no results.

### Actions.getSiteSearchCategories

**Type:** Report getter
**Access:** View access to site
**Description:** Returns internal search categories used by visitors on the site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — site search categories and their metrics.

## Contents

_Content tracking reports grouped by content name and content piece._

### Contents.getContentNames

**Type:** Report getter
**Access:** View access to site
**Description:** Returns content tracking metrics grouped by content name.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idSubtable | int\|null\|false | no | false | Subtable ID; when set, returns content pieces for the selected content name row |

**Returns:** DataTable\|DataTable\Map — content name rows with impressions, interactions, and interaction rate.

### Contents.getContentPieces

**Type:** Report getter
**Access:** View access to site
**Description:** Returns content tracking metrics grouped by content piece.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idSubtable | int\|null\|false | no | false | Subtable ID; when set, returns content names for the selected content piece row |

**Returns:** DataTable\|DataTable\Map — content piece rows with impressions, interactions, and interaction rate.

## PagePerformance

_Reporting API for aggregated page performance timing metrics._

### PagePerformance.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns aggregated page performance metrics for the requested site and period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — metrics for network, server, transfer, DOM, and page load timings.

## Events

_Lets you request reports about your users' Custom Events (category, action, name, and optional value)._

### Events.getCategory

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event metrics grouped by event category.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Whether subtables should be expanded in the response |
| secondaryDimension | 'eventAction'\|'eventName'\|false | no | false | Optional secondary dimension for subtable rows |
| flat | bool | no | false | Whether subtable rows should be flattened into a single table |

**Returns:** DataTable|DataTable\Map — event category metrics.

### Events.getAction

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event metrics grouped by event action.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Whether subtables should be expanded in the response |
| secondaryDimension | 'eventName'\|'eventCategory'\|false | no | false | Optional secondary dimension for subtable rows |
| flat | bool | no | false | Whether subtable rows should be flattened into a single table |

**Returns:** DataTable|DataTable\Map — event action metrics.

### Events.getName

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event metrics grouped by event name.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Whether subtables should be expanded in the response |
| secondaryDimension | 'eventAction'\|'eventCategory'\|false | no | false | Optional secondary dimension for subtable rows |
| flat | bool | no | false | Whether subtable rows should be flattened into a single table |

**Returns:** DataTable|DataTable\Map — event name metrics.

### Events.getActionFromCategoryId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event actions for one event category row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event category row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event action metrics for the selected category.

### Events.getNameFromCategoryId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event names for one event category row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event category row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event name metrics for the selected category.

### Events.getCategoryFromActionId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event categories for one event action row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event action row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event category metrics for the selected action.

### Events.getNameFromActionId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event names for one event action row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event action row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event name metrics for the selected action.

### Events.getActionFromNameId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event actions for one event name row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event name row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event action metrics for the selected name.

### Events.getCategoryFromNameId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns event categories for one event name row.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the event name row to expand |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map — event category metrics for the selected name.

## Transitions

_Provides API methods for transition reports around a specific page action (previous/following pages, referrers, exits)._

### Transitions.getTransitionsForPageTitle

**Type:** Report getter
**Access:** View access to site (enforced via getTransitionsForAction)
**Description:** Returns transition data for the specified page title.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pageTitle | string | yes | — | The page title to analyze. |
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |
| limitBeforeGrouping | int\|string | no | `0` | Maximum number of transition rows to keep before grouping the remainder. |

**Returns:** array — transition metrics and related referrer/action tables for the page title.

### Transitions.getTransitionsForPageUrl

**Type:** Report getter
**Access:** View access to site (enforced via getTransitionsForAction)
**Description:** Returns transition data for the specified page URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pageUrl | string | yes | — | The page URL to analyze. |
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |
| limitBeforeGrouping | int\|string | no | `0` | Maximum number of transition rows to keep before grouping the remainder. |

**Returns:** array — transition metrics and related referrer/action tables for the page URL.

### Transitions.getTransitionsForAction

**Type:** Report getter
**Access:** View access to site
**Description:** Returns transition data for the specified page action (URL or title), including internal/external referrers and following actions.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| actionName | string | yes | — | The page URL or title to analyze. |
| actionType | string | yes | — | Whether the action name is a `url` or `title`. |
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |
| limitBeforeGrouping | int\|string | no | `0` | Maximum number of transition rows to keep before grouping the remainder. |
| parts | string | no | `'all'` | Comma-separated list of report parts to include, or `all`. |

**Returns:** array — transition metrics and related referrer/action tables for the action.

### Transitions.getTranslations

**Type:** Action
**Access:** None (public)
**Description:** Returns translation strings used by the Transitions UI. _(Marked `@internal`.)_

**Parameters:**

_None._

**Returns:** array of translation strings.

### Transitions.isPeriodAllowed

**Type:** Action
**Access:** None (public)
**Description:** Checks whether a given period/date is allowed for transitions by the site's config settings.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website. |
| period | string | yes | — | The period to check. |
| date | string | yes | — | The date or date range to check. |

**Returns:** bool — whether the period is allowed.

## Insights

_Provides API methods for insights and movers/shakers comparisons between report periods._

### Insights.canGenerateInsights

**Type:** Action
**Access:** Some view access (at least one site)
**Description:** Detects whether insights can be generated for a given date/period combination (i.e. whether a previous comparison period exists).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| date | string | yes | — | The date or date range to process. |
| period | string | yes | — | The period to process (day, week, month, year, range). |

**Returns:** bool — whether insights can be generated.

### Insights.getInsightsOverview

**Type:** Report getter
**Access:** View access to site
**Description:** Generates the insights overview across all reports registered via the `Insights.addReportToOverview` event.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |

**Returns:** DataTable\Map — insight tables for every report in the overview.

### Insights.getMoversAndShakersOverview

**Type:** Report getter
**Access:** View access to site
**Description:** Detects movers and shakers across all reports registered via the `Insights.addReportToOverview` event.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |

**Returns:** DataTable\Map — movers-and-shakers tables for every report in the overview.

### Insights.getMoversAndShakers

**Type:** Report getter
**Access:** View access to site
**Description:** Detects the movers and shakers of a given date/report combination — rows with a higher-than-average impact on the metric.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| reportUniqueId | string | yes | — | Report identifier, e.g. `Actions_getPageUrls`. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |
| comparedToXPeriods | int | no | `1` | Number of past periods to compare against. |
| limitIncreaser | int | no | `4` | Maximum number of positive movers to include (`0` excludes them). |
| limitDecreaser | int | no | `4` | Maximum number of negative movers to include (`0` excludes them). |

**Returns:** DataTable — movers-and-shakers rows for the requested report.

### Insights.getInsights

**Type:** Report getter
**Access:** View access to site
**Description:** Generates insights by comparing a report for a date/period with a previous period, filtering out rows with insufficient growth or impact.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query. |
| period | string | yes | — | The period to process (day, week, month, year, range). |
| date | string | yes | — | The date or date range to process. |
| reportUniqueId | string | yes | — | Report identifier, e.g. `Actions_getPageUrls`. |
| segment | string\|null\|false | no | `false` | Custom segment to filter the report. |
| limitIncreaser | int | no | `5` | Maximum number of positive movers to include (`0` excludes them). |
| limitDecreaser | int | no | `5` | Maximum number of negative movers to include (`0` excludes them). |
| filterBy | string | no | `''` | Optional filter for mover type (`movers`, `new`, `disappeared`). |
| minImpactPercent | int | no | `2` | Minimum impact threshold in percent. |
| minGrowthPercent | int | no | `20` | Minimum growth threshold in percent vs the previous period. |
| comparedToXPeriods | int | no | `1` | Number of past periods to compare against. |
| orderBy | string | no | `'absolute'` | Row ordering mode (`absolute`, `relative`, `importance`). |

**Returns:** DataTable — insight rows for the requested report.

## Goals

_Manage goals (create, update, delete, list) and request goal and ecommerce conversion reports and metrics._

### Goals.getGoal

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a single goal's configuration attributes for a website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| idGoal | int | yes | — | The numeric ID of the goal to query |

**Returns:** Goal attributes array, or `null` if the goal does not exist.

### Goals.getGoals

**Type:** Report getter
**Access:** View access to site
**Description:** Returns all goals for one or more websites.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| orderByName | bool | no | false | Whether to sort the returned goals alphabetically by name |

**Returns:** Goal attributes, indexed by goal ID for single-site requests and a numeric list for multi-site requests.

### Goals.addGoal

**Type:** Action
**Access:** Write access to site
**Description:** Creates a goal for a website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to configure the goal for |
| name | string | yes | — | Goal name |
| matchAttribute | string | yes | — | Attribute used to match conversions (e.g. url, title, file, external_website, manually, event_*) |
| pattern | string | yes | — | Match pattern (URL/title/filename/external website/event value, or numeric threshold; ignored for `manually`) |
| patternType | string | yes | — | Matching operator (`exact`, `contains`, `regex`, `greater_than`, or empty for `manually`) |
| caseSensitive | bool | no | false | Whether string matching is case-sensitive |
| revenue | bool\|float | no | false | Default revenue for conversions; `false`/`0` disables a fixed value |
| allowMultipleConversionsPerVisit | bool | no | false | Whether multiple conversions may be recorded within one visit |
| description | string | no | '' | Optional goal description shown in the Goals UI |
| useEventValueAsRevenue | bool | no | false | Use tracked event value as goal revenue (event-based goals only) |

**Returns:** int — ID of the new goal.

### Goals.updateGoal

**Type:** Action
**Access:** Write access to site
**Description:** Updates an existing goal without reprocessing already recorded conversions.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website the goal belongs to |
| idGoal | int | yes | — | Goal ID to update |
| name | string | yes | — | Goal name |
| matchAttribute | string | yes | — | Attribute used to match conversions |
| pattern | string | yes | — | Match pattern (ignored for `manually`) |
| patternType | string | yes | — | Matching operator (`exact`, `contains`, `regex`, `greater_than`, or empty for `manually`) |
| caseSensitive | bool | no | false | Whether string matching is case-sensitive |
| revenue | bool\|float | no | false | Default revenue for conversions; `false`/`0` disables a fixed value |
| allowMultipleConversionsPerVisit | bool | no | false | Whether multiple conversions may be recorded within one visit |
| description | string | no | '' | Optional goal description shown in the Goals UI |
| useEventValueAsRevenue | bool | no | false | Use tracked event value as goal revenue (event-based goals only) |

**Returns:** void — nothing.

### Goals.deleteGoal

**Type:** Action
**Access:** Write access to site
**Description:** Soft deletes a goal. Archived stats data is still recorded but not displayed.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| idGoal | int | yes | — | The numeric ID of the goal to delete |

**Returns:** void — nothing.

### Goals.getItemsSku

**Type:** Report getter
**Access:** View access to site
**Description:** Returns ecommerce product metrics grouped by product SKU (purchased products, or abandoned-cart items when requested).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| abandonedCarts | bool | no | false | Return abandoned-cart product metrics instead of purchased products |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — ecommerce product metrics grouped by SKU.

### Goals.getItemsName

**Type:** Report getter
**Access:** View access to site
**Description:** Returns ecommerce product metrics grouped by product name.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| abandonedCarts | bool | no | false | Return abandoned-cart product metrics instead of purchased products |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — ecommerce product metrics grouped by name.

### Goals.getItemsCategory

**Type:** Report getter
**Access:** View access to site
**Description:** Returns ecommerce product metrics grouped by product category.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| abandonedCarts | bool | no | false | Return abandoned-cart product metrics instead of purchased products |
| segment | string\|null\|false | no | false | Custom segment to filter the report |

**Returns:** DataTable\|DataTable\Map — ecommerce product metrics grouped by category.

### Goals.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns goal and ecommerce metrics (conversions, visits converted, conversion rate, revenue), including new and returning visitor variants.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idGoal | int\|string\|false | no | false | Goal ID, `ecommerceOrder`, `ecommerceAbandonedCart`, or `false` for all goals |
| columns | string\|string[] | no | [] | Optional metric name(s) to return (e.g. `nb_conversions`, `conversion_rate`, `revenue`) |
| showAllGoalSpecificMetrics | bool | no | false | Include per-goal metric columns when no specific goal is selected |
| compare | bool | no | false | Prepare the table for a comparison report by deferring metric formatting |

**Returns:** DataTable\|DataTable\Map — goal metrics with additional columns for all, new, and returning visits.

### Goals.getMetrics

**Type:** Report getter
**Access:** View access to site
**Description:** Similar to `get()` but without new/returning visitor metrics and applying no default segment. **[DEPRECATED / internal]** — exists only to support the implementation of `get()`.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idGoal | int\|string\|false | no | false | Goal ID, `ecommerceOrder`, `ecommerceAbandonedCart`, or `false` for all goals |
| columns | string\|string[] | no | [] | Optional metric name(s) to return |
| showAllGoalSpecificMetrics | bool | no | false | Show all goal-specific metrics when no goal is set |

**Returns:** DataTable\|DataTable\Map — goal metrics.

### Goals.getDaysToConversion

**Type:** Report getter
**Access:** View access to site
**Description:** Returns conversions grouped by the number of days between first visit and conversion.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idGoal | int\|string\|false | no | false | Goal ID, `ecommerceOrder`, `ecommerceAbandonedCart`, or `false` for all goals |

**Returns:** DataTable\|DataTable\Map — conversion counts grouped by days until conversion.

### Goals.getVisitsUntilConversion

**Type:** Report getter
**Access:** View access to site
**Description:** Returns conversions grouped by the visit count before conversion.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idGoal | int\|string\|false | no | false | Goal ID, `ecommerceOrder`, `ecommerceAbandonedCart`, or `false` for all goals |

**Returns:** DataTable\|DataTable\Map — conversion counts grouped by visits until conversion.

## Referrers

_Access reports about websites, search engines, keywords, social networks, AI assistants, and campaigns used to reach your site._

### Referrers.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the referrer overview report with distinct referrer counts and percentage metrics per referrer type.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| columns | string\|string[]\|false | no | false | Specific columns to include, or false for all |

**Returns:** DataTable of referrer overview rows with summary counts and processed percentage metrics.

### Referrers.getReferrerType

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report describing visit information for each referrer type, whose subtables are the per-type reports (keywords, social networks, AI assistants, websites, campaigns).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| typeReferrer | bool\|int\|string | no | false | Deprecated referrer type filter to restrict rows |
| idSubtable | int\|null | no | null | Referrer type ID to load a subreport directly |
| expanded | bool | no | false | Load subtables eagerly |
| _setReferrerTypeLabel | bool | no | true | Replace referrer type IDs with readable labels |

**Returns:** DataTable|DataTable\Map of rows for each referrer type, or the selected referrer-type subreport.

### Referrers.getAll

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a flattened report containing all referrer subtables merged into one table.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable with subtables merged into the main table.

### Referrers.getKeywords

**Type:** Report getter
**Access:** View access to site
**Description:** Returns search keywords that brought visits to the requested website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load keyword subtables eagerly |
| flat | bool | no | false | Flatten subtables into the main table |

**Returns:** DataTable|DataTable\Map of search keyword rows.

### Referrers.getSearchEnginesFromKeywordId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the search engines associated with a specific keyword subtable.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Keyword subtable ID to expand |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of search engine rows for the selected keyword.

### Referrers.getSearchEngines

**Type:** Report getter
**Access:** View access to site
**Description:** Returns search engines that referred visits to the requested website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load keyword subtables eagerly |
| flat | bool | no | false | Flatten subtables into the main table |

**Returns:** DataTable|DataTable\Map of search engine rows.

### Referrers.getKeywordsFromSearchEngineId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns keywords for a specific search engine subtable.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Search engine subtable ID to expand |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of keyword rows for the selected search engine.

### Referrers.getCampaigns

**Type:** Report getter
**Access:** View access to site
**Description:** Returns campaigns that referred visits to the requested website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load campaign keyword subtables eagerly |

**Returns:** DataTable|DataTable\Map of campaign rows.

### Referrers.getKeywordsFromCampaignId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns campaign keywords for a specific campaign subtable.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | The site ID to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Campaign subtable ID to expand |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of campaign keyword rows for the selected campaign.

### Referrers.getWebsites

**Type:** Report getter
**Access:** View access to site
**Description:** Returns referring websites for the requested website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load URL subtables eagerly |
| flat | bool | no | false | Flatten subtables into the main table |

**Returns:** DataTable|DataTable\Map of referring website rows.

### Referrers.getUrlsFromWebsiteId

**Type:** Report getter
**Access:** View access to site
**Description:** Returns individual referrer URLs for a specific website subtable.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Website subtable ID to expand |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map of referrer URL rows for the selected website.

### Referrers.getSocials

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report comparing visits and related metrics for social network referrers, backfilling missing rows from website referrer data when needed.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load URL subtables eagerly |
| flat | bool | no | false | Flatten subtables into the main table |

**Returns:** DataTable|DataTable\Map of social network referrer rows.

### Referrers.getAIAssistants

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report comparing visits and related metrics for AI assistant referrers, backfilling missing rows from website referrer data when needed.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| expanded | bool | no | false | Load secondary-dimension subtables eagerly |
| flat | bool | no | false | Flatten subtables into the main table |
| secondaryDimension | string\|null | no | null | 'entryPageTitle' or 'entryPageUrl' grouping (default entryPageUrl) |

**Returns:** DataTable|DataTable\Map of AI assistant referrer rows.

### Referrers.getUrlsForSocial

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report of individual referrer URLs for a specific social networking site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| idSubtable | int\|null | no | null | Index into the Socials list; filters URLs by that network (null = all) |

**Returns:** DataTable|DataTable\Map of social referrer URL rows.

### Referrers.getEntryPageUrlsForAIAssistant

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report of individual entry page URLs for a specific AI assistant.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| idSubtable | int\|null | no | null | Index into the AI assistant list; filters URLs by that assistant (null = all) |

**Returns:** DataTable|DataTable\Map of entry page URL rows for the selected AI assistant.

### Referrers.getEntryPageTitlesForAIAssistant

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report of individual entry page names/titles for a specific AI assistant.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| idSubtable | int\|null | no | null | Index into the AI assistant list; filters titles by that assistant (null = all) |

**Returns:** DataTable|DataTable\Map of entry page title rows for the selected AI assistant.

### Referrers.getNumberOfDistinctSearchEngines

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct search engines in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct search engines.

### Referrers.getNumberOfDistinctSocialNetworks

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct social networks in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct social networks.

### Referrers.getNumberOfDistinctKeywords

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct search keywords in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct keywords.

### Referrers.getNumberOfDistinctCampaigns

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct campaigns in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct campaigns.

### Referrers.getNumberOfDistinctWebsites

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct referring websites in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct referring websites.

### Referrers.getNumberOfDistinctAIAssistants

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct AI assistants in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct AI assistants.

### Referrers.getNumberOfDistinctWebsitesUrls

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the number of distinct referrer URLs in the requested period.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-list or "all" |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |

**Returns:** DataTable|DataTable\Map numeric archive result with the count of distinct referrer URLs.

## MultiSites

_Request key metrics (visits, page views, revenue) for all websites in Matomo._

### MultiSites.getAll

**Type:** Report getter
**Access:** Must have view access to at least one site
**Description:** Returns total visits, actions and revenue plus their evolution for all accessible sites over a period; merges the archive so each row is a single site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| _restrictSitesToLogin | string\|null | no | null | Internal: username to restrict visible sites during a scheduled task |
| enhanced | bool | no | false | Include additional goal and ecommerce metrics |
| pattern | string\|null | no | null | Site name or ID pattern to limit matched websites |
| showColumns | string\|string[] | no | [] | Metric columns to include (comma-list or array) |

**Returns:** DataTable|Map of rows per matched site, with evolution metrics when available.

### MultiSites.getOne

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the MultiSites metrics for a single website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to query |
| period | string | yes | — | day, week, month, year or range |
| date | string | yes | — | Date or date range to process |
| segment | string\|null | no | null | Custom segment to filter the report |
| _restrictSitesToLogin | string\|null | no | null | Internal: username to restrict visible sites during a scheduled task |
| enhanced | bool | no | false | Include additional goal and ecommerce metrics |

**Returns:** DataTable|Map of metrics for the requested website.

### MultiSites.getAllWithGroups

**Type:** Report getter
**Access:** Must have view access to at least one site
**Description:** Returns the MultiSites dashboard response (totals, last date, grouped site rows) for the widget UI.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| period | string\|null | no | null | Period type, or null to use the request default |
| date | string\|null | no | null | Date or date range, or null to use the request default |
| segment | string\|null | no | null | Custom segment to filter the report |
| pattern | string | no | '' | Search term to filter listed websites by name |
| filter_limit | int | no | 0 | Maximum number of sites in the grouped response |

**Returns:** array of dashboard totals, last date, and grouped site rows.

## SEO

_Access a list of SEO metrics for a specified URL (e.g. Bing indexed pages, domain age)._

### SEO.getRank

**Type:** Report getter
**Access:** Must have view access to at least one site
**Description:** Returns SEO statistics for a given URL.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| url | string | yes | — | URL to request SEO stats for |

**Returns:** DataTable of SEO metrics for the URL's domain.

## BotTracking

_Provides API methods for bot and AI chatbot reporting._

### BotTracking.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the main bot tracking report.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| columns | string\|string[]\|null | no | null | Optional metric names to include in the report |

**Returns:** DataTable|DataTable\Map — bot tracking metrics for the requested selection and period.

### BotTracking.getAIChatbotRequests

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a report about AI chatbot requests; the subtables contain page or document URLs depending on the secondary dimension.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| expanded | bool | no | false | Whether subtables should be expanded in the response |
| flat | bool | no | false | Whether subtable rows should be flattened into a single table |
| secondaryDimension | 'pages'\|'documents'\|null | no | null | Subtable dimension: `pages` for page URLs or `documents` for document URLs |

**Returns:** DataTable|DataTable\Map — requests per AI chatbot for the selected secondary dimension.

### BotTracking.getPageUrlsForAIChatbot

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URLs requested by a specific AI chatbot.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the AI chatbot row to expand |

**Returns:** DataTable|DataTable\Map — page URLs requested by the selected AI chatbot.

### BotTracking.getDocumentUrlsForAIChatbot

**Type:** Report getter
**Access:** View access to site
**Description:** Returns document URLs requested by a specific AI chatbot.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| idSubtable | int | yes | — | Subtable ID for the AI chatbot row to expand |

**Returns:** DataTable|DataTable\Map — document URLs requested by the selected AI chatbot.

### BotTracking.getAIChatbotContentPages

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URLs accessed by AI chatbots across all chatbots, with server time and response size metrics.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |

**Returns:** DataTable|DataTable\Map — flat table of page URLs with Requests, Avg. Server Time, and Avg. Response Size.

### BotTracking.getAIChatbotContentDocuments

**Type:** Report getter
**Access:** View access to site
**Description:** Returns document URLs accessed by AI chatbots across all chatbots, with server time and response size metrics.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |

**Returns:** DataTable|DataTable\Map — flat table of document URLs with Requests, Avg. Server Time, and Avg. Response Size.

### BotTracking.getAIChatbotBrokenContent

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page and document URLs accessed by AI chatbots that returned HTTP errors (4xx/5xx).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |

**Returns:** DataTable|DataTable\Map — flat table of broken URLs with 5XX Requests and Page Not Found (404) Requests counts.

### BotTracking.getAIChatbotHumanFavouredPages

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URLs visited far more by humans than requested by AI chatbots, with a bounded 0–100 Human-Favoured Discrepancy Score. Segmentation is not supported (any `segment` is ignored).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |

**Returns:** DataTable|DataTable\Map — flat table of URLs with Unique Human Pageviews, AI Chatbot Requests, and the score.

### BotTracking.getAIChatbotAIFavouredPages

**Type:** Report getter
**Access:** View access to site
**Description:** Returns page URLs requested far more by AI chatbots than visited by humans, with a bounded 0–100 AI-Favoured Discrepancy Score. Segmentation is not supported (any `segment` is ignored).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |

**Returns:** DataTable|DataTable\Map — flat table of URLs with Unique Human Pageviews, AI Chatbot Requests, and the score.

## AIAgents

_Provides reporting API methods for distinguishing AI agent traffic from human traffic._

### AIAgents.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns visit summary metrics split between AI agents and human visitors, with AI-agent and human-specific column suffixes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): single ID, array, comma-separated list, or "all" |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string | no | '' (empty) | Custom segment appended to the AI-agent and human traffic filters |
| columns | list<string>\|string | no | '' (empty) | Metrics to include; comma-separated list or array |

**Returns:** DataTable\|DataTable\Map — visit summary metrics with `_ai_agent` and `_human` column suffixes.

## CustomDimensions

_Manage and access reports for configured Custom Dimensions._

### CustomDimensions.getCustomDimension

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the report for a configured custom dimension. Only reports for active dimensions can be fetched.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idDimension | int | yes | — | Custom dimension ID to load the report for |
| idSite | int | yes | — | The numeric ID of the website to query |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| expanded | bool | no | false | Whether subtables should be expanded in the response |
| flat | bool | no | false | Whether subtable rows should be flattened into a single table |
| idSubtable | int\|false | no | false | Optional subtable ID to load |

**Returns:** DataTable|DataTable\Map with the custom dimension report.

### CustomDimensions.configureNewCustomDimension

**Type:** Action
**Access:** Write access to site
**Description:** Configures a new custom dimension for a site. Custom dimensions cannot be deleted, so slots should be used carefully.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to configure the dimension for |
| name | string | yes | — | The custom dimension name |
| scope | string | yes | — | The dimension scope ('visit' or 'action') |
| active | bool\|int | yes | — | Whether the custom dimension should be active |
| extractions | array | no | [] | Optional extraction rules (action scope only) |
| caseSensitive | bool\|int | no | true | Whether extraction matching should be case-sensitive |
| description | string | no | '' | Optional description for the custom dimension |

**Returns:** int — ID of the configured custom dimension (may be reused across websites).

### CustomDimensions.configureExistingCustomDimension

**Type:** Action
**Access:** Write access to site
**Description:** Updates an existing custom dimension. Updates all values, so existing values must be passed for anything that should not be reset.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idDimension | int | yes | — | Custom dimension ID to update |
| idSite | int | yes | — | The numeric ID of the website the dimension belongs to |
| name | string | yes | — | The custom dimension name |
| active | bool\|int | yes | — | Whether the custom dimension should be active |
| extractions | array | no | [] | Optional extraction rules (action scope only) |
| caseSensitive | bool\|int\|null | no | null | Case-sensitivity of matching; null keeps current setting |
| description | string\|null | no | null | Optional description; null keeps current description |

**Returns:** void (no return value).

### CustomDimensions.getConfiguredCustomDimensions

**Type:** Report getter
**Access:** View access to site
**Description:** Returns all configured custom dimensions for a site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |

**Returns:** array of configured custom dimensions (each a map of attributes).

### CustomDimensions.getConfiguredCustomDimensionsHavingScope

**Type:** Report getter
**Access:** View access to site
**Description:** Convenience method returning configured custom dimensions filtered by scope. Marked `@hide` (hidden to reduce API surface area).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| scope | string | yes | — | Scope to filter configured dimensions by |

**Returns:** array of configured custom dimensions matching the given scope.

### CustomDimensions.getAvailableScopes

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the supported custom-dimension scopes for a site, including how many slots are available, used, and remaining.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |

**Returns:** array of scopes with value, name, numSlotsAvailable, numSlotsUsed, numSlotsLeft, and supportsExtractions.

### CustomDimensions.getAvailableExtractionDimensions

**Type:** Report getter
**Access:** Write access to at least one site (checkUserHasSomeWriteAccess)
**Description:** Returns the dimensions that can be used in extraction rules.

**Parameters:**
_None._

**Returns:** array of extraction dimensions with value and name.

## SegmentEditor

_Lets you add, update, delete, star/unstar, and list saved custom segments, and fetch summary visit data for a pre-processed segment._

### SegmentEditor.isUserCanAddNewSegment

**Type:** Action
**Access:** None (public) — returns `false` for anonymous users
**Description:** Returns whether the current user can create a new stored segment for a given site (or an all-websites segment when no site is given).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|null | yes | — | Site to check permissions for; when empty, checks all-websites segment creation (super user only). |

**Returns:** `true` if the current user can add a segment for the requested scope (bool).

### SegmentEditor.delete

**Type:** Action
**Access:** Segment owner or super user (must be non-anonymous; requires some view access)
**Description:** Deletes a stored segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSegment | int | yes | — | ID of the stored segment to delete. |

**Returns:** void.

### SegmentEditor.update

**Type:** Action
**Access:** Segment owner or super user (view access to the segment's site; enabling for all users / all sites requires super user)
**Description:** Modifies an existing stored segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSegment | int | yes | — | ID of the stored segment to modify. |
| name | string | yes | — | New name of the segment. |
| definition | string | yes | — | New definition of the segment. |
| idSite | int\|null | no | null | If supplied, associates the segment with a single site. |
| autoArchive | bool | no | false | Whether to automatically archive data with the segment. |
| enabledAllUsers | bool | no | false | Whether the segment is viewable by all users or only its creator. |

**Returns:** void.

### SegmentEditor.add

**Type:** Action
**Access:** View access to the site (all-websites segment requires super user); user must be allowed to add segments
**Description:** Adds a new stored segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| name | string | yes | — | Name of the new segment. |
| definition | string | yes | — | Definition of the new segment. |
| idSite | int\|null | no | null | If supplied, associates the segment with a single site. |
| autoArchive | bool | no | false | Whether to automatically archive data with the segment. |
| enabledAllUsers | bool | no | false | Whether the segment is viewable by all users or only its creator. |

**Returns:** The newly created segment ID (int).

### SegmentEditor.star

**Type:** Action
**Access:** Segment owner or super user (non-anonymous)
**Description:** Stars a stored segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSegment | int | yes | — | ID of the stored segment to star. |

**Returns:** `array{result: bool, starred: 1, starred_by: string}` with the update result and new starred state.

### SegmentEditor.unstar

**Type:** Action
**Access:** Segment owner or super user (non-anonymous)
**Description:** Unstars a stored segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSegment | int | yes | — | ID of the stored segment to unstar. |

**Returns:** `array{result: bool, starred: 0}` with the update result and new starred state.

### SegmentEditor.get

**Type:** Action
**Access:** Some view access; the segment must be visible to the user (view access to its site, and owner/super user for non-shared segments)
**Description:** Returns a stored segment by ID.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSegment | int | yes | — | ID of the stored segment to fetch. |

**Returns:** The stored segment, or `null` if it does not exist.

### SegmentEditor.getAll

**Type:** Action
**Access:** View access to site (some view access when no site given)
**Description:** Returns all stored segments visible to the current user, optionally scoped to one site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|null | no | null | If supplied, returns stored segments for one site only; otherwise all visible segments. |

**Returns:** List of stored segments visible to the current user.

### SegmentEditor.getSegmentData

**Type:** Report getter
**Access:** View access to site (enforced downstream via VisitsSummary API)
**Description:** Returns visit and action totals for a pre-processed segment together with visit evolution vs. the previous period. Throws if the segment is a real-time (non pre-processed) segment.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to query. |
| period | string | yes | — | Period to process: `day`, `week`, `month`, `year`, or `range`. |
| date | string | yes | — | Date or date range (`YYYY-MM-DD`, magic keywords, or ranges). |
| segment | string | yes | — | Custom segment definition to filter the report. |

**Returns:** `array{nb_visits, nb_actions, evolution_visits_direction, evolution_visits_icon, evolution_visits}` — visit/action totals and visit evolution metadata.

## Annotations

_Provides API methods to create, update, delete, and query annotations._

### Annotations.add

**Type:** Action
**Access:** View access to site and non-anonymous (checkUserCanAddNotesFor)
**Description:** Creates a new annotation for a site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The site ID to add the annotation to |
| date | string | yes | — | The date the annotation is attached to |
| note | string | yes | — | The text of the annotation (max 255 chars) |
| starred | bool | no | false | Whether the annotation should be starred |

**Returns:** array (Annotation) — the created annotation.

### Annotations.save

**Type:** Action
**Access:** Admin access to site, or the note creator with view access (non-anonymous)
**Description:** Updates an annotation for a site and returns the updated annotation; null date/note/starred values leave those fields unchanged.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The site ID the annotation belongs to |
| idNote | int | yes | — | The ID of the note |
| date | string\|null | no | null | New date; if null, date is not modified |
| note | string\|null | no | null | New text (max 255 chars); if null, text is not modified |
| starred | bool\|null | no | null | Whether to star; if null, starred state is unchanged |

**Returns:** array (Annotation) — the updated annotation.

### Annotations.delete

**Type:** Action
**Access:** Admin access to site, or the note creator with view access (non-anonymous)
**Description:** Removes an annotation from a site's list of annotations.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The site ID the annotation belongs to |
| idNote | int | yes | — | The ID of the note to delete |

**Returns:** void.

### Annotations.deleteAll

**Type:** Action
**Access:** Super user
**Description:** Removes all annotations for a single site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The ID of the site to remove annotations for |

**Returns:** void.

### Annotations.get

**Type:** Report getter
**Access:** View access to site
**Description:** Returns a single annotation for one site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The site ID the annotation is linked to |
| idNote | int | yes | — | The ID of the annotation to get |

**Returns:** array (Annotation) — the requested annotation.

### Annotations.getAll

**Type:** Report getter
**Access:** View access to site
**Description:** Returns every annotation for one or more sites within a date range derived from date, period, and optional number of past periods.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | string | yes | — | One site ID or a comma-separated list of site IDs |
| date | string\|null | no | null | The date of the period |
| period | string | no | 'day' | The period type (day, week, month, year, range) |
| lastN | int\|null | no | null | Include the last N periods in the date range |

**Returns:** array<int, array<int, Annotation>> — annotations keyed by site ID.

### Annotations.getAnnotationCountForDates

**Type:** Report getter
**Access:** View access to site
**Description:** Returns the count of annotations (including starred count) for a list of periods.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | string | yes | — | The site ID(s) to get the annotation count for |
| date | string | yes | — | The date of the period |
| period | string | yes | — | The period type (day, week, month, year, range) |
| lastN | int\|null | no | null | Get counts for the last N periods |
| getAnnotationText | bool | no | false | Include the note text when exactly one annotation exists for a date |

**Returns:** array — per-site, per-period count/starred (and optional note) structures.

## ImageGraph

_Generates static PNG graph images (line, bar, pie) for any existing Matomo report._

### ImageGraph.get

**Type:** Report getter
**Access:** View access to site
**Description:** Generates a static graph image (evolution line, vertical/horizontal bar, pie or 3D pie) for a given Matomo report. By default renders the PNG inline to the browser (binary image output); can also be saved to disk or returned as a raw PHP graph object.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | The numeric ID of the website to query |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range, or magic keywords (today, yesterday, lastWeek, etc.) |
| apiModule | string | yes | — | API module name of the source report |
| apiAction | string | yes | — | API method name of the source report |
| graphType | 'evolution'\|'verticalBar'\|'horizontalBar'\|'pie'\|'3dPie'\|false | no | false | Graph type; auto-selected if not given |
| outputType | int | no | API::GRAPH_OUTPUT_INLINE (0) | Output mode: 0 inline image, 1 saved file, 2 raw PHP graph object |
| columns | string\|false | no | false | Comma-separated metric names to plot |
| labels | string\|false | no | false | Comma-separated row labels to include for evolution graphs |
| showLegend | bool | no | true | Whether the graph legend should be displayed |
| width | int\|false | no | false | Graph width in pixels |
| height | int\|false | no | false | Graph height in pixels |
| fontSize | int | no | API::DEFAULT_FONT_SIZE (9) | Base font size used in the graph |
| legendFontSize | int\|false | no | false | Legend font size |
| aliasedGraph | bool | no | true | Whether anti-aliasing should be enabled |
| idGoal | int\|string\|false | no | false | Goal ID for report methods that support goals |
| colors | string\|false | no | false | Comma-separated hex colors to use in the graph |
| textColor | string | no | API::DEFAULT_TEXT_COLOR (222222) | Hex color used for text |
| backgroundColor | string | no | API::DEFAULT_BACKGROUND_COLOR (FFFFFF) | Hex color used for background |
| gridColor | string | no | API::DEFAULT_GRID_COLOR (CCCCCC) | Hex color used for grid lines |
| idSubtable | int\|false | no | false | Subtable ID for source reports that use subtables |
| legendAppendMetric | bool | no | true | Whether the metric name is appended to legend labels |
| segment | string\|null\|false | no | false | Custom segment to filter the report |
| idDimension | int\|string\|false | no | false | Dimension ID for reports that support dimensions |

**Returns:** Generated graph output depending on outputType — inline PNG image sent to the browser (binary, then exits), a saved file path, or a raw rendered PHP graph object.

## ScheduledReports

_Manage scheduled email reports and generate, download, or email any existing report._

### ScheduledReports.addReport

**Type:** Action
**Access:** View access to site (must be logged in / non-anonymous)
**Description:** Creates and schedules a new report.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to report on. |
| description | string | yes | — | Report title shown in UI and filenames (truncated to 250 chars). |
| period | string | yes | — | Delivery schedule: day, week, month, or never. |
| hour | int | yes | — | Hour of day (0–23) when the report is sent. |
| reportType | string | yes | — | Transport medium identifier, e.g. 'email'. |
| reportFormat | string | yes | — | Output format identifier, e.g. 'pdf' or 'html'. |
| reports | list<string> | yes | — | Report unique IDs to include (e.g. ['VisitsSummary_get']). |
| parameters | array | yes | — | Transport-specific parameters (e.g. emailMe, additionalEmails). |
| idSegment | int\|false | no | false | Saved segment ID to apply, or false for none. |
| evolutionPeriodFor | string | no | 'prev' | Evolution graphs compare previous periods ('prev') or each day ('each'). |
| evolutionPeriodN | int\|null | no | null | Number of previous periods when 'prev'; defaults to configured value. |
| periodParam | string\|null | no | null | Data period generated on each send; defaults to delivery period. |

**Returns:** int — the newly created scheduled report ID.

### ScheduledReports.updateReport

**Type:** Action
**Access:** View access to site (must be logged in / non-anonymous)
**Description:** Updates an existing scheduled report.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idReport | int | yes | — | Scheduled report ID to update. |
| idSite | int | yes | — | Numeric ID of the website the report belongs to. |
| description | string | yes | — | Report title shown in UI and filenames (truncated to 250 chars). |
| period | string | yes | — | Delivery schedule: day, week, month, or never. |
| hour | int | yes | — | Hour of day (0–23) when the report is sent. |
| reportType | string | yes | — | Transport medium identifier, e.g. 'email'. |
| reportFormat | string | yes | — | Output format identifier, e.g. 'pdf' or 'html'. |
| reports | list<string> | yes | — | Report unique IDs to include. |
| parameters | array | yes | — | Transport-specific parameters. |
| idSegment | int\|false | no | false | Saved segment ID to apply, or false for none. |
| evolutionPeriodFor | string | no | 'prev' | 'prev' (previous periods) or 'each' (each day). |
| evolutionPeriodN | int\|null | no | null | Number of previous periods when 'prev'. |
| periodParam | string\|null | no | null | Data period generated on each send. |

**Returns:** void.

### ScheduledReports.deleteReport

**Type:** Action
**Access:** Super user or the report owner (checkUserHasSuperUserAccessOrIsTheUser)
**Description:** Marks a scheduled report as deleted; the row is retained in the database with deleted = 1.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idReport | int | yes | — | Scheduled report ID to delete. |

**Returns:** void.

### ScheduledReports.getWidgetReportMap

**Type:** Report getter
**Access:** View access to site (marked @internal)
**Description:** Builds the report selection payload for a dashboard export, mapping dashboard widgets to their corresponding scheduled report IDs.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| dashId | int | yes | — | Dashboard ID to inspect. |
| idSite | int | yes | — | Website ID the dashboard is exported for. |
| segment | string | no | '' | Custom segment definition to resolve against saved segments. |

**Returns:** array{dashboardName: string, email: map of report unique IDs => true, idSegment: int|null, unmappedWidgets: string[]}.

### ScheduledReports.getReports

**Type:** Report getter
**Access:** View access to at least one site (checkUserHasSomeViewAccess); view access to idSite when supplied
**Description:** Returns scheduled reports matching the supplied filters; all filters are optional and passing false disables that filter.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|false | no | false | Filter to a specific website. |
| period | string\|false | no | false | Filter by delivery schedule (day/week/month/never). |
| idReport | int\|false | no | false | Return a single report; throws if not found. |
| ifSuperUserReturnOnlySuperUserReports | bool | no | false | When true, super users only get their own reports. |
| idSegment | int\|false | no | false | Filter to a specific saved segment. |

**Returns:** array of matching scheduled reports (ordered by description, with decoded parameters and reports fields).

### ScheduledReports.generateReport

**Type:** Action
**Access:** Must be logged in (non-anonymous); view access to the report's site
**Description:** Generates a scheduled report for the given date in the requested output mode (download, save to disk, inline, or return).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idReport | int | yes | — | Scheduled report ID to generate. |
| date | string | yes | — | Date or date range (YYYY-MM-DD, magic keywords, or range). |
| language | string\|false | no | false | ISO language code, or false for default. |
| outputType | int\|false | no | false | Output mode: OUTPUT_DOWNLOAD, OUTPUT_SAVE_ON_DISK, OUTPUT_INLINE, OUTPUT_RETURN. Defaults to download. |
| period | string\|false | no | false | Data period, or false to use the stored period. |
| reportFormat | string\|false | no | false | Output format, or false to use the stored format. |
| parameters | array\|false | no | false | Transport params override, or false for stored params. |

**Returns:** 5-element array [outputFilename, prettyDate, reportSubject, reportTitle, additionalFiles] for OUTPUT_SAVE_ON_DISK; rendered string for OUTPUT_RETURN; void when streaming to the browser.

### ScheduledReports.sendReport

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Sends a scheduled report immediately: generates it, saves to a temp file, dispatches via the configured transport, and cleans up.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idReport | int | yes | — | Scheduled report ID to send. |
| period | string\|false | no | false | Data period, or false to use the stored period. |
| date | string\|false | no | false | Date to generate for, or false for the previous scheduled period. |
| force | bool | no | false | Send even if already sent for the same period. |

**Returns:** void.

## MobileMessaging

_Manage SMS credentials, phone number verification, and SMS account settings._

### MobileMessaging.areSMSAPICredentialProvided

**Type:** Report getter
**Access:** View access to at least one site
**Description:** Checks whether SMS API credentials are configured for the current user.

_None._

**Returns:** bool — true if SMS API credentials are available for the current user.

### MobileMessaging.getSMSProvider

**Type:** Report getter
**Access:** Super user, or logged-in user when delegated management is enabled
**Description:** Returns the configured SMS provider for the current user.

_None._

**Returns:** string|null — the configured SMS provider identifier, or null if none configured.

### MobileMessaging.setSMSAPICredential

**Type:** Action
**Access:** Super user, or logged-in user when delegated management is enabled
**Description:** Stores the SMS API credentials for the selected provider.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| provider | string | yes | — | SMS provider identifier to configure. |
| credentials | array | no | [] | Provider credentials such as an API key or username. |

**Returns:** void.

### MobileMessaging.addPhoneNumber

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Adds a phone number for the current user and sends a verification code to it.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| phoneNumber | string | yes | — | Phone number in international (E.164) format. |

**Returns:** void.

### MobileMessaging.resendVerificationCode

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Requests a new verification code for a pending phone number.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| phoneNumber | string | yes | — | Phone number in international format. |

**Returns:** void.

### MobileMessaging.getCreditLeft

**Type:** Report getter
**Access:** Super user, or logged-in user when delegated management is enabled
**Description:** Returns the remaining SMS credit for the configured provider account.

_None._

**Returns:** int|string — remaining SMS credit reported by the configured provider.

### MobileMessaging.getPhoneNumbers

**Type:** Report getter
**Access:** Must be logged in (non-anonymous)
**Description:** Returns the phone numbers configured for the current user.

_None._

**Returns:** array — phone numbers keyed by phone number, including verification metadata.

### MobileMessaging.removePhoneNumber

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Removes a phone number from the current user account.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| phoneNumber | string | yes | — | Phone number in international format. |

**Returns:** void (fires the MobileMessaging.deletePhoneNumber event).

### MobileMessaging.validatePhoneNumber

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Verifies a phone number using the submitted verification code.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| phoneNumber | string | yes | — | Phone number in international format. |
| verificationCode | string | yes | — | Verification code received by SMS. |

**Returns:** bool — true if the phone number was verified successfully, false otherwise.

### MobileMessaging.deleteSMSAPICredential

**Type:** Action
**Access:** Super user, or logged-in user when delegated management is enabled
**Description:** Deletes the configured SMS API credentials.

_None._

**Returns:** void.

### MobileMessaging.setDelegatedManagement

**Type:** Action
**Access:** Super user
**Description:** Configures whether regular users can manage their own SMS API credentials.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| delegatedManagement | bool | yes | — | true to let regular users manage their own credentials; false to restrict to super users. |

**Returns:** void.

### MobileMessaging.getDelegatedManagement

**Type:** Report getter
**Access:** View access to at least one site
**Description:** Returns whether regular users can manage their own SMS API credentials.

_None._

**Returns:** bool — true if regular users can manage their own credentials, false if only super users can.

## SitesManager

_Gives full control over websites in Matomo (create, update, delete) and many methods to retrieve websites by various attributes, plus global tracking/exclusion settings, timezone and currency lists._

### SitesManager.getJavascriptTag

**Type:** Action
**Access:** View access to site
**Description:** Returns the JavaScript tracking tag for the given website, ready to be embedded on every page to be tracked.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |
| piwikUrl | string | no | '' | Domain/URL path to the Matomo install (defaults to current URL) |
| mergeSubdomains | bool | no | false | Track visitors across all subdomains |
| groupPageTitlesByDomain | bool | no | false | Prepend site domain to page title |
| mergeAliasUrls | bool | no | false | Treat alias URLs as same website for outlinks |
| visitorCustomVariables | array | no | [] | Visitor-scope custom variables |
| pageCustomVariables | array | no | [] | Page-scope custom variables |
| customCampaignNameQueryParam | string | no | '' | Custom campaign name query param |
| customCampaignKeywordParam | string | no | '' | Custom campaign keyword query param |
| doNotTrack | bool | no | false | Respect browser Do-Not-Track |
| disableCookies | bool | no | false | Disable first-party cookies |
| trackNoScript | bool | no | false | Include `<noscript>` fallback |
| crossDomain | bool | no | false | Enable cross-domain linking |
| forceMatomoEndpoint | bool | no | false | Force Matomo endpoint (pre-3.7.0 installs) |
| excludedQueryParams | string\|string[] | no | '' | Query params to exclude from URLs |
| excludedReferrers | string\|string[] | no | '' | Referrer hosts/URLs to ignore |
| disableCampaignParameters | bool | no | false | Prevent campaign params being sent |

**Returns:** String — the JavaScript tag to include in HTML pages.

### SitesManager.getImageTrackingCode

**Type:** Action
**Access:** None (public)
**Description:** Returns HTML-encoded image (`<img>`) link tracking code for a given site, optionally with an action name and goal conversion.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Site ID to generate tracking code for |
| piwikUrl | string | no | '' | Domain/URL path to the Matomo install |
| actionName | string\|false | no | false | Action name to include, or false to omit |
| idGoal | int\|false | no | false | Goal ID to trigger a conversion, or false |
| revenue | int\|float\|false | no | false | Revenue for the goal conversion |
| forceMatomoEndpoint | bool | no | false | Force Matomo endpoint (pre-3.7.0 installs) |

**Returns:** String — the HTML-encoded image tracking code.

### SitesManager.getSitesFromGroup

**Type:** Action
**Access:** Super user
**Description:** Returns all websites belonging to the specified group.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| group | string | no | '' | Group name (empty string returns ungrouped sites) |

**Returns:** Array of site objects belonging to the group.

### SitesManager.getSitesGroups

**Type:** Action
**Access:** Super user
**Description:** Returns the list of website groups, including the empty group if some websites have none.

**Parameters:** _None._

**Returns:** List of distinct group name strings.

### SitesManager.getSiteFromId

**Type:** Action
**Access:** View access to site
**Description:** Returns the website information for a single site (name, main_url, timezone, currency, etc.).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |

**Returns:** Site data array.

### SitesManager.getSiteUrlsFromId

**Type:** Action
**Access:** View access to site
**Description:** Returns the list of all URLs registered for the website (main_url plus alias URLs).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |

**Returns:** List of URL strings, main URL first.

### SitesManager.getAllSites

**Type:** Action
**Access:** Super user
**Description:** Returns all websites, indexed by idsite.

**Parameters:** _None._

**Returns:** Array of site objects keyed by idsite.

### SitesManager.getAllSitesId

**Type:** Action
**Access:** Super user
**Description:** Returns the list of all registered website IDs.

**Parameters:** _None._

**Returns:** List of integer website IDs.

### SitesManager.getSitesWithAdminAccess

**Type:** Action
**Access:** None (public) — results limited to sites the current user has admin access to (all sites for Superuser)
**Description:** Returns the list of websites the current user has 'admin' access to.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| fetchAliasUrls | bool | no | false | Include alias_urls key per site |
| pattern | string\|false | no | false | Optional name/URL pattern filter |
| limit | int\|false | no | false | Max sites to return |
| sitesToExclude | int[] | no | [] | Site IDs to exclude |

**Returns:** List of site objects.

### SitesManager.getSitesWithMinimumAccess

**Type:** Action
**Access:** None (public) — results limited to sites where the current user has at least the given access level
**Description:** Returns websites where the current user has at least the provided access level (view/write/admin).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| permission | string | yes | — | One of 'view', 'write' or 'admin' |
| pattern | string\|null | no | null | Optional name/URL pattern filter |
| limit | int\|null | no | null | Max sites to return |
| sitesToExclude | array | no | [] | Site IDs to exclude |
| siteTypesToExclude | array | no | [] | Site types (e.g. 'website', 'mobileapp') to exclude |

**Returns:** List of site objects.

### SitesManager.getMessagesToWarnOnSiteRemoval

**Type:** Action
**Access:** Super user
**Description:** Returns warning messages to display before deleting a site. (Marked `@internal`.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to inspect |

**Returns:** List of warning message strings.

### SitesManager.getSitesWithViewAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's view-access sites (empty for Superuser)
**Description:** Returns the list of websites with 'view' access for the current user.

**Parameters:** _None._

**Returns:** List of site objects.

### SitesManager.getSitesWithAtLeastViewAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's accessible sites (all for Superuser)
**Description:** Returns the list of websites with 'view' or 'admin' access for the current user.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| limit | int\|false | no | false | Max sites to return |
| _restrictSitesToLogin | string\|false | no | false | Internal: restrict sites to a login during scheduled tasks |

**Returns:** List of site objects.

### SitesManager.getSitesIdWithAdminAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's admin-access sites
**Description:** Returns the list of website IDs with 'admin' access for the current user (all IDs for Superuser).

**Parameters:** _None._

**Returns:** List of integer website IDs.

### SitesManager.getSitesIdWithViewAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's view-access sites (empty for Superuser)
**Description:** Returns the list of website IDs with 'view' access for the current user.

**Parameters:** _None._

**Returns:** List of integer website IDs.

### SitesManager.getSitesIdWithWriteAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's write-access sites (empty for Superuser)
**Description:** Returns the list of website IDs with 'write' access for the current user.

**Parameters:** _None._

**Returns:** List of integer website IDs.

### SitesManager.getSitesIdWithAtLeastViewAccess

**Type:** Action
**Access:** None (public) — results limited to the current user's accessible sites (all for Superuser)
**Description:** Returns the list of website IDs with 'view' or 'admin' access for the current user.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| _restrictSitesToLogin | string\|false | no | false | Internal: restrict sites to a login during scheduled tasks |

**Returns:** List of integer website IDs.

### SitesManager.getSitesIdFromSiteUrl

**Type:** Action
**Access:** None (public) — results limited to sites the current user can access (all for Superuser)
**Description:** Returns website IDs associated with a URL, matching main and alias URLs across HTTP/HTTPS and www/non-www variants.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| url | string | yes | — | The URL to search for |

**Returns:** List of matching `{idsite}` entries.

### SitesManager.addSite

**Type:** Action
**Access:** Super user
**Description:** Adds a new website defined by a name and an array of URLs (first is main_url, rest are aliases), with optional tracking/config settings.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| siteName | string | yes | — | Site name |
| urls | string[]\|string\|null | no | null | Main URL plus alias URLs |
| ecommerce | int\|null | no | null | Ecommerce enabled (1) / disabled (0) |
| siteSearch | int\|null | no | null | Site Search enabled (1) / disabled (0) |
| searchKeywordParameters | string\|null | no | null | Comma-separated search keyword params |
| searchCategoryParameters | string\|null | no | null | Comma-separated search category params |
| excludedIps | string\|null | no | null | Comma-separated IPs to exclude (wildcards allowed) |
| excludedQueryParameters | string\|null | no | null | Comma-separated URL query params to strip |
| timezone | string\|null | no | null | Timezone (defaults to global default) |
| currency | string\|null | no | null | Currency code (defaults to global default) |
| group | string\|null | no | null | Website group (requires Superuser) |
| startDate | string\|null | no | null | Statistics start date YYYY-MM-DD (defaults to today) |
| excludedUserAgents | string\|null | no | null | Comma-separated user-agent substrings to exclude |
| keepURLFragments | int\|null | no | null | 1 keep, 2 remove, 0 use global default |
| type | string\|null | no | null | Website type (defaults to 'website') |
| settingValues | array\|null | no | null | Measurable settings keyed by plugin |
| excludeUnknownUrls | bool\|null | no | null | Track only URLs matching registered URLs |
| excludedReferrers | string\|null | no | null | Comma-separated hosts/URLs to exclude from referrers |
| description | string\|null | no | null | Optional site description |

**Returns:** Integer ID of the newly created website.

### SitesManager.getSiteSettings

**Type:** Action
**Access:** Admin access to site
**Description:** Returns the editable measurable settings metadata for a website, grouped by plugin.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |

**Returns:** List of formatted measurable-setting groups.

### SitesManager.deleteSite

**Type:** Action
**Access:** Super user
**Description:** Deletes a website (and its config such as goals/segments) but not its logs or archives; the last remaining site cannot be deleted.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to delete |
| passwordConfirmation | string\|null | no | null | Current user's password (required with session token) |

**Returns:** Void (no return value).

### SitesManager.addSiteAliasUrls

**Type:** Action
**Access:** Admin access to site
**Description:** Adds alias URLs to a website without duplicating existing ones; the main_url is unaffected.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |
| urls | string[]\|string | yes | — | Alias URLs to add |

**Returns:** Integer count of newly inserted URLs.

### SitesManager.setSiteAliasUrls

**Type:** Action
**Access:** Admin access to site
**Description:** Overwrites the website's list of alias URLs with the provided list; the main_url is unaffected.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |
| urls | string[] | no | [] | Alias URLs to persist |

**Returns:** Integer count of newly inserted URLs.

### SitesManager.getIpsForRange

**Type:** Action
**Access:** None (public)
**Description:** Returns the start and end IP addresses of a given IP range.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| ipRange | string | yes | — | IP range in presentation format, e.g. '192.168.1.0/24' |

**Returns:** Array `[lowIp, highIp]`, or false on error.

### SitesManager.setGlobalExcludedIps

**Type:** Action
**Access:** Super user
**Description:** Sets the IPs (wildcards allowed) to be excluded from tracking on all websites, including future ones.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| excludedIps | string | yes | — | Comma-separated list of IPs to exclude |

**Returns:** Boolean — always true.

### SitesManager.setGlobalSearchParameters

**Type:** Action
**Access:** Super user
**Description:** Sets the global Site Search keyword and category parameter names, used when sites do not define their own.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| searchKeywordParameters | string | yes | — | Comma-separated keyword parameter names |
| searchCategoryParameters | string | yes | — | Comma-separated category parameter names |

**Returns:** Boolean — always true.

### SitesManager.getSearchKeywordParametersGlobal

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the global site-search keyword parameter names, falling back to the built-in defaults.

**Parameters:** _None._

**Returns:** Comma-separated string of keyword parameter names.

### SitesManager.getSearchCategoryParametersGlobal

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the global site-search category parameter names.

**Parameters:** _None._

**Returns:** Comma-separated string, or false if not configured.

### SitesManager.getExcludedQueryParameters

**Type:** Action
**Access:** View access to site (checked via getSiteFromId)
**Description:** Returns the URL query parameters excluded for the given website, including globally excluded parameters.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |

**Returns:** Array of excluded query parameter names.

### SitesManager.getExcludedQueryParametersGlobal

**Type:** Action
**Access:** Some view access (checkUserHasSomeViewAccess)
**Description:** Returns the URL query parameters excluded from all websites, based on the current exclusion type.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|null | no | null | Optional site ID for site-specific filtering |

**Returns:** Comma-separated string of URL parameters.

### SitesManager.getExcludedUserAgentsGlobal

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the user-agent substrings used to exclude visits across all websites.

**Parameters:** _None._

**Returns:** Comma-separated string, or false if not configured.

### SitesManager.setGlobalExcludedUserAgents

**Type:** Action
**Access:** Super user
**Description:** Sets the list of user-agent substrings used to exclude visits across all websites.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| excludedUserAgents | string | yes | — | Comma-separated list of substrings |

**Returns:** Void (no return value).

### SitesManager.getExcludedReferrers

**Type:** Action
**Access:** View access to site
**Description:** Returns the URLs/hosts ignored when detecting referrers for the given site (site-specific plus global).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website |

**Returns:** List of excluded referrer URLs/hosts.

### SitesManager.getExcludedReferrersGlobal

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the global list of URLs/hosts ignored when detecting referrers.

**Parameters:** _None._

**Returns:** Comma-separated string of excluded referrer URLs/hosts.

### SitesManager.setGlobalExcludedReferrers

**Type:** Action
**Access:** Super user
**Description:** Sets the global list of URLs/hosts to ignore when detecting referrers (accepts fully qualified, protocol-less, or wildcard subdomain forms).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| excludedReferrers | string | yes | — | Comma-separated list of URLs/hosts |

**Returns:** Void (no return value).

### SitesManager.getKeepURLFragmentsGlobal

**Type:** Action
**Access:** Some view access (checkUserHasSomeViewAccess)
**Description:** Returns whether the default global behavior is to keep URL fragments when tracking.

**Parameters:** _None._

**Returns:** Boolean — true if fragments are kept by default.

### SitesManager.setKeepURLFragmentsGlobal

**Type:** Action
**Access:** Super user
**Description:** Sets whether the default global behavior should be to keep URL fragments when tracking.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| enabled | bool | yes | — | True to keep fragments, false to remove them |

**Returns:** Void (no return value).

### SitesManager.setGlobalExcludedQueryParameters

**Type:** Action
**Access:** Super user (delegated to setGlobalQueryParamExclusion)
**Description:** [DEPRECATED — use setGlobalQueryParamExclusion] Sets the list of URL query parameters to exclude on all websites.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| excludedQueryParameters | string | yes | — | Comma-separated list of URL query parameters |

**Returns:** Boolean — always true.

### SitesManager.getExcludedIpsGlobal

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the list of IPs excluded from all websites.

**Parameters:** _None._

**Returns:** Comma-separated string of IPs, or false.

### SitesManager.getDefaultCurrency

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns the default currency used when creating a website (defaults to 'USD').

**Parameters:** _None._

**Returns:** Currency code string.

### SitesManager.setDefaultCurrency

**Type:** Action
**Access:** Super user
**Description:** Sets the default currency used when creating websites.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| defaultCurrency | string | yes | — | Currency code, e.g. 'USD' |

**Returns:** Boolean — always true.

### SitesManager.getDefaultTimezone

**Type:** Action
**Access:** None (public)
**Description:** Returns the default timezone used when creating a website (defaults to 'UTC').

**Parameters:** _None._

**Returns:** Timezone identifier string.

### SitesManager.setDefaultTimezone

**Type:** Action
**Access:** Super user
**Description:** Sets the default timezone used when creating websites.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| defaultTimezone | string | yes | — | Timezone string, e.g. 'Europe/Paris' |

**Returns:** Boolean — always true.

### SitesManager.setGlobalQueryParamExclusion

**Type:** Action
**Access:** Super user
**Description:** Sets global query-parameter exclusion by type: common session params, Matomo recommended PII, or a custom list.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| exclusionType | string | yes | — | 'common_session_parameters', 'matomo_recommended_pii', or 'custom' |
| queryParamsToExclude | string\|null | no | null | Comma-separated params (required when type is 'custom') |

**Returns:** Void (no return value).

### SitesManager.getExclusionTypeForQueryParams

**Type:** Action
**Access:** Some view access (checkUserHasSomeViewAccess)
**Description:** Returns the query-parameter exclusion type, inferring it from existing custom exclusions when unset.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|null | no | null | Optional site ID for site-specific filtering |

**Returns:** Query-parameter exclusion type name string.

### SitesManager.updateSite

**Type:** Action
**Access:** Admin access to site
**Description:** Updates an existing website; any parameter left null keeps its current value.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Website ID to edit |
| siteName | string\|null | no | null | Website name |
| urls | string[]\|string\|null | no | null | Website URLs |
| ecommerce | int\|null | no | null | Ecommerce enabled (1) / disabled (0) |
| siteSearch | int\|null | no | null | Site Search enabled (1) / disabled (0) |
| searchKeywordParameters | string\|null | no | null | Comma-separated search keyword params |
| searchCategoryParameters | string\|null | no | null | Comma-separated search category params |
| excludedIps | string\|null | no | null | Comma-separated IPs to exclude (wildcards allowed) |
| excludedQueryParameters | string\|null | no | null | Comma-separated URL query params to strip |
| timezone | string\|null | no | null | Timezone string |
| currency | string\|null | no | null | Currency code |
| group | string\|null | no | null | Group name (requires Superuser) |
| startDate | string\|null | no | null | Statistics start date YYYY-MM-DD |
| excludedUserAgents | string\|null | no | null | Comma-separated user-agent substrings to exclude |
| keepURLFragments | int\|null | no | null | 1 keep, 2 remove, 0 use global default |
| type | string\|null | no | null | Website type |
| settingValues | array\|null | no | null | Measurable settings keyed by plugin |
| excludeUnknownUrls | bool\|null | no | null | Track only URLs matching registered URLs |
| excludedReferrers | string\|null | no | null | Comma-separated hosts/URLs to exclude from referrers |
| description | string\|null | no | null | Optional site description |

**Returns:** Void (no return value).

### SitesManager.getCurrencyList

**Type:** Action
**Access:** None (public)
**Description:** Returns the list of supported currencies as code-to-name (with symbol) pairs.

**Parameters:** _None._

**Returns:** Map of currency code to human-readable name with symbol.

### SitesManager.getCurrencySymbols

**Type:** Action
**Access:** None (public)
**Description:** Returns the list of supported currency symbols.

**Parameters:** _None._

**Returns:** Map of currency code to its symbol.

### SitesManager.isTimezoneSupportEnabled

**Type:** Action
**Access:** Some view access (checkUserHasSomeViewAccess)
**Description:** Returns whether timezone support is enabled on the server.

**Parameters:** _None._

**Returns:** Boolean — true if timezone support is available.

### SitesManager.getTimezonesList

**Type:** Action
**Access:** None (public)
**Description:** Returns the list of supported timezones grouped by continent, used to populate timezone selectors.

**Parameters:** _None._

**Returns:** Timezones grouped by continent (identifier to human-readable label).

### SitesManager.getTimezoneName

**Type:** Action
**Access:** None (public)
**Description:** Returns a user-friendly label for a timezone (usually the country name, plus a city for multi-timezone countries).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| timezone | string | yes | — | Timezone, e.g. 'Asia/Tokyo' |
| countryCode | string\|null | no | null | Upper-case country code, or null to auto-detect |
| multipleTimezonesInCountry | bool\|null | no | null | Whether the country has multiple timezones, or null to auto-detect |

**Returns:** Timezone label string, e.g. "Japan" or "United States - Los Angeles".

### SitesManager.getUniqueSiteTimezones

**Type:** Action
**Access:** Super user
**Description:** Returns the list of unique timezones currently in use across all configured sites.

**Parameters:** _None._

**Returns:** List of distinct timezone identifier strings.

### SitesManager.getPatternMatchSites

**Type:** Action
**Access:** None (public) — results limited to sites the current user has at least view access to
**Description:** Finds websites matching a pattern in their name, URL or group.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pattern | string | yes | — | Search string to match name/URL/group |
| limit | int\|false | no | false | Max sites to return |
| sitesToExclude | int[] | no | [] | Site IDs to exclude |

**Returns:** List of matching site objects.

### SitesManager.getNumWebsitesToDisplayPerPage

**Type:** Action
**Access:** Some view access (checkUserHasSomeViewAccess)
**Description:** Returns the number of websites to display per page (used for pagination in site selectors and dashboards).

**Parameters:** _None._

**Returns:** Integer number of websites per page.

### SitesManager.detectConsentManager

**Type:** Action
**Access:** View access to site
**Description:** Scans a site's content to detect which consent manager (if any) is in use and whether it is connected to Matomo. (Marked `@internal`.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to inspect |
| timeOut | int | no | 60 | HTTP timeout in seconds (clamped to 1–60) |

**Returns:** Array `{name, url, isConnected}` of the detected consent manager, or null.

## UsersManager

_Manages users and their permissions (roles/capabilities) to access specific websites: create, invite, update, delete users, list users, and get/set site access and user preferences._

### UsersManager.getAvailableRoles

**Type:** Action
**Access:** Some admin access
**Description:** Returns the list of all available roles, excluding the `superuser` and `noaccess` roles.

**Parameters:**
_None._

**Returns:** List of roles, each with `id`, `name`, `description`, and `helpUrl`.

### UsersManager.getAvailableCapabilities

**Type:** Action
**Access:** Some admin access
**Description:** Returns the list of all available capabilities.

**Parameters:**
_None._

**Returns:** List of capabilities, each with `id`, `name`, `description`, `helpUrl`, `includedInRoles`, and `category`.

### UsersManager.setUserPreference

**Type:** Action
**Access:** Super user or the user themselves (super user required when target is the anonymous user)
**Description:** Sets a supported UsersManager preference for a user. Plugins can register custom preference names via config.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login of the user whose preference is updated. |
| preferenceName | string | yes | — | Preference name registered by UsersManager or plugin config. |
| preferenceValue | mixed | yes | — | Value to store for the preference. |

**Returns:** void.

### UsersManager.getUserPreference

**Type:** Action
**Access:** Super user or the user themselves
**Description:** Returns a supported UsersManager preference for a user, falling back to its default when unset.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| preferenceName | string | yes | — | Preference name to read. |
| userLogin | string\|null\|false | no | false | User login to read; `false` reads the current user. |

**Returns:** Stored preference value, or the default value when none was saved.

### UsersManager.getUsersPlusRole

**Type:** Action
**Access:** Admin access to site (non-admins see only their own user; anonymous users see nothing)
**Description:** Returns all users along with their role for a given site, enriched with capabilities. Non-super admins only see users with access to sites they administer. Sends `X-Matomo-Total-Results` header.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to inspect. |
| limit | int\|null | no | null | Maximum number of users to return. |
| offset | int\|null | no | 0 | Zero-based result offset. |
| filter_search | string\|null | no | null | Text to search in user login or email. |
| filter_access | string\|null | no | null | Access filter (`noaccess`, `some`, `view`, `write`, `admin`, `superuser`; `superuser` only for super users). |
| filter_status | string\|null | no | null | Invite status filter. |

**Returns:** List of visible users enriched with role and capabilities for the site.

### UsersManager.getUsers

**Type:** Action
**Access:** Some admin access
**Description:** Returns users visible to the current requester, optionally filtered to specific logins.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogins | string | no | '' | Comma-separated logins to fetch; empty returns every visible user. |

**Returns:** List of matching users enriched with invite and access metadata.

### UsersManager.getUsersLogin

**Type:** Action
**Access:** Some admin access
**Description:** Returns the login names of all users visible to the current requester.

**Parameters:**
_None._

**Returns:** Array of matching user logins (string[]).

### UsersManager.getUsersSitesFromAccess

**Type:** Action
**Access:** Super user
**Description:** Returns the site IDs where each user has the requested access entry; users without that access are omitted.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| access | string | yes | — | Access entry to match (role or capability ID). |

**Returns:** Mapping of user login to the site IDs where that access entry is assigned.

### UsersManager.getUsersAccessFromSite

**Type:** Action
**Access:** Admin access to site
**Description:** Returns one access entry per visible user for the requested site; users with no access are omitted.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric site ID. |

**Returns:** Mapping of user login to access entry.

### UsersManager.getUsersWithSiteAccess

**Type:** Action
**Access:** Admin access to site
**Description:** Returns users who have the requested access entry for a website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to inspect. |
| access | string | yes | — | Access entry to match (role or capability ID). |

**Returns:** List of matching users enriched with user metadata.

### UsersManager.getSitesAccessFromUser

**Type:** Action
**Access:** Super user
**Description:** Returns the raw site access entries assigned to a user. Super users receive every site with `admin` access.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Existing user login to inspect. |

**Returns:** Site access rows for the user (each with `site` and `access`).

### UsersManager.getSitesAccessForUser

**Type:** Action
**Access:** Some admin access
**Description:** Returns site access rows for a non-superuser, with filtering and pagination. Rejects super users. Sends `X-Matomo-Total-Results` and `X-Matomo-Has-Some` headers.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Existing non-superuser login to inspect. |
| limit | int\|null | no | null | Maximum number of sites to return. |
| offset | int\|null | no | 0 | Zero-based result offset. |
| filter_search | string\|null | no | null | Text to search in site names, URLs, or groups. |
| filter_access | string\|null | no | null | Access filter (`some`, `view`, `write`, `admin`). |

**Returns:** Site access rows including role and explicit capabilities for each returned site.

### UsersManager.getUser

**Type:** Action
**Access:** Super user or the user themselves
**Description:** Returns one user's metadata as visible to the requester.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Existing user login to fetch. |

**Returns:** Enriched user data, or an empty array when no record is returned.

### UsersManager.getUserByEmail

**Type:** Action
**Access:** Super user
**Description:** Returns one user's metadata for the given email address.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userEmail | string | yes | — | Existing email address to look up. |

**Returns:** Enriched user data, or an empty array when no record is returned.

### UsersManager.addUser

**Type:** Action
**Access:** Some admin access (non-superusers must supply an initial site)
**Description:** Creates a new user account. Password confirmation is required when using session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login name for the new user. |
| password | string | yes | — | Password for the new user. |
| email | string | yes | — | Email address for the new user. |
| _isPasswordHashed | bool | no | false | `true` if `password` is already pre-hashed. |
| initialIdSite | int\|null | no | null | Initial site to grant `view` access; required for non-superusers. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** void.

### UsersManager.inviteUser

**Type:** Action
**Access:** Some admin access
**Description:** Invites a new user by email and grants initial access to a website. Password confirmation required for session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login name for the invited user. |
| email | string | yes | — | Email address for the invited user. |
| initialIdSite | int\|null | no | null | Initial site to grant `view` access to (required in practice). |
| expiryInDays | int\|null | no | null | Days before the invite expires; uses configured default when empty. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** void.

### UsersManager.setSuperUserAccess

**Type:** Action
**Access:** Super user
**Description:** Enables or disables super user access for a user. Granting super user access removes all previous permissions. Password confirmation may be required.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | User login to update. |
| hasSuperUserAccess | bool\|int\|string | yes | — | `true`/`1` to grant, `false`/`0` to remove. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required. |

**Returns:** void.

### UsersManager.hasSuperUserAccess

**Type:** Action
**Access:** None (public) — reports the current user's status
**Description:** Detects whether the current user has super user access.

**Parameters:**
_None._

**Returns:** `true` if the current user has super user access (bool).

### UsersManager.getUsersHavingSuperUserAccess

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Returns all users that currently have super user access (not filtered by access, since the UI must display them).

**Parameters:**
_None._

**Returns:** List of super user records enriched with invite metadata.

### UsersManager.updateUser

**Type:** Action
**Access:** Super user or the user themselves
**Description:** Updates a user's password and/or email. Current user's password confirmation is required (when enabled) if password or email changes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login of the user to update. |
| password | string\|false | no | false | New password, or `false` to keep the current one. |
| email | string\|false | no | false | New email, or `false` to keep the current one. |
| _isPasswordHashed | bool | no | false | `true` if `password` is already pre-hashed. |
| passwordConfirmation | string\|false | no | false | Current user's password confirmation when required. |

**Returns:** void.

### UsersManager.deleteUser

**Type:** Action
**Access:** Some admin access (non-superusers may only delete pending users they invited)
**Description:** Deletes a user account and all of its access assignments. Password confirmation required for session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Existing user login to delete. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** void.

### UsersManager.logoutUser

**Type:** Action
**Access:** Super user
**Description:** Signs a user out of all active sessions (e.g. for a lost or compromised device). Password confirmation required for session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login of the user to sign out. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** void.

### UsersManager.userExists

**Type:** Action
**Access:** Must be logged in (non-anonymous) with some view access
**Description:** Returns whether the given login exists. The anonymous login and the current user's own login are always treated as existing.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login to check. |

**Returns:** `true` if the login exists (bool).

### UsersManager.userEmailExists

**Type:** Action
**Access:** Must be logged in (non-anonymous) with some view access
**Description:** Returns whether a user with the given email exists.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userEmail | string | yes | — | Email address to check. |

**Returns:** `true` if the email exists (bool).

### UsersManager.getUserLoginFromUserEmail

**Type:** Action
**Access:** Must be logged in (non-anonymous) with some admin access
**Description:** Returns the login name for an existing user with the given email address.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userEmail | string | yes | — | Email address to look up. |

**Returns:** Login name of the matched user (string).

### UsersManager.setUserAccess

**Type:** Action
**Access:** Admin access to the target site(s)
**Description:** Sets access entries for a user across one or more sites. `noaccess` removes existing entries; otherwise replaces them with one role plus optional capabilities. Anonymous user may only be granted `view` or `noaccess`.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | User login to update. |
| access | string\|list<string> | yes | — | Access entries to grant; `noaccess` to remove, or one role plus optional capabilities. |
| idSites | string\|int\|int[] | yes | — | Site ID(s): single, array, comma-separated list, or `all`. |
| passwordConfirmation | string\|null | no | null | Password confirmation; only required when granting anonymous `view` access via session auth. |

**Returns:** void.

### UsersManager.addCapabilities

**Type:** Action
**Access:** Admin access to the target site(s)
**Description:** Adds capabilities to a user for given sites. Only allowed on sites where the user already has a role; cannot target the anonymous or super users. Capabilities already implied by the role are skipped.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | User login to update. |
| capabilities | string\|string[] | yes | — | Capability IDs to add. |
| idSites | int\|int[]\|string | yes | — | Site ID or IDs to update. |

**Returns:** void.

### UsersManager.removeCapabilities

**Type:** Action
**Access:** Admin access to the target site(s)
**Description:** Removes separately granted capability rows from a user for given sites. Capabilities implied by an assigned role remain effective.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | User login to update. |
| capabilities | string\|string[] | yes | — | Capability IDs to remove. |
| idSites | int\|int[]\|string | yes | — | Site ID or IDs to update. |

**Returns:** void.

### UsersManager.createAppSpecificTokenAuth

**Type:** Action
**Access:** None (public) — authenticated by the supplied user login plus password confirmation
**Description:** Generates a new app-specific API token for a user after verifying the user's current password.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login name or email address of the user. |
| passwordConfirmation | string | yes | — | The user's current password. |
| description | string | yes | — | Description for the token (e.g. app name). |
| expireDate | string\|null | no | null | Optional expiry date for the token. |
| expireHours | int\|string | no | 0 | Optional hours before expiry; ignored when `expireDate` is set. |
| secureOnly | bool | no | false | `true` if the token must not be accepted in GET requests. |

**Returns:** Newly generated app-specific token (string).

### UsersManager.newsletterSignup

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Signs the current user up for the Matomo newsletter.

**Parameters:**
_None._

**Returns:** Signup result payload (`['success' => true]` or `['error' => true]`).

### UsersManager.resendInvite

**Type:** Action
**Access:** Some admin access (non-superusers only for users they invited)
**Description:** Resends an existing user invitation email. Password confirmation required for session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login name of the invited user. |
| expiryInDays | int | no | 7 | Days before the regenerated invite expires. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** void.

### UsersManager.generateInviteLink

**Type:** Action
**Access:** Some admin access (non-superusers only for users they invited)
**Description:** Generates a fresh invitation link for an existing pending user. Password confirmation required for session auth.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login name of the invited user. |
| expiryInDays | int | no | 7 | Days before the generated invite expires. |
| passwordConfirmation | string\|null | no | null | Current user's password confirmation when required by session auth. |

**Returns:** Generated invitation URL (string).

## TwoFactorAuth

_Provides API methods for managing two-factor authentication._

### TwoFactorAuth.resetTwoFactorAuth

**Type:** Action
**Access:** Super user
**Description:** Disables (resets) two-factor authentication for the specified user, after confirming the current user's password.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| userLogin | string | yes | — | Login of the user whose 2FA should be reset |
| passwordConfirmation | string | no | '' | Current superuser's password confirmation |

**Returns:** Void (no return value).

## Login

_Provides API methods for login-related administration tasks (brute-force protection)._

### Login.unblockBruteForceIPs

**Type:** Action
**Access:** Super user
**Description:** Removes all currently blocked brute-force protection IP addresses.

**Parameters:** _None._

**Returns:** Void (no return value).

## PrivacyManager

_Manage GDPR workflows, data anonymization settings, and privacy compliance controls._

### PrivacyManager.deleteDataSubjects

**Type:** Action
**Access:** Some admin access; admin access to the sites of the given visits
**Description:** Deletes the requested data subjects from the stored visit data.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| visits | array | yes | — | Visit descriptors to delete; each entry must contain idsite and idvisit. |

**Returns:** array<string,int> — deletion counts keyed by storage area (log table or plugin name).

### PrivacyManager.exportDataSubjects

**Type:** Report getter
**Access:** Some admin access; admin access to the sites of the given visits
**Description:** Exports the requested data subjects from the stored visit data.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| visits | array | yes | — | Visit descriptors to export; each entry must contain idsite and idvisit. |

**Returns:** array grouped by log table name, each containing an array of row data.

### PrivacyManager.findDataSubjects

**Type:** Report getter
**Access:** Some admin access (per-site view access also filtered)
**Description:** Finds data subjects matching a segment across the requested websites (only sites with visitor logs/profiles enabled); returns at most 401 matching visits.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string\|int[] | yes | — | Website ID(s): comma-separated, "all", numeric strings, or ["all"]. |
| segment | string | yes | — | Segment expression identifying the data subjects (supports ; and ,). |

**Returns:** DataTable of matching visitor details (reduced column set), or an empty array when no sites qualify.

### PrivacyManager.anonymizeSomeRawData

**Type:** Action
**Access:** Super user (password confirmation required)
**Description:** Schedules asynchronous anonymization of selected raw visit data.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSites | int\|string\|int[] | yes | — | Website ID(s); empty or "all" schedules all websites. |
| date | string | yes | — | Date or date range to anonymize. |
| anonymizeIp | bool | no | false | Anonymize visitor IP addresses. |
| anonymizeLocation | bool | no | false | Anonymize stored location data. |
| anonymizeUserId | bool | no | false | Anonymize stored user IDs. |
| unsetVisitColumns | string[] | no | [] | Visit column names to clear. |
| unsetLinkVisitActionColumns | string[] | no | [] | Link-visit-action column names to clear. |
| passwordConfirmation | string | no | '' | Current user password confirmation. |

**Returns:** void.

### PrivacyManager.getAvailableVisitColumnsToAnonymize

**Type:** Report getter
**Access:** Super user
**Description:** Returns visit-log columns that can be anonymized manually.

_None._

**Returns:** array of available visit columns with their default replacement values.

### PrivacyManager.getAvailableLinkVisitActionColumnsToAnonymize

**Type:** Report getter
**Access:** Super user
**Description:** Returns link-visit-action columns that can be anonymized manually.

_None._

**Returns:** array of available link-visit-action columns with their default replacement values.

### PrivacyManager.getAnonymisationSettings

**Type:** Report getter
**Access:** Admin access to site when idSiteSpecific is given; otherwise super user (marked @internal)
**Description:** Returns the current anonymization and privacy settings.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSiteSpecific | int\|null | no | null | Specific site ID to load settings for, or null for global. |

**Returns:** array of anonymization settings (mask length options, referrer anonymization options, tracker file details, etc.).

### PrivacyManager.setAnonymizeIpSettings

**Type:** Action
**Access:** Admin access to site when idSiteSpecific is given; otherwise super user (marked @internal)
**Description:** Applies IP anonymization settings globally or for a specific website.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| anonymizeIPEnable | bool | yes | — | Enable IP anonymization. |
| ipAddressMaskLength | int | yes | — | Number of bytes to mask in stored IPs. |
| useAnonymizedIpForVisitEnrichment | bool | yes | — | Use anonymized IPs for visit enrichment. |
| anonymizeUserId | bool | no | false | Anonymize stored user IDs. |
| anonymizeOrderId | bool | no | false | Anonymize stored ecommerce order IDs. |
| anonymizeReferrer | string | no | '' | Referrer anonymization mode. |
| forceCookielessTracking | bool | no | false | Force cookieless tracking instance-wide (ignored for site-specific). |
| randomizeConfigId | bool | no | false | Randomize visitor config IDs. |
| idSiteSpecific | int\|null | no | null | Specific site ID to update, or null for global. |
| useSiteSpecificSettings | bool | no | false | Keep site-specific settings; if false for a site request, override is removed. |
| passwordConfirmation | string | no | '' | Password confirmation (required when randomizeConfigId enabled). |

**Returns:** bool — true after settings are updated or the site override is removed.

### PrivacyManager.deactivateDoNotTrack

**Type:** Action
**Access:** Super user (marked @internal)
**Description:** Disables support for the Do Not Track browser header.

_None._

**Returns:** bool — true after Do Not Track support has been disabled.

### PrivacyManager.activateDoNotTrack

**Type:** Action
**Access:** Super user (marked @internal)
**Description:** Enables support for the Do Not Track browser header.

_None._

**Returns:** bool — true after Do Not Track support has been enabled.

### PrivacyManager.setScheduleReportDeletionSettings

**Type:** Action
**Access:** Super user (password confirmation required; marked @internal)
**Description:** Configures the minimum interval between scheduled data deletion runs.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| deleteLowestInterval | int | no | 7 | Minimum number of days between scheduled deletion runs. |
| passwordConfirmation | string | no | '' | Current user password confirmation. |

**Returns:** bool — true after the settings have been saved.

### PrivacyManager.setDeleteLogsSettings

**Type:** Action
**Access:** Super user (password confirmation required; marked @internal)
**Description:** Configures automatic raw log deletion settings.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| enableDeleteLogs | int\|string | no | '0' | Flag enabling raw log deletion. |
| deleteLogsOlderThan | int | no | 180 | Delete logs older than this many days (values below 1 normalized to 1). |
| passwordConfirmation | string | no | '' | Current user password confirmation. |

**Returns:** bool — true after the settings have been saved.

### PrivacyManager.setDeleteReportsSettings

**Type:** Action
**Access:** Super user (password confirmation required; marked @internal)
**Description:** Configures automatic report deletion settings.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| enableDeleteReports | int\|string | no | 0 | Flag enabling report deletion. |
| deleteReportsOlderThan | int | no | 3 | Delete reports older than this many periods (below 2 normalized to 2). |
| keepBasic | int | no | 0 | Keep basic metrics. |
| keepDay | int | no | 0 | Keep day reports. |
| keepWeek | int | no | 0 | Keep week reports. |
| keepMonth | int | no | 0 | Keep month reports. |
| keepYear | int | no | 0 | Keep year reports. |
| keepRange | int | no | 0 | Keep range reports. |
| keepSegments | int | no | 0 | Keep segmented reports. |
| passwordConfirmation | string | no | '' | Current user password confirmation. |

**Returns:** bool — true after the settings have been saved.

### PrivacyManager.executeDataPurge

**Type:** Action
**Access:** Super user (password confirmation required; marked @internal)
**Description:** Executes a data purge, deleting raw data and report data using the current config options.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| passwordConfirmation | string | yes | — | Current user password confirmation. |

**Returns:** void.

### PrivacyManager.getCompliancePolicies

**Type:** Report getter
**Access:** None (no explicit access check; marked @internal)
**Description:** Returns the available compliance policies.

_None._

**Returns:** array — list of compliance policy details.

### PrivacyManager.getComplianceStatus

**Type:** Report getter
**Access:** Super user (marked @internal)
**Description:** Returns the compliance status for a given policy and site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int\|string | yes | — | Site ID to inspect, or "all" for global status. |
| complianceType | string | yes | — | Compliance policy name to inspect. |

**Returns:** array — compliance status (enforcement state, config control flag, requirement details).

### PrivacyManager.setComplianceStatus

**Type:** Action
**Access:** Super user (password confirmation required for session tokens; marked @internal)
**Description:** Enables or disables enforcement of a compliance policy.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | string | yes | — | Site ID to update, or "all" for global status. |
| complianceType | string | yes | — | Compliance policy name to update. |
| enforce | bool | yes | — | true to enforce the policy, false to disable enforcement. |
| passwordConfirmation | string\|null | no | null | Current user password confirmation when required. |

**Returns:** bool — true if the policy is enabled after the update, false otherwise.

## Dashboard

_Manage user dashboards and retrieve their widget configurations._

### Dashboard.getDashboards

**Type:** Report getter
**Access:** None strictly required — anonymous receives the default dashboard; otherwise super user or the user themselves (checkUserHasSuperUserAccessOrIsTheUser)
**Description:** Returns the dashboards available to a user, including the widgets in each dashboard. Falls back to the default dashboard when the user has none.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | no | '' | Login of the user to load dashboards for (defaults to current user) |
| returnDefaultIfEmpty | bool | no | true | Whether to return the default dashboard when the user has none |

**Returns:** list of dashboards, each containing name, id, and widgets.

### Dashboard.createNewDashboardForUser

**Type:** Action
**Access:** Must be logged in (non-anonymous); super user or the user themselves
**Description:** Creates a new dashboard for a user, optionally populated with the default widget layout.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | yes | — | Login of the user the dashboard should be created for |
| dashboardName | string | no | '' | Name of the new dashboard |
| addDefaultWidgets | bool | no | true | Whether to populate with the default widget layout |

**Returns:** int|string — ID of the newly created dashboard.

### Dashboard.removeDashboard

**Type:** Action
**Access:** Must be logged in (non-anonymous); super user or the user themselves
**Description:** Removes a dashboard for a user. (Deleting the first dashboard, ID 1, is allowed but requires immediately adding a new one; intended for automation only.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idDashboard | int | yes | — | ID of the dashboard to remove |
| login | string | no | '' | Login of the dashboard owner (defaults to current user) |

**Returns:** void (no return value).

### Dashboard.copyDashboardToUser

**Type:** Action
**Access:** Admin access to at least one site (checkUserHasSomeAdminAccess)
**Description:** Copies one of the current user's dashboards to another user.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idDashboard | int | yes | — | ID of the dashboard to copy |
| copyToUser | string | yes | — | Login of the user that should receive the dashboard copy |
| dashboardName | string | no | '' | Name for the copied dashboard |

**Returns:** int|string — ID of the newly created dashboard copy.

### Dashboard.resetDashboardLayout

**Type:** Action
**Access:** Must be logged in (non-anonymous); super user or the user themselves
**Description:** Resets a dashboard to the default widget layout.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idDashboard | int | yes | — | ID of the dashboard to reset |
| login | string | no | '' | Login of the dashboard owner (defaults to current user) |

**Returns:** void (no return value).

## LanguagesManager

_Access existing Matomo translations and manage per-user language and time-format preferences._

### LanguagesManager.isLanguageAvailable

**Type:** Report getter
**Access:** None (public)
**Description:** Returns whether a language code can be used in the current Matomo instance.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| languageCode | string | yes | — | The ISO language code to validate |
| _ignoreConfig | bool | no | false | Whether to ignore the configured language allowlist |

**Returns:** bool — true if the language is available, false otherwise.

### LanguagesManager.getAvailableLanguages

**Type:** Report getter
**Access:** None (public)
**Description:** Returns the available Matomo language codes.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| _ignoreConfig | bool | no | false | Whether to ignore the configured language allowlist |

**Returns:** List of available ISO language codes.

### LanguagesManager.getAvailableLanguagesInfo

**Type:** Report getter
**Access:** None (public)
**Description:** Returns translation coverage information for each available language, including names, translators and completion percentage.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| excludeNonCorePlugins | bool | no | true | Whether to exclude non-core plugins from the percentage calculation |
| _ignoreConfig | bool | no | false | Whether to ignore the configured language allowlist |

**Returns:** List of per-language translation metadata (code, name, english_name, translators, percentage_complete).

### LanguagesManager.getAvailableLanguageNames

**Type:** Report getter
**Access:** None (public)
**Description:** Returns the available languages with their localized and English names.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| _ignoreConfig | bool | no | false | Whether to ignore the configured language allowlist |

**Returns:** List of available languages with `code`, `name` and `english_name` fields.

### LanguagesManager.getTranslationsForLanguage

**Type:** Report getter
**Access:** None (public)
**Description:** Returns all translation strings for a specific language across core and loaded plugins.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| languageCode | string | yes | — | The ISO language code to load |

**Returns:** List of translation entries with `label` and `value` keys, or false if the language is unavailable.

### LanguagesManager.getLanguageForUser

**Type:** Report getter
**Access:** Super user or the user themselves
**Description:** Returns the saved language preference for a user.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | yes | — | The user login to read the language for |

**Returns:** string saved language code, or false for the anonymous user.

### LanguagesManager.setLanguageForUser

**Type:** Action
**Access:** Super user or the user themselves; must be logged in (non-anonymous)
**Description:** Stores the language preference for a user.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | yes | — | The user login to update |
| languageCode | string | yes | — | The ISO language code to store |

**Returns:** bool — true if stored, false if the language code is unavailable.

### LanguagesManager.uses12HourClockForUser

**Type:** Report getter
**Access:** Super user or the user themselves
**Description:** Returns whether a user prefers 12-hour time formatting.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | yes | — | The user login to query |

**Returns:** bool — true if the user uses a 12-hour clock, false otherwise or for the anonymous user.

### LanguagesManager.set12HourClockForUser

**Type:** Action
**Access:** Super user or the user themselves
**Description:** Stores whether a user prefers 12-hour time formatting.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| login | string | yes | — | The user login to update |
| use12HourClock | bool | yes | — | Whether to enable 12-hour clock formatting |

**Returns:** bool — true if the preference was stored, false for the anonymous user.

## Feedback

_Provides API methods for submitting product feedback and managing feedback reminders._

### Feedback.sendFeedbackForFeature

**Type:** Action
**Access:** Must be logged in (non-anonymous); requires some view access
**Description:** Sends a feature survey response (like/dislike, optional choice, and message) to the Matomo team or configured feedback email address.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| featureName | string | yes | — | Name of the feature the feedback is about |
| like | bool\|null | no | null | Whether the user likes the feature |
| choice | string\|null | no | null | Optional selected multiple-choice answer |
| message | string\|null | no | null | Feedback message entered by the user |

**Returns:** string — a translation-key validation message, or `success` when the feedback email is sent.

### Feedback.sendFeedbackForSurvey

**Type:** Action
**Access:** Must be logged in (non-anonymous); requires some view access
**Description:** Sends a survey question/answer to the Matomo team (or the configured feedback email address) and postpones the next reminder by six months.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| question | string | yes | — | Survey question or feature label the answer belongs to |
| message | string\|false | no | false | Survey answer entered by the user |

**Returns:** string — a translation-key validation message, or `success` when the feedback email is sent.

### Feedback.updateFeedbackReminderDate

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Postpones the feedback reminder for the current user by six months.

**Parameters:**
_None._

**Returns:** string — JSON-encoded array containing the next reminder date.

## Tour

_Provides API methods for Tour challenges and engagement levels._

### Tour.getChallenges

**Type:** Report getter
**Access:** Super user
**Description:** Returns the available Tour challenges for the current super user, including each challenge's completion and skip state.

**Parameters:**
_None._

**Returns:** array — list of challenge entries with `id`, `name`, `description`, `isCompleted`, `isSkipped`, and `url`.

### Tour.skipChallenge

**Type:** Action
**Access:** Super user
**Description:** Marks the specified Tour challenge as skipped for the current super user. Throws if the challenge is already completed or not found.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| id | string | yes | — | The challenge ID to skip |

**Returns:** bool — `true` when the challenge was skipped successfully.

### Tour.getLevel

**Type:** Report getter
**Access:** Super user
**Description:** Returns the current Tour level details for the current super user, including current and next level names.

**Parameters:**
_None._

**Returns:** array — level details with `description`, `currentLevel`, `currentLevelName`, `nextLevelName`, `numLevelsTotal`, and `challengesNeededForNextLevel`.

## CoreAdminHome

_Administrative API methods for scheduling, archiving, invalidation, tracking failures, and opt-out code generation._

### CoreAdminHome.runScheduledTasks

**Type:** Action
**Access:** Super user
**Description:** Runs all scheduled tasks that are due to run at this time.

**Parameters:**
_None._

**Returns:** Array of results for each executed scheduled task (each with `task` and `output`).

### CoreAdminHome.setArchiveSettings

**Type:** Action
**Access:** Super user
**Description:** Sets browser-trigger archiving and today's archive time-to-live settings. (Internal; requires general settings admin to be enabled.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| enableBrowserTriggerArchiving | bool\|string | yes | — | Whether browser-triggered archiving is enabled |
| todayArchiveTimeToLive | int\|string | yes | — | Time-to-live for today's archive |

**Returns:** true on success.

### CoreAdminHome.setTrustedHosts

**Type:** Action
**Access:** Super user
**Description:** Saves the list of trusted hostnames into the configuration. (Internal; requires general settings admin to be enabled.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| trustedHosts | string[] | yes | — | List of trusted hostnames |

**Returns:** true on success.

### CoreAdminHome.setBrandingSettings

**Type:** Action
**Access:** Super user
**Description:** Enables or disables use of a custom logo/favicon and publishes any temporary uploaded logo or favicon. (Internal.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| useCustomLogo | bool\|string | yes | — | Whether to use a custom logo |
| hasCustomLogo | bool\|string | yes | — | Whether a custom logo is available |
| hasCustomFavicon | bool\|string | yes | — | Whether a custom favicon is available |

**Returns:** Array describing the applied branding settings (e.g. `useCustomLogo`, `customLogoPath`, `customFaviconPath`).

### CoreAdminHome.invalidateArchivedReports

**Type:** Action
**Access:** Admin access to site
**Description:** Invalidates report data so it is recomputed on the next archiving run. Done automatically when tracking or importing visits in the past.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSites | string | yes | — | Comma-separated list of site IDs to invalidate reports for |
| dates | string\|string[] | yes | — | Comma-separated dates/date ranges to invalidate (array when period is range) |
| period | 'day'\|'week'\|'month'\|'year'\|'range'\|false | no | false | Period type to invalidate; parents are invalidated too |
| segment | string\|false | no | false | Segment to invalidate reports for |
| cascadeDown | bool | no | false | If true, child periods are also invalidated |
| _forceInvalidateNonexistent | bool | no | false | Whether to also invalidate archives that do not currently exist |

**Returns:** Array of log messages describing the scheduled invalidation work.

### CoreAdminHome.runCronArchiving

**Type:** Action
**Access:** Super user
**Description:** Initiates cron archiving via web request, streaming log output into the HTTP response.

**Parameters:**
_None._

**Returns:** No return value (void); logs are dumped to output.

### CoreAdminHome.deleteAllTrackingFailures

**Type:** Action
**Access:** Admin access to site (super users also delete failures for nonexistent sites; otherwise requires some admin access)
**Description:** Deletes all tracking failures the user has at least admin access to. A super user also deletes tracking failures for sites that no longer exist.

**Parameters:**
_None._

**Returns:** No return value (void).

### CoreAdminHome.deleteTrackingFailure

**Type:** Action
**Access:** Admin access to site
**Description:** Deletes a specific tracking failure for a site.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Site ID that owns the tracking failure |
| idFailure | int\|string | yes | — | Tracking failure ID to delete |

**Returns:** No return value (void).

### CoreAdminHome.getTrackingFailures

**Type:** Report getter
**Access:** Admin access to site (super users also see failures for nonexistent sites; otherwise requires some admin access)
**Description:** Returns all tracking failures visible to the current user. A super user also retrieves failed requests for sites that no longer exist.

**Parameters:**
_None._

**Returns:** Array of tracking failures visible to the current user.

### CoreAdminHome.archiveReports

**Type:** Action
**Access:** Super user for direct/bulk archiveReports calls, otherwise View access to site
**Description:** Prepares (runs) the archive for a given site, period, date and optional segment/plugin/report. (Internal.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Site ID to archive |
| period | string | yes | — | Period (day, week, month, year, range) |
| date | string | yes | — | Date or date range |
| segment | string\|null\|false | no | false | Segment to archive |
| plugin | string\|null\|false | no | false | Restrict archiving to a specific plugin |
| report | string\|string[]\|null\|false | no | false | Restrict archiving to a specific report |

**Returns:** Array with archive results (e.g. `idarchives`, `nb_visits`, and peak memory usage when triggered via archive.php).

### CoreAdminHome.getOptOutJSEmbedCode

**Type:** Action
**Access:** None (public)
**Description:** Returns the JavaScript embed code for the opt-out iframe, styled with the provided colors, fonts and options. (Internal.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| backgroundColor | string | yes | — | Background color |
| fontColor | string | yes | — | Font color |
| fontSize | string | yes | — | Font size |
| fontFamily | string | yes | — | Font family |
| applyStyling | bool | yes | — | Whether to apply styling |
| showIntro | bool | yes | — | Whether to show the intro text |
| matomoUrl | string | yes | — | Base Matomo URL |
| language | string | yes | — | Language code |

**Returns:** Opt-out JavaScript embed code (string).

### CoreAdminHome.getOptOutSelfContainedEmbedCode

**Type:** Action
**Access:** None (public)
**Description:** Returns the self-contained opt-out embed code styled with the provided colors, fonts and options. (Internal.)

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| backgroundColor | string | yes | — | Background color |
| fontColor | string | yes | — | Font color |
| fontSize | string | yes | — | Font size |
| fontFamily | string | yes | — | Font family |
| applyStyling | bool | no | false | Whether to apply styling |
| showIntro | bool | no | true | Whether to show the intro text |

**Returns:** Self-contained opt-out embed code (string).

### CoreAdminHome.whatIsNewMarkAllChangesReadForCurrentUser

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Marks all "what is new" changes as read for the currently logged-in user. (Internal.)

**Parameters:**
_None._

**Returns:** true if changes were marked as read, false if the user was not found.

## CorePluginsAdmin

_API methods for reading and updating plugin settings (all methods are marked `@internal`)._

### CorePluginsAdmin.setSystemSettings

**Type:** Action
**Access:** Super user
**Description:** Saves system-level plugin settings after confirming the current user's password. Marked `@internal`.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| settingValues | array | yes | — | Map of plugin name to setting name/value entries |
| passwordConfirmation | string\|false | no | false | Current user's password confirmation (SensitiveParameter) |

**Returns:** void (no return value).

### CorePluginsAdmin.setUserSettings

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Saves user-level plugin settings for the current user. Marked `@internal`.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| settingValues | array | yes | — | Map of plugin name to setting name/value entries |

**Returns:** void (no return value).

### CorePluginsAdmin.getSystemSettings

**Type:** Report getter
**Access:** Super user
**Description:** Returns formatted system-level plugin settings. Marked `@internal`.

**Parameters:**
_None._

**Returns:** array of formatted system settings.

### CorePluginsAdmin.getUserSettings

**Type:** Report getter
**Access:** Must be logged in (non-anonymous)
**Description:** Returns formatted user-level plugin settings for the current user. Marked `@internal`.

**Parameters:**
_None._

**Returns:** array of formatted user settings.

### CorePluginsAdmin.getNumberOfPluginUpdates

**Type:** Report getter
**Access:** Super user (returns 0 on any failure, including access denial)
**Description:** Returns the number of plugins that have updates available on the Marketplace (cached ~5 minutes; 0 if the Marketplace is disabled). Marked `@internal`.

**Parameters:**
_None._

**Returns:** int — number of plugin updates available.

## DBStats

_Reports on the overall status of the MySQL tables used by Matomo (super-user only)._

### DBStats.getGeneralInformation

**Type:** Report getter
**Access:** Super user
**Description:** Gets general information about the Matomo installation, including tracked website count, user count, and total database space used.

**Parameters:**
_None._

**Returns:** array — [website count, user count, total database size].

### DBStats.getDBStatus

**Type:** Report getter
**Access:** Super user
**Description:** Gets general database info that is not specific to any table (from MySQL SHOW STATUS).

**Parameters:**
_None._

**Returns:** array of database status rows returned by the metadata provider.

### DBStats.getDatabaseUsageSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable summarizing how data is distributed among Matomo tables, grouped into tracker, numeric archive, blob archive, and other tables (four rows).

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getTrackerDataSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by each log (tracker) table.

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getMetricDataSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by each numeric archive table.

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getMetricDataSummaryByYear

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by each numeric archive table, grouped by year.

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getReportDataSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by each blob archive table.

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getReportDataSummaryByYear

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by each blob archive table, grouped by year.

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getAdminDataSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing how much space is taken up by 'admin' tables (any table that is not an archive or log table).

**Parameters:**
_None._

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getIndividualReportsSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing total space taken up by each individual report type (goal reports and reports of format .*_[0-9]+ are grouped).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| forceCache | bool | no | false | Whether to bypass the cache and recalculate the summary |

**Returns:** DataTable with columns data_size, index_size, row_count.

### DBStats.getIndividualMetricsSummary

**Type:** Report getter
**Access:** Super user
**Description:** Returns a datatable describing total space taken up by each individual metric type (goal metrics, metrics of format .*_[0-9]+ and 'done...' metrics are grouped).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| forceCache | bool | no | false | Whether to bypass the cache and recalculate the summary |

**Returns:** DataTable with columns data_size, index_size, row_count.

## Marketplace

_Lets you manage your license key so you can download and install premium plugins you have subscribed to._

### Marketplace.createAccount

**Type:** Action (internal)
**Access:** Super user
**Description:** Creates a new Matomo Marketplace account for the given email address, validates the email against configured rules, then stores the returned license key.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| email | string | yes | — | Email address for the new Marketplace account |

**Returns:** bool — `true` once the account is created and the license key stored.

### Marketplace.deleteLicenseKey

**Type:** Action
**Access:** Super user
**Description:** Deletes an existing license key if one is set.

**Parameters:**
_None._

**Returns:** bool — `true` after the stored license key has been removed.

### Marketplace.requestTrial

**Type:** Action (internal)
**Access:** Must be logged in (non-anonymous)
**Description:** Requests a free trial of the given premium plugin on behalf of a non-super-user. Rejects super users and invalid/unknown plugin names.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pluginName | string | yes | — | Name of the premium plugin to request a trial for |

**Returns:** bool — `true` when the trial request has been submitted.

### Marketplace.startFreeTrial

**Type:** Action (internal)
**Access:** Super user
**Description:** Starts a free trial for the given plugin via the Marketplace service using the stored license key.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| pluginName | string | yes | — | Name of the plugin to start a free trial for |

**Returns:** bool — `true` when the free trial has started successfully.

### Marketplace.saveLicenseKey

**Type:** Action
**Access:** Super user
**Description:** Saves the given license key if it is actually valid (exists on the Matomo Marketplace and is not yet expired).

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| licenseKey | string | yes | — | Marketplace license key to validate and store |

**Returns:** bool — `true` after the license key has been validated and saved.

## ProfessionalServices

_Provides API methods for Professional Services widgets and prompts._

### ProfessionalServices.dismissWidget

**Type:** Action
**Access:** Must be logged in (non-anonymous)
**Description:** Dismisses a Professional Services promo widget for the current user. (Marked `@internal`; the `widgetName` is read from the request.)

**Parameters:** _None._ (Reads `widgetName` from the request parameters.)

**Returns:** Boolean — true when the dismissal was recorded.

## CustomJsTracker

_Provides API methods for custom JavaScript tracker configuration._

### CustomJsTracker.doesIncludePluginTrackersAutomatically

**Type:** Action
**Access:** Some admin access (checkUserHasSomeAdminAccess)
**Description:** Returns whether plugin tracker files will be included automatically in `matomo.js`.

**Parameters:** _None._

**Returns:** Boolean — whether plugin tracker files are included automatically.

## JsTrackerInstallCheck

_Internal plugin API to verify whether the JavaScript tracking code has been successfully installed on a site._

### JsTrackerInstallCheck.wasJsTrackerInstallTestSuccessful

**Type:** Action
**Access:** View access to site
**Description:** Checks whether a test tracking request was recorded for the given nonce, and returns the site's main URL. Returns false when no request matched or the nonce is not found.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to query |
| nonce | string | no | '' | Optional nonce to validate; if omitted, returns the most recent result |

**Returns:** Array `{isSuccess: bool, mainUrl: string}`.

### JsTrackerInstallCheck.initiateJsTrackerInstallTest

**Type:** Action
**Access:** View access to site
**Description:** Initiates a JS tracker install test by generating a nonce and storing it, to be detected later during the Tracker.isExcludedVisit event.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Numeric ID of the website to test |
| url | string | no | '' | Optional URL to append the nonce to (defaults to the site's main URL) |

**Returns:** Array `{url: string, nonce: string}`.

## Overlay

_Exposes translation data and overlay-specific page transition reports._

### Overlay.getTranslations

**Type:** Action
**Access:** None (public)
**Description:** Returns the translation strings used by the Overlay client.

**Parameters:**
_None._

**Returns:** array<string, string> — Overlay translation strings keyed by client-side identifier.

### Overlay.getExcludedQueryParameters

**Type:** Action
**Access:** None (public)
**Deprecated:** Use `SitesManager.getExcludedQueryParameters` instead (to be removed in Matomo 6).
**Description:** Returns the excluded query parameters configured for a website, used for client-side URL normalization. Delegates to `SitesManager.getExcludedQueryParameters`.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| idSite | int | yes | — | Deprecated site ID parameter retained for backward compatibility |

**Returns:** array — excluded query parameter names.

### Overlay.getFollowingPages

**Type:** Report getter
**Access:** None (public); access enforced by the delegated Transitions API
**Description:** Returns the following pages reached after visits to a specific page URL, computed from the raw logs (not archives). Use `filter_limit=-1` to avoid the default result limit.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| url | string | yes | — | Page URL to analyze |
| idSite | int | yes | — | The numeric ID of the website to query |
| period | string | yes | — | Period to process (day, week, month, year, range) |
| date | string | yes | — | Date or date range to process |
| segment | string\|false\|null | no | false | Custom segment to filter the report |

**Returns:** DataTable — rows for following pages, outlinks, and downloads reached from the requested URL.

