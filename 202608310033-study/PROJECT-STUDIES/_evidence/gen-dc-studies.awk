function slug(s,  t){ t=tolower(s); gsub(/[^a-z0-9]+/,"-",t); gsub(/^-+|-+$/,"",t); if(length(t)>50) t=substr(t,1,50); gsub(/-+$/,"",t); return t }
function km(v){ return (v+0)<0 ? "no match within search radius" : sprintf("%.2f km", v+0) }
function volt(v){ if(v=="") return "unstated"; gsub(/;/," / ",v); return v }
function esc(s){ gsub(/\|/,"/",s); return s }
function L(x){ D = D x "\n" }
BEGIN{ FS="\t" }
{
  id=$1; lon=$2; lat=$3; lc=$4; url=$5; sk=$6+0; sv=$7; sn=$8; ck=$9+0; ckv=$10;
  vk=$11+0; vn=$12; pk=$13+0; pn=$14; pmw=$15; pst=$16; pref=$17; name=$18; score=$19+0; verdict=$20;
  short = (name!="") ? name : id;
  ord = (lc=="PROPOSED") ? "1-proposed" : ((lc=="CONSTRUCTION") ? "2-construction" : "3-built");
  fn = sprintf("%s-%03d-%s.md", ord, score, slug(short));
  if (fn in used) { used[fn]++; fn=sprintf("%s-%03d-%s-%d.md", ord, score, slug(short), used[fn]) } else used[fn]=1;

  D="";
  L("# " esc(short));
  L("");
  L("**Verdict: " verdict "**  |  demand score " score " / 100  |  OSM element `" id "`");
  L("");
  L("> Generated 2026-08-31 from data already held in the repositories. No Overpass, OSM, planning-register");
  L("> or operator fetch was performed. This is a **built-estate** record, not a project pipeline record.");
  L("> Everything marked **inferred** is a derived opinion of this model, never a published fact.");
  L("");
  L("---");
  L("");
  L("## 1. Identity - as published by the source");
  L("");
  L("| field | value |");
  L("|---|---|");
  L("| source record id | `" id "` |");
  L("| OSM element | " url " |");
  L("| coordinates (lat, lon) | " lat ", " lon " |");
  L("| lifecycle as tagged | **" lc "** |");
  L("| facility identity status | `SOURCE_ELEMENT_ONLY` |");
  L("| name in the OSM candidate export | **null** - the export carries no name |");
  L("| operator in the OSM candidate export | **null** |");
  L("| owner in the OSM candidate export | **null** |");
  L("| eligible for company binding | **false** |");
  L("| licence | ODbL-1.0 |");
  L("| attribution | (c) OpenStreetMap contributors |");
  L("");
  L("**`SOURCE_ELEMENT_ONLY` means what it says.** One OSM element is not one facility. Buildings and campuses are");
  L("not merged by the producer, deliberately, so two rows may describe one site and one row may describe part of a");
  L("site. Nothing here asserts a facility identity.");
  L("");
  L("## 2. Name recovery - cross-source proximity, NOT identity");
  L("");
  if (name!="") {
    L("The pinned V8 `datacentres` layer in `data-gridatlas` carries a named point **" sprintf("%.0f m",vk*1000) "** from this");
    L("element: **" esc(name) "**.");
    L("");
    L("At that separation the two records are almost certainly the same site - the V8 layer appears to derive from the");
    L("same OpenStreetMap source with names retained. **But proximity never establishes identity** under the federation");
    L("rule (`coordinates_are_identity: false`), so this name is offered as a **candidate label**, not as a fact about");
    L("this element. Confirming it requires re-reading the OSM tags, which needs a supervised Overpass fetch.");
  } else if (vk>=0) {
    L("The nearest named point in the pinned V8 `datacentres` layer is " km(vk) " away" (vn!=""?", recorded as \"" esc(vn) "\"":"") ".");
    L("That is too far, or too generic, to offer even as a candidate label. **This element remains unnamed.**");
  } else {
    L("No named point in the pinned V8 `datacentres` layer lies within the search radius. **This element remains unnamed.**");
  }
  L("");
  L("## 3. Grid exposure - computed from held topology, screening-grade only");
  L("");
  L("| measure | value |");
  L("|---|---|");
  L("| nearest transmission circuit | " km(ck) (ckv!=""?" at " ckv " kV":"") " |");
  L("| nearest substation | " km(sk) " |");
  L("| that substation, voltage | " volt(sv) " |");
  L("| that substation, name | " (sn==""?"_unnamed in source_":esc(sn)) " |");
  L("");
  if (ck>=0 && ck<=2) L("Sitting within 2 km of a " ckv " kV circuit. For a data centre that is the difference between a");
  else if (ck>=0 && ck<=10) L("Within " km(ck) " of a " ckv " kV circuit - a workable connection distance for a load of this kind.");
  else L("Some distance from mapped transmission. A large load here would depend on distribution reinforcement.");
  if (ck>=0 && ck<=2) L("viable large load and a decade in a connection queue. It is the single most commercially relevant fact held about this site.");
  L("");
  L("## 4. Generation adjacency - the pairing that matters");
  L("");
  if (pk>=0) {
    L("| measure | value |");
    L("|---|---|");
    L("| nearest live solar or BESS project | " km(pk) " |");
    L("| that project | " esc(pn) " |");
    L("| its capacity | " pmw " MW |");
    L("| its inferred window state | **" pst "** |");
    L("| its REPD reference | `" pref "` |");
    L("");
    if ((pst=="FUNDING_WINDOW_INFERRED" || pst=="PROCURING_INFERRED") && pk<=5) {
      L("**This is the high-value case.** A live generation project inside the inferred commercial window sits within");
      L(sprintf("%.2f km", pk) " of this load. Private-wire, co-location and behind-the-meter conversations are live *now*, and the");
      L("generation side is at the exact point where studies and cable design are being bought.");
    } else if ((pst=="FUNDING_WINDOW_INFERRED" || pst=="PROCURING_INFERRED")) {
      L("A live generation project inside the inferred commercial window sits " km(pk) " away. Too far for a private wire");
      L("without a substantial route, but close enough to matter for grid-capacity competition at the same nodes.");
    } else if (pk<=5) {
      L("A live generation project is close, but it is not in the commercial window (" pst "). Note the adjacency and");
      L("re-check when that project moves state.");
    } else {
      L("No live generation project close enough for a direct pairing conversation.");
    }
  } else {
    L("No live solar or BESS project was found within the search radius of this element.");
  }
  L("");
  L("## 5. Corporate evidence already held");
  L("");
  L("**None, by design.** The producer emits `eligible_for_company_binding: false` and");
  L("`abstention_reason: VERIFIED_COMPANY_NUMBER_REQUIRED` for every one of the 612 relationship rows in the");
  L("`data-centres-gb` candidate. No operator, owner or company number is asserted anywhere.");
  L("");
  L("The only company-side evidence held that touches this sector is aggregate: the `companies` candidate report");
  L("records **316 companies tagged `BTM_DATA_CENTRE`** (SIC 63110) out of 294,904 selected. That is a population,");
  L("not a link to this site.");
  L("");
  L("## 6. What cannot be determined without a live fetch");
  L("");
  L("1. **Name, operator and owner** - stripped from the candidate export. One bounded Overpass re-read recovers the tags.");
  L("2. **IT load in MW** - not in OSM, not in the repositories, and the single most important missing number. Only operator disclosure or a planning application carries it.");
  L("3. **Whether this element is one facility** - `SOURCE_ELEMENT_ONLY`. Merging buildings into campuses needs a deliberate, evidenced rule.");
  L("4. **Grid connection status and contracted capacity** - nothing held answers this; it needs the NESO connection register.");
  if (lc=="PROPOSED" || lc=="CONSTRUCTION") L("5. **The planning application behind it** - this element is tagged " lc ", so a planning record almost certainly exists. Nothing in the repositories links to it. This is the acquisition gap described in `DATACENTRES-NEXT/`.");
  else L("5. **Any expansion or new-build application at this site** - a built site is also a pipeline site if it is expanding. Nothing held would show that.");
  L("6. **The company that owns it** - Companies House number required before any binding, by contract.");
  L("");
  L("## 7. Verdict");
  L("");
  if (lc=="PROPOSED") L("**WATCH - PROPOSED.** One of only **8** elements in the whole held estate tagged `PROPOSED`. This is as close as the repositories currently get to a data-centre pipeline, and it is almost nothing. Acquiring the real proposed-and-consented pipeline is the priority described in `DATACENTRES-NEXT/NEXT-VERSION-DATACENTRES.md`.");
  else if (lc=="CONSTRUCTION") L("**WATCH - BUILDING.** One of only **4** elements tagged `CONSTRUCTION`. Load is arriving here; the connection is already agreed and the generation-pairing conversation is late but not closed.");
  else L("**BUILT / UNKNOWN STAGE.** Tagged `OPERATIONAL_OR_UNSPECIFIED`, which in OSM conflates \"running\" with \"untagged\". Demand-side value is retrofit, expansion and co-location, not new connection.");
  L("");
  printf "%s", D > fn;
  close(fn);
  n++;
}
END{ print n " data-centre study files written" }
