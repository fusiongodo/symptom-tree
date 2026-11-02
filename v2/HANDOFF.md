# HANDOFF: ME/CFS symptom mapping – V1 CLOSED (2 Nov 2026, evening)

## Status
The symptom tree is **closed as V1**. No further work on it until the app V1 is done (next week). Then start with the
new granularisation workflow (below). The user commits himself; deliveries are zips with paths relative to v2/.

## What the last session did (user decisions 2 Nov 2026)
1. **FUNCAP = cost items (verified).** All 55 FUNCAP55 items (and all 27 FUNCAP27) share the stem "What are the consequences
   for you if you perform …? To what extent does this affect how much else you can do?", the 0–6 consequence scale and the
   timeframe (checked against `Instrument items`; sections.py asserts one response scale). Model:
   x = f(θ_budget − d(activity, abilities)) + ε. Abilities only raise the demand d → facet, not granule.
2. **New granule EN6 "Activity tolerance / energy budget"** (section Energy, construct FUN). All 55 FUNCAP items → EN6 only,
   no exceptions. Facets: `load type` (= FUNCAP domain A–H: self-care, walking and exercise, upright, housework,
   communication, outside home, light and sound, concentration; context, ASKED) + `load` (size, value type).
   Old mapping kept in each item's note ("Until V1 close: …"). Generated in sections.py (`LOAD_TYPE`, `F55_LOAD`,
   `F55_BEFORE`, `F55_ITEMS`, `COST_NODE`).
3. **CG8 removed** (only item was F55-49). "My memory" is now a direct leaf (CG5).
4. **Tree:** PF-N3 (was "A specific everyday activity" → PF1/PF3 [activity]) is now the cost node "What an activity costs
   me (energy budget)" → 8 load-type leaves + "in general" (unspecified) + "It changes – I say which activity at each
   check-in" (`load type: per check-in`, flag `facet per check-in` = the app's configuration option: fixed facet or named
   per check-in) + multi-select. Home = PF-N3 (FUN); EN-N3 under Energy is the second path (same leaves). Polarity of the
   cost leaves: bad (confirm question on mismatch). Facet `activity` no longer asked (STRICT is now `load type`).
5. **Taxonomy:** no item type 7. FUNCAP = type 2 (graded) on EN6, the activity sets the difficulty. "Cost" is a measure type;
   the measure-type rule now says a measure type that changes the measured VARIABLE is not a format.
6. **Instrument characterisation**: THEORY.md §2.7 (table + profiles) and poster panel 08 (live from `model.profile`,
   item type per item via `model.item_types`). Numbers V1: DSQ 104 items / 56 granules / 66 drawers, mostly context variants
   + single; RAND-36 36 / 14 / 15, mostly parallel; FUNCAP 55 / 1 / 8, all graded; Bell global; PGIC change.
7. **Poster corrections done:** no more hard truncation (`fit()` scales font), s-formula now s = h(θ_g(c_s)) + ε with
   stored π_A(c_s); examples that used FUNCAP as composite replaced (composite: DSQ2-38 → CG6, CG7; Jaccard: DSQ2-80
   {CG4, EN4}, J = 1/8; panel 01 walking: R36 only). Panels renumbered: 08 instruments, 09 polarity, 10 overlap,
   11 symbol index, 12 outlook (incl. new workflow).
8. **THEORY.md → out/theory.html** (pipeline/build_theory_html.py, needs `markdown`; build.sh runs it).
9. Method tab: rules upserted ("Measure type", "Facet 'activity'" superseded, "Asked facets", "Cost items (FUNCAP)",
   "Facet 'load type'", "Granule removed: CG8"). Recalc: 0 errors.

## Still not understood by the user (explicitly parked)
A / π_A and the s-formula (questions 4 and 5 below). The formula was rewritten, but he has not had an explanation that
worked. Explain only when he asks; differently than before (concrete example first).

## After App V1 (user, 2 Nov 2026) – also in THEORY.md §9 and poster panel 12
New granularisation workflow, developer more involved, systematic:
1. Read the instrument papers → general understanding (construct, question, scale, scoring).
2. Sketch how the tree connects to this instrument type and what to watch out for (lesson V1: FUNCAP asks cost, not ability).
3. An application where the AI proposes the granularisation per section (cross-instrument), maybe grouped by construct
   directly. The reviewer sees all items of the section plus the original question and scale of each instrument.
4. The reviewer must approve before the next section / construct.
5. Finally the tests (blind agent T1 + another one, e.g. blind second annotator for M).
Also: translate the DIY theory into psychometrics/statistics conventions; pain regions as own granules; decide the DSQ
context drawers (e.g. extra question after EN4); T1 on FUNCAP (user expected it to fail before the remap).

---

# (history) V2, session 2 Nov 2026 (afternoon) – questions 1–3 and 6 answered/implemented in the V1 close above

## START HERE (next chat)
User took a break; continue in a fresh chat. FIRST answer the open questions below, bottom-up, ONE topic per answer,
concrete example first (he did not understand the last explanations of A/π_A and of the s-formula – explain differently,
not the same way again). Do NOT apply the pending corrections before he has his answers; he asked "answer first".

**Before questions 1–3:** read FUNCAP, RAND-36 and DSQ COMPLETELY from `All items` (text, response format, granules,
facets). The previous chat only saw samples (DSQ ~60 items with facets, RAND-36 items 1–24, FUNCAP ~15 items). The claim
"all 55 FUNCAP items share the 0–6 cost scale" was generalised from F55-29..32 – VERIFY it.

### Open questions of the user (in this order of importance)
1. **FUNCAP = cost items (most important).** User: FUNCAP 32 "dinner party" does not measure divided attention /
   comprehension / expression / noise sensitivity, but how much the activity costs (energy budget, crash). A person with
   very low cognitive ability but no energy problem would answer 6. "Granules are actually facets" for these items.
   Claude's answer (accepted as direction, not confirmed): x = f(θ_tol − d(c)) + ε; θ_tol = tolerance / energy budget
   (EN2 fatigability, EN4 PEM), d(c) = demand of the activity; CG/SN granules describe the KIND of load (→ facet, e.g.
   key load-type); individual context (friends vs strict family) = unasked, person-specific facet (person × item
   interaction, missing measurement invariance → G-theory). Probably affects all FUNCAP items (0–6 consequence scale seen on F55-29..32 – UNVERIFIED for the rest),
   incl. physical ones. The Messtyp rule called FUNCAP "format only" – too weak: the measured variable changes.
   Proposal: item type 7 "Kosten" in the taxonomy + remapping as future todo. User unsure whether FUNCAP needs a new type.
2. **Update the item taxonomy.** User: FUNCAP is not composite-heavy, it mostly asks the same variable (budget) under
   different activities. Rethink the six types (THEORY.md §2) with this.
3. **Characterise the instruments by item types** (user: "very important", somewhere visible – poster + THEORY.md).
   User's sketch: FUNCAP = budget/cost per activity; DSQ = many different variables (symptom frequency + severity);
   RAND-36 = ? (user guess: much averaging, several varied questions per variable). Compute from data first
   (All items: Response format, Measure type, granules per item, drawers per instrument) and show it, e.g. per instrument:
   items, granules, items per granule, share parallel / graded / composite / cost, typical facet types lost.
4. **A and π_A** not understood ("A seems to be the tree – what is π_A then?"). Facts: A = list of facet KEYS the tree
   asks somewhere ({region, activity, bladder, sweating}); π_A = operation that deletes all facets whose key is not in A.
5. **s = h(θ, π_A(c)) + ε** not understood (user confidence 70 %; asked why not h(A(θ, c))). Claude admitted the formula
   mixes two things. Cleaner: s = h(θ_g(c_s)) + ε (c_s = what the user really means); we only observe π_A(c_s).
   A never acts on θ: the granule is always stored completely (G_ℓ). Rewrite in poster 01 + THEORY.md §1 accordingly.
6. User expects T1 (blind Haiku) to perform badly on FUNCAP – plausible given 1.; worth testing after the taxonomy fix.

### Pending corrections (apply only after the questions are answered)
- Poster chips are hard-truncated at 28 chars ("greying/blacking ou", "dizziness or fainti") → no truncation / wrap
  (pipeline/build_poster.py, `chip(...)[:28]` in panel 05 and similar `[:26]`, `[:40]`, `[:46]` cuts).
- Rewrite the s-formula (see 5.) and A / π_A wording in poster panel 01 and THEORY.md §1.
- New future todo (mark "nach App V1"): translate our DIY theory into the conventions of psychometrics / statistics.
- Add item type 7 + instrument characterisation (see 1.–3.).
- R3 confirmed by user (each facet key at most once per path). R1, R2 accepted.

### Artefacts (all generated by ./build.sh from data/mecfs-criteria.xlsx)
- out/theory-poster.svg – Lernplakat, panels 01–11 (generated by pipeline/build_poster.py, numbers live from merge.json)
- out/mapping-explorer.html – explorer, views Schubladen / Verluste / Granules; also published:
  https://claude.ai/artifact/WiWDfjP2Zppk2MEiMFj2fa (republish from the new chat via `url`)
- out/mecfs-tree.svg – the tree (pipeline/svg_tree.py)
- THEORY.md – text version of the theory (same notation as the poster, symbol index at the end)
- xlsx sheets worth reading for 3.: `All items` (cols: Response format, Measure type, Granule(s), Facets),
  `Instrument items` (verbatim, incl. FUNCAP27/DSQ-1), `Method` (rules)
- User commits himself (never commit/push). Deliver changed files as a zip with paths relative to v2/.

---

# HANDOFF: ME/CFS symptom mapping – V2 (2 Nov 2026)

## START HERE (V2)
V2 = repository package: theory (THEORY.md) + communication (out/theory-poster.svg, out/mecfs-tree.svg) + exploration
(out/mapping-explorer.html) + rough test setup (tests/t1). Everything is generated from ONE source: the Sec tabs of
data/mecfs-criteria.xlsx → `./build.sh`. Shared logic in pipeline/model.py (facet types, drawers, resolution chain).
The tree was deliberately NOT changed in V2.

**Theory built on 2 Nov (see THEORY.md; user loved it, keep the vocabulary):** five objects (θ, c, item, scale, score);
six item types (parallel = average, graded = scan the θ axis / IRT, composite, global, change, measured); three facet
types (Wert / Format / Kontext); tree leaf = (G_l, c_l|A), projection π_A, hit rule; drawers = equivalence classes
i ~ j ⇔ L(i) = L(j); resolution chain |items| ≥ |granule + all facets| ≥ |drawers| (DSQ 104 ≥ 99 ≥ 66, RAND-36 36 ≥ 33 ≥ 17,
FUNCAP 55 ≥ 55 ≥ 25; the older 95/30 in step 14 notes predate later mapping changes); the criterion (unasked facet is
lossless iff drawers differ only by Wert/Format); Jaccard overlap; polarity sign.

**Next (user's order of interest):**
1. Review the DSQ drawers flagged 'Kontext' in the explorer (14, heuristic by facet key) → decide per drawer: ask an extra
   facet, accept loss, or reclassify the facet value. Known: EN4 trigger physical / mental / exercise → extra question after EN4.
2. Mapping candidates: F55-32 dinner party + CG6 (word finding); R36-5 / R36-7 / R36-16 (see below).
3. Tests: T1 for DSQ + FUNCAP (3 runs), Test 3 (blind 2nd annotator for M).
4. Step 14 decisions 3–4, step 15 JSON export (unchanged, see below).
5. FUTURE (after app V1, user idea 2 Nov): LLM extracts per-check-in facets c_t from voice/text logs → refines the
   drawer per measurement (THEORY.md §10). Analyse at finest level with enough data, partial pooling to drawer; beware
   informative missingness. Not now – priority is app V1 (UX, Apple Health, privacy backend, presentations).
6. FUTURE (user, 2 Nov): build the tree on scientific standards (Guttman facet theory, Cronbach generalizability theory,
   or newer if those are outdated); test the decomposition θ_g(c) = θ_g + δ_g(c) per granule; todo: pain regions
   (head, belly …) become separate granules instead of facets of PN1 (user's view). See THEORY.md §9.

How to work with the user: bottom-up, one concept per answer, concrete example first, formulas welcome; no xlsx – use
the explorer / SVG. Abbreviations (non-IT) listed before the answer on first use.

---

# (V1 history) step 14: next session = formal framework (measurement model), then DSQ examples and tests

## START HERE (state 1 Nov 2026, evening)
**Where we stopped.** We were testing the tree (T1 pilot) when the user got worried: granules are not unique per item within an
instrument. Most of the session after that was explaining the model. Testing resumes once the user is at peace with the model.

**How to work with the user (important).**
- He does NOT read the xlsx. The xlsx is ground truth for scripts; show him content as SVG, HTML pages or ONE concrete example.
- Bottom-up, one topic per answer, short. Check understanding before moving on.

**Model explanation that worked (reuse it).**
1. Granule = a variable/concept (what is felt or done), not a single questionnaire question. Several items per granule are fine.
   Example: RAND-36 23 pep, 27 energy, 29 worn out, 31 tired → all EN1. RAND-36 itself averages them into one scale
   ("Energy/fatigue" in the RAND-36 docs; "Vitality" in SF-36). Studies report scales, not items → mapping to the right scale is enough.
   User accepted this for RAND-36.
2. Walking example: R36-9/10/11 (one mile / several blocks / one block) all PF2, differ only by facet load. The user's score value
   (e.g. metres walked) already contains that distinction → the tree does not need to ask it.
3. Facets = labels (where / when / how much / which activity). Items carry all their labels (from the item text). A score carries a
   label only if the tree asks for it (pain region, activity, bladder, sweating). A score name may contain a label the tree does not ask
   (e.g. 'dizzy when standing') → that label is lost; the score matches all items of the granule.
4. Uniqueness check (granule + ALL facets): DSQ 95/104, RAND-36 30/36, FUNCAP 55/55 items unique. With only the tree-asked facets the
   real ceiling is lower (not yet computed).

**GOAL OF THE NEXT SESSION (user, 1 Nov 2026, 20:45): define a real framework with mathematical character.**
User's words, condensed: "Until today my model was: granules = core concepts that all items across instruments are made of → every item
is uniquely identifiable within its instrument → a user variable always hits exactly one item per instrument. That model was clear and
I liked it. Then the shock: RAND-36 uses SEVERAL questions to pin down ONE variable. What was missing is the academic superstructure.
The framework should be mathematical and explain which kinds of items exist and how everything fits together."
Start with this before DSQ examples / tests (they then become applications of the framework). Explain bottom-up, ONE concept per
answer, with ONE concrete example each, and visuals instead of tables where possible.
Honest starting point (user asked, 20:49): granules were INFERRED by Claude from item texts (by mechanism) → they are a reasoned
hypothesis, not an established result. 'Granule = latent variable' is NOT written in the xlsx; it is an interpretive lens from
measurement theory that fits the data (several items per granule) but is unproven (would need real response data, e.g. factor
analysis). The user's earlier phrase 'granules = core concepts items are composed of' is correct (= M: item → set of granules); only
the inference 'therefore every item is unique within its instrument' does not follow logically (M need not be injective) – Claude
should have flagged that earlier. The framework must state these levels explicitly: rule (xlsx) / hypothesis (granules) / lens
(latent variable) / evidence (tests).
Seed (measurement theory, to be developed WITH the user, not dumped):
- Latent variable θ (= granule): what we want to know, not directly observable. A user score s is a direct self-rating of θ.
- Item x_i = indicator of θ: x_i ≈ f_i(θ | facet conditions c_i) + noise. Facets = the conditions c (where, when, how much, activity).
- Scale = aggregate of several items (e.g. mean) → less noise; studies report scales. Comparison happens at scale level.
- Item types to define: (1) single indicator; (2) parallel/redundant indicators of the same θ (RAND-36 Energy/fatigue 23/27/29/31);
  (3) graded/threshold items on one θ at different difficulty (walking one block / several / one mile – Guttman/IRT logic);
  (4) composite items loading on several θ (FUNCAP 32 conversation → CG2, CG4, CG7, SN2); (5) global items (overall health);
  (6) change items (PGIC, RAND-36 2: Δθ, not θ); (7) measured, not rated (device values).
- Mapping user score → instrument: s ↔ θ (+ asked facets) ↔ set of items / scale; coverage of a scale = share of its items reached.
- Uniqueness: item identifiable within instrument by θ + all facets (DSQ 95/104, RAND-36 30/36, FUNCAP 55/55), not needed for
  comparison because studies use scales; the user score value already carries what graded items split up.

**Next steps, in this order.**
1. DSQ ambiguity: show the user (as HTML/visual, not xlsx) which DSQ items collide on granule + tree-asked facets, so he can judge
   whether they are 'same variable' (fine, like RAND-36) or a real loss of precision. Also compute the real ceiling per instrument.
2. Run the tests:
   - T1 (tree): blind Haiku walks the tree with each item as score name, all instruments, sharper multi-pick instruction, 3 runs.
     Pilot RAND-36 done: 32/35 exact, 3 construct-level (files in t1/: make_blind.py, score.py, report HTML, results/steps CSV).
   - Test 3 (mapping M): blind 2nd annotator gets granule definitions + items, assigns granules; compare with M; the user reviews only
     the disagreements on an HTML page.
3. Mapping candidates found so far: R36-5 groceries → PF2 + PF3 [outing]? R36-7 one flight → PF2 + PF3 (like R36-6)? R36-16 ambiguous
   (PF4 vs PF3). PF3 label reads like 'intense sport' → rename e.g. 'Lifting, carrying, physical effort'.
4. Still open from step 14: decision 3 (multi-select: max 3 components, unweighted, pooled at construct level only – proposed, not
   confirmed), decision 4 ('None of these fits – keep it personal' on every node). Then step 15 JSON export.
5. Small: flatten note row 2 in merged tabs (frozen header rows take most of the screen); SVG text copy-paste jumps (DOM order).


## Goal
Users of an N-of-1 app track self-defined check-in scores. Each score is mapped via a short
question tree (granule) to official instrument items, so data can be analysed across users.
End products:
1. **mecfs-criteria.xlsx** – clean data structure (items, granules, trees)
2. **SVG** – granules + question tree (written at the very end, from scratch)
3. **JSON tree** for the app – question/answer algorithm, as easy as possible for ME/CFS patients
Not perfect is fine: usability beats completeness.

## Review doc
Review notes for the user (to check / compromises / app hints), maintained after each section:
https://claude.ai/artifact/SQaiv43rWkNTFnsKhjtHwb (Claude Doc; edit with the Docs connector).

## Files
- `mecfs-criteria.xlsx` – single source of truth
  - `Method`: frozen rules + "Rules added after pilots" (scale, direction, measure type,
    cross-user analysis, facets, granules without items, asked facets, mapping by mechanism)
  - `Instrument items`: 401 rows, all items verbatim (DSQ-1, DSQ-2, RAND-36, FUNCAP55/27,
    Bell [German], PGIC). Column "Other version" links DSQ-1 ↔ DSQ-2 and FUNCAP55 ↔ FUNCAP27.
  - `Sec Sleep`, `Sec Cognition`, `Sec Energy`, `Sec Pain`, `Sec Sensory`, `Sec Function`, `Sec Autonomic`, `Sec Neuromuscular`, `Sec Temperature`, `Sec Immune`, `Sec Mood`, `Sec Global`: done sections
  - grey tabs = LEGACY (paraphrased, predate the method); ignore
- `Constructs`, `All granules`, `All items`, `Full tree`: merged tabs (steps 12/14), generated by `merge.py` – never edit by hand
- `sections.py` – section generator. Runs on the xlsx alone, idempotent:
  `python3 sections.py mecfs-criteria.xlsx`. New section = add one dict to `SECTIONS`.
- `merge.py` (+ `merge_parse.py`) – step 12 merge. Reads only the Sec tabs, idempotent, run AFTER sections.py:
  `python3 sections.py mecfs-criteria.xlsx && python3 merge.py mecfs-criteria.xlsx`, then recalc (0 errors).
  Asserts: no UNHANDLED item, every Sec item exists in `Instrument items`, every redirect resolves,
  every leaf matches ≥ 1 item (except MO4 and 'measured' leaves). Also writes `mecfs-criteria_merge.json`
  (granules + full tree incl. matched items) = input for svg_tree.py and step 13.
- `svg_tree.py` – `python3 svg_tree.py mecfs-criteria_merge.json mecfs-tree.svg` (tree cards + granule register)
- `dsqmap.py` – DSQ-1 → DSQ-2 item map (used by sections.py)
- `build_items.py` – only needed to rebuild `Instrument items` from the PDFs (normally not).

## Workflow per section
1. Collect all items of the section from `Instrument items` (all instruments).
2. Granulize: granule = one sensation or ability, no location/trigger/timing (→ facets).
3. Assign by mechanism, not by instrument heading. Composite items map to all granules.
4. Hand off items that belong elsewhere ("Boundary" table, `→ Section`).
5. Build tree: category + 1–2 questions, plain language, "a mix" → multi-select/composite.
6. Write findings; check formulas (recalc, 0 errors).

## Conventions
- Granule IDs: SL, CG, EN, PN, SN, PF, AU, NM, NE, IM, MO, GL + number. Node IDs prefixed (CG-N1 …), root N0.
- DSQ-2 is primary (item IDs DSQ2-n), DSQ-1 shown as "Other version".
- Leaves only from verbatim items. After any leaf the app asks the direction
  ("Is a high value good or bad?").

## Status
| # | Section | Status |
|---|---|---|
| 1 | Sleep | done (SL1–6) |
| 2 | Cognition | done (CG1–9) |
| 3 | Energy / PEM | done (EN1–5) |
| 4 | Pain | done (PN1–4) |
| 5 | Sensory & vision | done (SN1–5) |
| 6 | Physical function (FUNCAP A–D, F; RAND-36 PF/RP) | done (PF1–5) |
| 7 | Autonomic (incl. GI + urinary) | done (AU1–8) |
| 7b | Neuromuscular | done (NM1–4) |
| 8 | Neuroendocrine & temperature | done (NE1–8) |
| 9 | Immune | done (IM1–6) |
| 10 | Mood (RAND-36 EWB/RE) | done (MO1–4) |
| 11 | Global (Bell, PGIC, RAND-36 GH/SF) | done (GL1–4) |
| 12 | Merge → full tree, dedupe, SVG | done (merge.py, svg_tree.py) |
| 13 | Study repository (58 LC/ME-CFS trials, outcome constructs) | done → `LC_MECFS_outcome_repository.xlsx` |
| 14 | Construct layer + tree rebuild + SVG | 1 + 2 done (constructs, polarity); **next: decisions 3–4** |
| 15 | JSON export for the app (incl. polarity, "none fits") | open |
| 16 | Prompt for Claude Code: replace stub tree in the app | open |
Decided: gastrointestinal + urinary are part of 7 (AU5–8); neuromuscular is its own section 7b (prefix NM).

## Items already handed off
None left: every section 1–11 is done; boundary rows point to existing granules.

## Merge (step 12) – done Oct 2026
- Coverage columns (Sec tabs + All granules) now include Bell and PGIC.
- Dedupe: 6 items in two tabs (DSQ2-15, -18, -70; F55-32, -52; R36-33) → union of granules/facets in `All items`.
- `All items`: 247 outcome items (DSQ-2, F55, R36, Bell as 1 item, PGIC): 197 mapped, 11 excluded,
  39 not an outcome / stem, 0 unhandled. 68 granules, only MO4 without item.
- Tree: N0 = 8 areas + 'Several of these areas' (multi-select, walk each branch). SN, NM, AU, NE, IM under
  'Other body symptoms' (BD-N1). Max 4 questions to a leaf. 93 leaves.
- Redirects resolved: leaf stores target granule + 'Same leaf as'. '→ EN' (mentally exhausted) → EN3.
- 'Measured, not rated' leaves added in sections.py: AU-N2 heart rate from watch/sensor (AU3), NE-N4 weight from
  scale (NE7); granule only, 0 items.
- Asked-facet matching (merge.py `match`): same value, 'unspecified', or item carries none of the node's asked
  facets → match. 'activity' strict.

## Step 13 – JSON export (next)
- Source: `mecfs-criteria_merge.json` (tree rows with node/parent/q/a/to/g/facet/flags/items). Build nested JSON:
  node → question + options; option → child node | leaf {granules, facets, items, flags} | multi-select.
- Direction question after every leaf; multi-select at N0 walks each chosen branch.
- Open user decisions that may change the tree: see review doc, section 'Merge' (type 'Prüfen').

## Decided (Oct 2026)
- DSQ2-75 → EN2 (fatigability; PEM = 76/77; consistent with DSQ-1 17).
- DSQ2-79 → CG3 only (rate, not formulation; CG7 dropped). Motor check done in NM: stays CG3.
- PGIC stem: "Since you started '<protocol name>', how has your overall condition changed?
  (Think of your symptoms, your energy and what you can manage day to day.)" – set in
  `Instrument items` and `build_items.py`.

## Function notes
- New facet 'activity' (self-care, housework, outing, exercise), ASKED in Function tree (rule in `Method`).
- `sections.py`: FUNCAP27 equivalent is now filled automatically from `Instrument items` notes.

## Autonomic notes
- 'After standing' items mapped to their sensation + trigger: standing (69 → AU3, 70 → SN4, 71 → AU2); AU1 = DSQ2-90 only.
- AU8 bladder: asked facet (urgency / night / general).
- Wearable heart rate has no DSQ leaf; AU3 only as nearest granule → flag 'measured, not rated' at merge.


## Open decisions
- User still to review the "Rules added after pilots" in `Method` (incl. 4 merge rules added in step 12).
- DSQ2-2 (body weight, demographic) as item for the measured-weight leaf NE7? (review doc)
- Review-doc comment: periodic questionnaires monthly or tied to protocol blocks? (unanswered)
- FUNCAP license: courtesy email to authors; Bell terms unverified.

## Step 14 part 1 – done (1 Nov 2026)
- Decision 1 confirmed incl.: MO3 home = Daily functioning, also reachable under Mood (double path, must stay visible in SVG);
  PF1/AU1 wording split (PF1 'How long I can sit or stand before I must lie down', AU1 'How unwell I get when sitting or standing upright');
  SN6 smell/taste ≠ IM6 (perception vs intolerance).
- `merge.py`: `CONSTRUCTS` (10: GLO FAT PEM COG SLP PAI CAR FUN MOO BOD) + construct patches on the section trees (full tree only;
  Sec tabs unchanged except SN6 + wording). N0 = 10 constructs + 'Several'. PEM = direct leaf EN4 at N0. AU-N2 = construct node CAR
  (+ AU4, + general); AU-N1 removed, AU-N3/N4 directly under BD-N1. New PF-N4 (PF4 / MO3 / GL4). GL3 removed from tree (periodic).
- Construct-level leaves ('… in general': COG, SLP, MOO, CAR; 'Something else' BOD): store construct only, no items.
- Double paths: generic rule in merge.py – one home leaf per mapping (inside its construct, asserted), others 'Same leaf as' with identical
  items. 11 second-path leaves (MO3, GL4, EN3/4/5, EN2, PN1 ×3, IM4, IM6).
- New tab `Constructs` (study counts from LC_MECFS_outcome_repository.xlsx, read by merge.py); `Construct` column in All granules (O)
  and Full tree (N, + Area O); JSON now has `constructs`, granule `construct`, tree `construct`/`area`.
- SVG: N0 construct chips, '↗ node' (second path) / '⇄ node' (home), white chip = construct level, register grouped by construct.
- Numbers: 69 granules, 101 leaves, max 4 questions, recalc 0 errors.
- Review doc not yet updated for step 14 (do it when 3–4 are decided).

## Step 14 decision 2 – polarity, done (1 Nov 2026)
- User: direction is set in the app independently of the tree, default higher = better; may be changed after the tree, but is
  normally fixed at mapping time → static label pair per leaf in JSON, app picks the side.
- merge.py: POL_GOOD / POL_NEUTRAL / BIPOLAR dicts. Types: bipolar (EN1, MO1, MO2, IM5 + 'Sleep/Mood in general') → label per direction,
  no question; good (CG1–8, SN4, SN5, PF1–3, PF5, GL1) / bad (rest) → confirm 'So a high value means less of this?' only on mismatch
  (No = flip direction); neutral (EN5, device leaves) → never asked, sign basis 'more'.
- NE7 deliberately NOT bipolar (loss/gain are not good/bad; already two 'bad' leaves + neutral device leaf).
- Sign: +1 if high = healthier, −1 otherwise. Direction flipped later → sign flips, confirm again on a new mismatch.
- Post-leaf direction question removed (Method 'Direction' marked superseded). Full tree cols P–S, All granules P–R, JSON
  `polarity`, `label_high_better`, `label_high_worse`, `confirm_if`, top-level `confirm_question`. SVG glyphs ± ▲ ▼ ○.
- Leaves: 72 bad, 19 good, 6 bipolar, 4 neutral.

## SVG markup rework (1 Nov 2026, user feedback)
- User found ⇄/↗ + dashed chips counter-intuitive (same leaf looked like different things) and right-aligned chips hard to pair with text.
- Now: chip LEFT in a per-card chip column, zebra rows, '›' = leads to next card, 'multi' = multi-select. Chip = polarity glyph + granule
  only (facet is in the answer text). Same leaf = identical chip everywhere + small grey line 'also via: <other click path>'.
- Legend = one row of real sample chips (End point · Polarity · Same leaf, other way in), no prose.
- Same granule → same answer text on both paths: EN5 'How much I did (activity / energy used)', MO3 'How much my emotions limit my work
  or daily tasks' (patched in merge.py).
- One text per leaf (user: consistency matters for presenting): merge.py copies the home leaf's answer text to every other path.
  Home texts made self-contained (HOME_TEXT): pain regions 'Muscle pain', 'Headache' …; EN-N2 'How fast my body tires' / 'How fast my mind
  tires' (question now 'Which one does …'); EN4 at N0 'How bad my crashes are after doing too much' (ordinal, not binary).
- Polarity glyphs ▲▼± stay in the SVG (user decision); ± = both phrasings exist, so no confirm question.
- Self-care items (F55-2..5, F55-7, R36-12) and the 'Washing, dressing, toilet' leaf: PF3 removed → PF1 only (user: PF3 = force/sport, would
  become too general). Housework keeps PF1 + PF3.
- IMPORTANT for working with the user: he does NOT read the xlsx. The xlsx is the ground truth for the scripts; to convey it, use other media
  (SVG, HTML review pages, concrete examples). Explain bottom-up with ONE concrete example.
- Open: T1 pilot RAND-36 (Haiku, blind) 32/35 exact, files in t1/. Next ideas: T1 all instruments (sharper multi-pick prompt);
  Test 3 = blind 2nd annotator checks the mapping M, user reviews only disagreements; flatten note row in merged tabs (freeze panes).
- User found the construct/section split hard to grasp at first: explain bottom-up with a concrete click example before notation.

## Step 14 – Construct layer (decided direction, Nov 2026)
Why: studies mostly report coarse constructs (fatigue 40/58 studies, cognition 25, QoL 22, daily functioning 21,
mood 21, pain 19, sleep 19), often with ad hoc scales. The tree's middle level should equal these constructs so a
user who stops early still has a study-comparable value; granules stay the finest level below.

Proposed middle level (to confirm first):
| # | Construct | Granules |
|---|---|---|
| 1 | Fatigue / energy | EN1, EN2, EN3 |
| 2 | Crash / PEM | EN4 |
| 3 | Brain fog / thinking | CG1–CG9 |
| 4 | Sleep | SL1–SL6 |
| 5 | Pain (incl. head, chest) | PN1–PN4 |
| 6 | Mood | MO1, MO2, MO4 |
| 7 | Heart, circulation, breathing | AU1–AU4 |
| 8 | Daily functioning | PF1–PF5, EN5, MO3, GL4 |
| 9 | Overall health | GL1, GL2 |
| 10 | Other body symptoms | SN, NM, AU5–AU8, NE, IM |
- GL3 (global change) NOT in the check-in tree: delta question → periodic questionnaires.
- Symptom burden = computed index over 1–7, not a node.
- New granules: smell/taste (under Sensory, 4 studies); "other" catch-all leaf under 10 (cough, skin, hair loss).

Open decisions for step 14:
1. ~~Confirm the table above~~ → done (part 1).
2. ~~Polarity~~ → done (see above). Original proposal: two-pole granules (EN1, MO1, MO2, NE7, IM5) get `goodPole` + `labelGood`/`labelBad`; app shows the label
   matching the user's direction (set before mapping); store sign (+1/−1) per mapping. Unipolar granules (pain …):
   if user sets higher = better → one confirm question ("So a high value means less pain?").
   Post-leaf direction question becomes redundant.
3. Multi-select: a score may span constructs ("several areas") – define how many and how stored (composite).
4. Every node needs "None of these fits – keep it personal" (e.g. "Thirst" fits nowhere).

Implementation of 1: done via CONSTRUCTS in merge.py. Decisions 2–4 still open; 4 ('None fits') is a tree change in merge.py
(add option per node), 2 needs `goodPole`/labels per granule (sections.py granule tuple or a POLARITY dict in merge.py).

## App status (Nov 2026)
Check-in configuration redesign implemented by Claude Code (Swift, PulseKit tests pass). Mapping flow uses a stub
`MappingTreeProvider`; sharing opt-in "Share for research" in Settings (off by default). Observed UX issue: stub
option "Feeling drained or exhausted" confused a user with higher = better → solved by decision 2 above.

## Files for the next chat
mecfs-criteria.xlsx, LC_MECFS_outcome_repository.xlsx, sections.py, merge.py, merge_parse.py, svg_tree.py, dsqmap.py,
HANDOFF.md, t1/ (make_blind.py, score.py, run_rand36_haiku.json; report + CSVs are regenerated by score.py).
Pipeline: sections.py → merge.py → recalc → svg_tree.py; T1: make_blind.py <merge.json> <xlsx> <instrument> <out.json>, agent run,
score.py <blind.json> <run.json> <merge.json> <out.html> <label>. Not needed: build_items.py (only rebuilds items from PDFs), *_merge.json and *.svg (regenerated).
Review doc: https://claude.ai/artifact/SQaiv43rWkNTFnsKhjtHwb
