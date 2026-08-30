# chatgpt-audits
Claude has built a massive study, copy being uploaded for review
Massive study uploaded for review vs gridatlas repo, pipelinenews and so on. Keep all findings and sandboxes in this repo but do not be afraid to fetch data from others

# chatgpt-audits

The audit and sandbox repository for the Ventus grid-intelligence platform. This repo holds
STUDY, ANALYSIS, and SANDBOX work only. It is not a product repo. Nothing here is trusted
until a human has reviewed it and graduated it into a real repo.

## Purpose

This repo is the quarantined workshop notebook. Its job is to analyse the real product repos
(gridatlas, data-gridatlas, pipelinenews, companies, spiders, cvaa, globalgrid2050 and the
data-* repos) and produce findings, plans and draft artefacts — WITHOUT ever changing them.
A parallel analysis by Claude exists at gridatlas/_build-plan. The highest-value work here is
to CROSS-CHECK the two: where they agree, we trust; where they differ, we investigate.

## The product being analysed (context you must hold before writing anything)

This is a TIMING ENGINE for grid-connection sales, not a map. The money for studies, cable and
LV design is paid BEFORE a project's design freeze; the market fights over inverters AFTER. The
value is being one supplier a month ahead of the trade press by watching two registers —
Companies House for the FUNDING signal, local planning registers for the PROCUREMENT signal —
and staying silent until both are on the record. gridatlas is the front door where you SEE it;
the intelligence is knowing which project entered the funding window this week. The spine is a
frozen renewables planning extract (~7,680 records >1MW). Companies <-> pipelinenews <-> gridatlas
is the triangle; datacentres are the demand side, a second pipeline.

## Hard rules (every session, no exceptions)

- READ freely from any repo on local disk to analyse. WRITE only inside this repo.
- No git add/commit/push/checkout in any OTHER repo. No edits to any other repo's tracked files.
- "Fetch data from others" means READ the sibling repos locally. It does NOT mean live network
  fetch/scrape/API calls. Any real external fetch is a separate, supervised, source-carded job —
  never done unsupervised here.
- Everything produced is UNREVIEWED until a human marks it reviewed. Label it as such.
- Never claim inference as fact. Mark every derived opinion "inferred". Absence is not evidence.

## Folder convention
