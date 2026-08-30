# postcodes.io Source Card

> **DRAFT — for review, then copy to `spiders/docs/sources/postcodes_io.md`.**
> **PRIORITY 1: this source is already called by the shipped product and has no card.**
> Nothing in this file was fetched. Every value marked *verify on first supervised run* must be confirmed
> against the publisher before the status moves past `studied`.

Document type: source-card

Source name: postcodes.io

Publisher / owner: Ideal Postcodes (operator of the postcodes.io open service)

Primary URL: `https://api.postcodes.io`

Source-card status: **draft — must reach `approved-for-declared-reference` because the product already depends on it**

Last checked: not checked in this session — no network access permitted

Licence: the underlying data is ONS/Ordnance Survey open data redistributed by the service; the ONS Postcode
Directory and OS Open Names are published under the Open Government Licence v3.0 with an Ordnance Survey and Royal
Mail copyright notice. *Exact wording and any service-level terms: verify on first supervised run.*

Attribution requirement: OGL v3.0 attribution plus the OS / Royal Mail / ONS copyright line normally required for
ONSPD and OS Open Names. **The GridAtlas search cartridge currently displays
`Location only · postcodes.io · no project identity claimed` in every postcode popup, which names the service but
does **not** carry the upstream OS/ONS attribution.** *This is the specific compliance gap to close.*

Access method: public HTTPS JSON API, no authentication

API key required: no

Rate limit or access limit: the service publishes no hard published quota but asks for reasonable use.
**Current product behaviour is one request per keystroke behind a 180 ms debounce** — on a fast typist that is
several requests per second per user. *Verify the acceptable rate on first supervised run and set a ceiling.*

Data type: UK postcode lookup, outcode lookup, and place (OS Open Names) search, each returning coordinates and
administrative geography

Update frequency: follows the quarterly ONS Postcode Directory and OS Open Names release cycle

Field list (as used by the product today):
`postcode`, `outcode`, `longitude`, `latitude`, `admin_district`, `admin_county`, `region`, and for places
`name_1`, `local_type`, `county_unitary`, `region`

Declared fields: everything the endpoint returns for `/postcodes/{postcode}`, `/outcodes/{outcode}` and
`/places?q=`

Derived-only fields: any GridAtlas classification, any join to a REPD project, any inference that a postcode
implies a project location

Known gaps:
- terminated postcodes are not distinguished by the current product code
- **no parish, ward or LSOA is currently read**, although ONSPD carries them — this is the route to the missing
  parish join described in `questions.md` Q3
- place search returns settlements, not addresses

Known failure modes: HTTP 404 on an unknown postcode (already handled — the cartridge returns null, not an error);
service outage; rate limiting; schema drift on `result` shape; a valid-format postcode that is not live

Allowed Spider use: location lookup for a user-typed query; **fly-to only**; deriving a parish or ward from a
postcode *once that field is added to this card and the derivation is marked derived*

Not-allowed Spider use: establishing project identity. The GridAtlas cartridge already enforces this correctly —
`result_class: LOCATION_ONLY`, `sets_deep_link: false`, and `selectLocation()` **deletes** any stale `repd_ref`
from the URL before flying. That behaviour must not regress.

Screening boundary: a coordinate returned by this service locates a *place*. It never identifies a project, an
owner or an asset.

Status: draft

---

## Live-product exposure (why this card is urgent)

| fact | value |
|---|---|
| caller | `gridatlas/atlas/cartridges/202608301624-place-global-search-v9-5.js` |
| constant | `GEOCODER_BASE = 'https://api.postcodes.io'` |
| endpoints called | `/postcodes/{compact}`, `/outcodes/{compact}`, `/places?q=&limit=8` |
| trigger | **every keystroke**, 180 ms debounce |
| verified by | `gridatlas/tools/scope/verify-compose.mjs` asserts the literal `GEOCODER_BASE = 'https://api.postcodes.io'` |
| failure handling | already isolated — a geocoder failure cannot break the REPD lane, and failures are recorded in `state.geocoder_failures` |

The engineering is good. The **governance** is missing: `spiders/docs/os/EXTERNAL_SOURCE_RULES.md` states that
*"every external source needs a source-card before it becomes part of the Spider OS"*, and by extension before it
ships in a product. This card closes that, and the attribution line is the one substantive change it demands.
