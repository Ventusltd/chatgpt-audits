# Nominatim / OpenStreetMap Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/nominatim.md`.**
> **PRIORITY 1: this source is already called by the shipped product and has no card.**
> Nothing was fetched. Values marked *verify* must be confirmed before the status moves past `studied`.

Document type: source-card

Source name: Nominatim, the OpenStreetMap geocoding service

Publisher / owner: OpenStreetMap Foundation

Primary URL: `https://nominatim.openstreetmap.org/search`

Source-card status: **draft — must reach `approved-for-declared-reference`, with an explicit rate and attribution
undertaking, because the product already depends on it**

Last checked: not checked in this session — no network access permitted

Licence: **ODbL-1.0** for the underlying OpenStreetMap data. Derived works carry share-alike obligations.

Attribution requirement: **© OpenStreetMap contributors**, displayed wherever the data is shown. The GridAtlas
shell already carries `Data © OpenStreetMap contributors | © CARTO | EV data © Open Charge Map` in the map
attribution strip, and the search cartridge popup adds
`Location only · Nominatim / OpenStreetMap · no project identity claimed`. **Attribution is satisfied.**

Access method: public HTTPS JSON API

API key required: no

Rate limit or access limit: the OSMF usage policy for the public instance is restrictive — broadly **at most one
request per second**, a required identifying User-Agent or Referer, no heavy or bulk use, and no autocomplete-style
per-keystroke querying. **A browser cannot set a User-Agent.** This is the material compliance risk on this card.
*Verify the current policy text on first supervised run.*

Data type: forward geocoding — free-text place and address search returning coordinates and a display name

Update frequency: continuous, following OSM edits

Field list (as used by the product today): `lat`, `lon`, `name`, `display_name`, `address.city`, `address.town`,
`address.village`

Declared fields: everything `/search?format=jsonv2&addressdetails=1` returns

Derived-only fields: any GridAtlas ranking, deduplication against the UK lane, or classification of a result

Known gaps: coverage and naming vary by contributor activity; no authoritative UK address model; not a substitute
for a postcode directory

Known failure modes: HTTP 429 rate limiting, HTTP 403 on policy breach, service outage, empty results for a valid
place, schema drift, ambiguous international matches

Allowed Spider use: **explicit user-activated** global location search; fly-to only

Not-allowed Spider use:
- per-keystroke or autocomplete querying — **the product is already correct here**: the global lane runs only on
  Enter or the GO button, never on `input`
- establishing project identity — `result_class: LOCATION_ONLY`, `sets_deep_link: false`
- bulk geocoding of the REPD spine or any other dataset
- any use as a substitute for a licensed address source

Screening boundary: a Nominatim result locates a *place named by OSM contributors*. It never identifies a project,
an owner or an asset, and it is not an authoritative address.

Status: draft

---

## Live-product exposure

| fact | value |
|---|---|
| caller | `gridatlas/atlas/cartridges/202608301624-place-global-search-v9-5.js` |
| constant | `GLOBAL_GEOCODER_URL = 'https://nominatim.openstreetmap.org/search'` |
| trigger | Enter key or the GO button only — **not** on keystroke |
| parameters | `format=jsonv2&limit=8&addressdetails=1&accept-language=en&q=` |
| deduplication | `dedupeGlobalLocations()` drops results matching a UK-lane result by label within 0.03° |
| failure handling | isolated; failures recorded in `state.geocoder_failures` |

**The one thing to decide.** The public Nominatim instance is not intended to back a product's search box, however
politely it is called. Three options, in increasing cost:

1. keep the current explicit-activation behaviour, add a `Referer`-based identification, and document the expected
   volume in this card — cheapest, and probably acceptable at current usage;
2. move to a commercially supported geocoder for the global lane;
3. self-host a Nominatim instance.

Option 1 is the recommendation until measured volume says otherwise. What is **not** acceptable is shipping
against the public instance with no card, no volume estimate and no named owner of the obligation.
