function slug(s,  t){ t=tolower(s); gsub(/[^a-z0-9]+/,"-",t); gsub(/^-+|-+$/,"",t); if(length(t)>58) t=substr(t,1,58); gsub(/-+$/,"",t); return t }
function km(v){ return (v+0)<0 ? "not computed (no valid coordinate)" : sprintf("%.2f km", v+0) }
function volt(v){ if(v=="") return "unstated"; gsub(/;/," / ",v); return v }
function esc(s){ gsub(/\|/,"/",s); return s }
function L(x){ D = D x "\n" }
function pctstr(p){ return sprintf("%.0f%%", p*100) }
BEGIN{ FS="\t" }
{
  ref=$1; mw=$2+0; tech=$3; st=$4; nm=$5; op=$6; lpa=$7; cty=$8; rgn=$9; ctry=$10;
  lon=$11; lat=$12; geom=$13; subd=$14; gr=$15; expd=$16; upd=$17; pref=$18;
  sk=$19+0; sv=$20; sn=$21; ck=$22+0; ckv=$23; dk=$24+0; dn=$25; ok=$26+0; on=$27;
  dtok=$28+0; dlist=$29; spvshape=$30; bind=$31; state=$32; dsc=$33+0; lead=$34+0; pct=$35+0;
  verdict=$36; score=$37+0; opn=$38+0; opm=$39+0; addr=$40;

  fn=sprintf("%07.1f-%s-%s.md", mw, ref, slug(nm));
  if (fn in used) { used[fn]++; fn=sprintf("%07.1f-%s-%s-%d.md", mw, ref, slug(nm), used[fn]) } else used[fn]=1;

  D="";
  L("# " esc(nm));
  L("");
  L("**Verdict: " verdict "**  |  window score " sprintf("%.1f",score) " / 100  |  REPD ref `" ref "`  |  " sprintf("%.1f",mw) " MW " tech);
  L("");
  L("> Generated 2026-08-31 from data already held in the repositories. No live register, Companies House");
  L("> or news fetch was performed. Everything marked **inferred** is a derived opinion of this model,");
  L("> never a published fact.");
  L("");
  L("---");
  L("");
  L("## 1. Identity - official, from the frozen REPD spine");
  L("");
  L("| field | value |");
  L("|---|---|");
  L("| repd_ref | `" ref "` |");
  L("| gg_project_id | `GG2050-REPD-" ref "` |");
  L("| name | " esc(nm) " |");
  L("| capacity_mw | **" sprintf("%.1f",mw) "** |");
  L("| technology | " tech " |");
  L("| official status | " st " |");
  L("| operator / applicant as published | " (op==""?"_not published_":esc(op)) " |");
  L("| planning authority | " (lpa==""?"_none recorded_":esc(lpa)) " |");
  L("| county | " (cty==""?"_none_":esc(cty)) " |");
  L("| region / country | " esc(rgn) " / " esc(ctry) " |");
  L("| coordinates (lat, lon) | " (geom=="valid" ? lat ", " lon : "**" geom "** - no usable point") " |");
  L("| planning application reference | " (pref==""?"**empty - blocks any register lookup**":"`" esc(pref) "`") " |");
  L("| application submitted | " (subd==""?"_not recorded_":subd) " |");
  L("| permission granted | " (gr==""?"_not recorded_":gr) " |");
  L("| permission expired | " (expd==""?"-":expd) " |");
  L("| REPD record last updated | " (upd==""?"_unknown_":upd) " |");
  L("");
  L("Source: `pipelinenews/data/projects/202608261927-project-partition-v9-1-*.json` - DESNZ REPD Q2 2026,");
  L("spine release 9.1, `projects_sha256 24484ca8...5ad52`, 7,680 records at 1 MW and above.");
  L("");
  L("## 2. Lifecycle state - INFERRED");
  L("");
  L("The spine carries five lifecycle values. This refines them into the eight-state commercial model drafted in");
  L("`_build-plan/window-intelligence.md` section 9, using only the official status and the official dates.");
  L("");
  L("- Official status: **" st "**");
  L("- Inferred window state: **" state "**");
  if (state=="FUNDING_WINDOW_INFERRED") L("- Reading: consented, and early enough in the consent-to-construction lead that the money for studies, cable and LV design is plausibly being committed **now**.");
  else if (state=="PROCURING_INFERRED") L("- Reading: consented and well into the lead. Design decisions are likely being made; this is the last call for specification influence.");
  else if (state=="PAST_EXPECTED_START") L("- Reading: consented longer ago than the calibrated median lead for its class, with no construction recorded. Either stalled, or building without the register catching up. Needs a live check.");
  else if (state=="DESIGN_FROZEN_OR_LATER") L("- Reading: already building. Cable and LV are decided. Delivery and O and M only.");
  else if (state=="PRE_CONSENT") L("- Reading: no consent yet. Nothing is being bought. Watch only.");
  else if (state=="DISTRESSED") L("- Reading: planning permission has expired. Under the evidence-order rule, distress outranks everything.");
  else if (state=="CONSENTED_NO_DATE") L("- Reading: recorded as awaiting construction but with no permission-granted date, so the clock cannot be started. Abstain.");
  else L("- Reading: insufficient official evidence to place this project in the commercial model. Abstain.");
  L("");
  L("## 3. Timing - INFERRED against a calibration measured from this spine");
  L("");
  if (gr!="" && dsc>=0) {
    L("Calibration: over the 7,680-project spine, every solar and BESS project that reached construction was measured");
    L("for `under_construction - planning_permission_granted`. Medians over the 1,176 projects carrying both dates:");
    L("solar **234 days** (n=1,003), BESS **570 days** (n=143). By band: solar 1-5 MW 213 d (n=288), solar 5-20 MW");
    L("218 d (n=584), solar 20-50 MW 457 d (n=121), BESS 20-50 MW 707 d (n=72). Bands with fewer than 30 samples");
    L("fall back to the technology median rather than guess.");
    L("");
    L("| measure | value |");
    L("|---|---|");
    L("| permission granted | " gr " |");
    L("| days since consent, to 2026-08-31 | **" dsc "** |");
    L("| calibrated median lead for this class | " lead " days |");
    L("| position through the lead | **" pctstr(pct) "** |");
    L("");
    if (pct<=0.60) L("At " pctstr(pct) " through the calibrated lead this project sits inside the **funding window** as this model defines it, being 0 to 60 per cent of consent-to-construction. Studies, cable and LV design are bought here.");
    else if (pct<=1.00) L("At " pctstr(pct) " through the calibrated lead this project is in the **procurement** band, 60 to 100 per cent. Later than ideal for specification influence, but not yet frozen.");
    else L("At " pctstr(pct) " of the calibrated lead, this project is past the point at which a comparable project had started building. Treat as stalled-or-unrecorded until a live register check says otherwise.");
  } else if (st=="Under Construction") {
    L("Already under construction. The consent-to-construction lead no longer applies; the design freeze has passed.");
  } else if (state=="DISTRESSED") {
    L("Permission expired" (expd!=""?" on **" expd "**":"") ". No timing model applies.");
  } else {
    L("No `planning_permission_granted` date is recorded on the spine, so no timing position can be computed.");
    L("This is an abstention, not a finding of no activity.");
  }
  L("");
  L("## 4. Grid exposure - computed from held topology, screening-grade only");
  L("");
  L("Straight-line distance from the project point to the nearest feature in the pinned V8 transplant");
  L("(`data-gridatlas` generation 202608291015: 5,800 substations; 400/275/132 kV circuit vertices sampled every");
  L("third vertex, 47,897 points). **A straight line is not a route, a connection, a cost or a likelihood.**");
  L("");
  L("| measure | value |");
  L("|---|---|");
  L("| nearest transmission circuit | " km(ck) (ckv!=""?" at " ckv " kV":"") " |");
  L("| nearest substation | " km(sk) " |");
  L("| that substation, voltage | " volt(sv) " |");
  L("| that substation, name | " (sn==""?"_unnamed in source_":esc(sn)) " |");
  L("| nearest mapped data centre | " km(dk) (dn!=""?" - " esc(dn):"") " |");
  L("| nearest industrial offtaker | " km(ok) (on!=""?" - " esc(on):"") " |");
  L("");
  if (ck>=0 && ck<=2) L("Very close to a " ckv " kV circuit. Connection engineering is a near-term conversation.");
  else if (ck>=0 && ck<=10) L("Within a plausible connection distance of a " ckv " kV circuit.");
  else if (ck>=0) L("Some distance from the nearest mapped transmission circuit; a distribution-level connection is the more likely route.");
  else L("No coordinate, so no grid exposure could be computed. That absence is itself a reason to check the record.");
  L("");
  L("## 5. Corporate and procurement evidence already held");
  L("");
  L("| measure | value |");
  L("|---|---|");
  L("| operator as published | " (op==""?"_not published_":esc(op)) " |");
  L("| that operator, live solar and BESS projects in this pipeline | " opn " |");
  L("| that operator, live solar and BESS MW in this pipeline | " sprintf("%.1f",opm) " MW |");
  L("| operator name has SPV shape, legal suffix plus energy token | " spvshape " |");
  L("| distinctive project-name tokens | " dtok " (" (dlist==""?"none":dlist) ") |");
  L("| SPV-binding strength under the drafted rule | **" bind "** |");
  L("| addressable by `?repd_ref=` in GridAtlas today | **" addr "** |");
  L("");
  if (bind=="HIGH") L("Two or more distinctive name tokens. Under the binding rule drafted in `companies-engine.md` section 6.3 this project is a **high-precision** candidate for binding to a project vehicle by name, if and when the company register is queried.");
  else if (bind=="LOW") L("Only one distinctive name token. Under the drafted binding rule that is too weak to bind a vehicle on its own; corroboration would be required.");
  else L("No distinctive name token of five or more characters. The deterministic SPV name rule in `companies/build/python/202608262245-compile-companies-house.py` **cannot** generate a candidate edge for this project at all.");
  if (opn>=5) { L(""); L("The named operator holds " opn " live projects totalling " sprintf("%.1f",opm) " MW in this pipeline - a portfolio developer, not a single-asset vehicle. Expect the project company to sit beneath a parent, and expect procurement to be centralised."); }
  L("");
  L("**Limitation, stated plainly.** The 482,030-row Company-REPD candidate table exists in this workspace only as a");
  L("ZSTD Parquet blob on the `candidate/202608272155-compact` branch of `Ventusltd/companies`. It cannot be decoded");
  L("without DuckDB, which this session is not permitted to run. So no per-project company edge is quoted here. What");
  L("is quoted instead is the deterministic name rule applied to this project, which predicts whether an edge could");
  L("exist at all. Every such edge is `ABSTAIN` with role `UNKNOWN` by contract, and none of it is ownership.");
  L("");
  L("## 6. Funding-window judgement - INFERRED");
  L("");
  if (state=="FUNDING_WINDOW_INFERRED") L("**Approaching design freeze: YES, and early.** Consented " dsc " days ago against a calibrated median lead of " lead " days for its class. On the evidence held, this is the phase in which studies, cable and LV design are commissioned.");
  else if (state=="PROCURING_INFERRED") L("**Approaching design freeze: YES, and late.** " pctstr(pct) " through the calibrated lead. Specification influence is closing.");
  else if (state=="PAST_EXPECTED_START") L("**Approaching design freeze: CANNOT SAY.** Consented " dsc " days ago, which is " pctstr(pct) " of the calibrated lead. Either construction has begun and the register has not caught up, or the project has stalled. In held data the two look identical.");
  else if (state=="DESIGN_FROZEN_OR_LATER") L("**Approaching design freeze: NO - it has passed.** The project is building.");
  else if (state=="PRE_CONSENT") L("**Approaching design freeze: NO.** No consent, so no clock. Nothing is being bought yet.");
  else if (state=="DISTRESSED") L("**Approaching design freeze: NO.** Permission has expired. Under the evidence-order rule distress outranks every other signal.");
  else L("**Approaching design freeze: CANNOT SAY.** Insufficient official evidence.");
  L("");
  L("Score " sprintf("%.1f",score) " / 100. Components: inferred state, capacity, grid proximity, record freshness,");
  L("name-binding strength, demand adjacency. Weights are declared in `_RANKING.md` section 3.");
  L("");
  L("## 7. What cannot be determined without a live fetch");
  L("");
  L("These are the gaps a supervised fetch would close. None can be answered from held data.");
  L("");
  L("1. **Registered charges** - has a lender taken security over the project vehicle, and on what date? The earliest funding evidence. Needs the Companies House REST charges endpoint.");
  L("2. **Corporate PSC change** - has the developer sold, or a fund taken control? Needs the PSC endpoint or the PSC snapshot product.");
  L("3. **Company rename, SIC change, status change** - obtainable by diffing two Basic Company Data snapshots; the repositories hold neither snapshot.");
  L("4. **Which company actually is the vehicle** - the candidate table is present but undecodable here, and every row is ABSTAIN with role UNKNOWN by contract.");
  if (pref!="") L("5. **Condition discharge and reserved matters** - the procurement tell. Needs the LPA register; this project does carry reference `" esc(pref) "` to query with.");
  else L("5. **Condition discharge and reserved matters** - the procurement tell. This project carries **no planning application reference**, so a register lookup would have to abstain rather than guess.");
  L("6. **Grid connection status** - is there a NESO connection-register entry, and at what stage? Nothing held answers this.");
  L("7. **Actual construction start** - the register lags. For the PAST_EXPECTED_START population this is the decisive unknown.");
  L("8. **Contractor and ICP appointments** - no attribution row exists for this project anywhere in the repositories.");
  L("");
  L("## 8. Verdict");
  L("");
  if (verdict=="WATCH") L("**WATCH** - in or near the commercial window on held evidence. Confirm with a live register and charge check before acting.");
  else if (verdict=="TOO EARLY") L("**TOO EARLY** - no consent yet, so nothing is being bought. Re-check when the application is determined.");
  else if (verdict=="TOO LATE") L("**TOO LATE** - already building. The cable and LV decisions are made. Aftermarket only.");
  else if (verdict=="DISTRESSED") L("**DISTRESSED** - permission expired. Stop selling and note the exposure.");
  else L("**UNKNOWN** - insufficient evidence to place this project. Abstain rather than guess.");
  if (addr=="NO") { L(""); L("> **Deep-link warning.** This `repd_ref` is not present in the GridAtlas REPD Parquet, so"); L("> `?repd_ref=" ref "` would not resolve on the map today. See `_RANKING.md` section 5."); }
  L("");
  printf "%s", D > fn;
  close(fn);
  n++;
}
END{ print n " study files written" }
