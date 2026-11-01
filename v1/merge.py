"""Step 12 – merge all 'Sec *' tabs into three tabs: 'All granules', 'All items', 'Full tree'.

Runs on the xlsx alone, idempotent, after sections.py:
    python3 sections.py mecfs-criteria.xlsx && python3 merge.py mecfs-criteria.xlsx
"""
import re, sys, copy, json
from collections import OrderedDict, defaultdict
import openpyxl
from openpyxl.styles import Alignment, PatternFill
from merge_parse import parse, granule_ids

WB = sys.argv[1]
SECS = parse(WB)
wb = openpyxl.load_workbook(WB)
BYPRE = {s["prefix"]: s for s in SECS}
src = wb["Sec Sleep"]
ST = {k: (copy.copy(src[c].font), copy.copy(src[c].fill)) for k, c in
      dict(title="A1", note="A2", sec="A4", hdr="A5", body="B6").items()}
WARN = PatternFill("solid", fgColor="FFFCE8B2")
TABS = ("All granules", "All items", "Full tree")

# ============================================================ 1. ITEMS (dedupe)
PRE = {"DSQ-2": "DSQ2", "FUNCAP55": "F55", "RAND-36 v1": "R36"}
INST = {"DSQ-2": "DSQ", "FUNCAP55": "FUNCAP", "RAND-36 v1": "RAND-36"}
NOT_OUTCOME = ("demographic", "history", "exclusion", "attribution")


def norm_key(k):
    if k.startswith("BELL-"): return "BELL"
    return k


def expand(key):
    """'DSQ2-120a–d' -> [DSQ2-120a..d]; 'R36-17–19' -> [R36-17..19]; 'R36-20, 32' -> both."""
    pre, rest = key.split("-", 1)
    out = []
    for part in re.split(r",\s*", rest):
        m = re.match(r"^(\d+)([a-z])–([a-z])$", part)
        n = re.match(r"^(\d+)–(\d+)$", part)
        if m:
            out += [f"{pre}-{m.group(1)}{chr(c)}" for c in range(ord(m.group(2)), ord(m.group(3)) + 1)]
        elif n:
            out += [f"{pre}-{i}" for i in range(int(n.group(1)), int(n.group(2)) + 1)]
        else:
            out.append(f"{pre}-{part}")
    return out


occ = OrderedDict()  # key -> list of (prefix, item dict)
for s in SECS:
    for it in s["items"]:
        occ.setdefault(norm_key(it["item"]), []).append((s["prefix"], it))
bnd = defaultdict(list)
for s in SECS:
    for b in s["boundary"]:
        for k in expand(b["item"]) if not b["item"].startswith("BELL") else ["BELL"]:
            bnd[k].append((s["prefix"], b))


def union(seq):
    return list(OrderedDict.fromkeys(x for x in seq if x))


def facet_union(strs):
    segs = []
    for s_ in strs:
        segs += [x.strip() for x in (s_ or "").split(";")]
    return "; ".join(union(segs))


def measure_type(ver, rf, sec):
    if ver == "DSQ-2":
        return "symptom: frequency + severity" if (rf or "").startswith("Frequency") else "DSQ other (binary / categorical / hours)"
    if ver == "FUNCAP55": return "capacity: cost (consequence)"
    if ver == "RAND-36 v1":
        if sec.startswith(("Physical functioning", "Role")): return "limitation"
        if "Energy" in sec or "Emotional" in sec: return "frequency (time)"
        if sec in ("Pain", "Social functioning"): return "severity / extent"
        return "global rating"
    return ""


rows = []
ITEMS = list(wb["Instrument items"].iter_rows(min_row=2, values_only=True))
for r in ITEMS:
    ver = r[1]
    if ver not in PRE: continue
    key = f"{PRE[ver]}-{r[2]}"
    o = occ.get(key, [])
    gr = union(g for _, it in o for g in granule_ids(it["granules"]))
    listed = union([BYPRE[p]["tab"][4:] for p, _ in o] + [f"{BYPRE[p]['tab'][4:]} ({b['goes']})" for p, b in bnd.get(key, [])])
    other = r[12] if ver == "DSQ-2" else None
    if ver == "FUNCAP55":
        m = re.search(r"Same as FUNCAP27 item (\d+)", r[11] or "")
        other = f"F27: {m.group(1)}" if m else None
    note = "; ".join(union(it["note"] for _, it in o))
    if gr:
        status = "mapped"
    elif any(b["goes"] == "excluded" for _, b in bnd.get(key, [])):
        status = "excluded"; note = "; ".join(union(b["why"] for _, b in bnd[key] if b["goes"] == "excluded"))
    elif key == "DSQ2-119":
        status = "stem only"; note = "Sub-items 119a–d mapped (EN5)"
    elif (r[6] or "").startswith(NOT_OUTCOME):
        status = f"not an outcome ({r[6].split(' ')[0]})"
        if key == "DSQ2-2": note = "Body weight; candidate item for a measured weight score (NE7), see review notes"
    else:
        status = "UNHANDLED"
    rows.append([key, INST[ver], ver, other, r[4], r[6], r[8], r[7], ", ".join(gr), status,
                 BYPRE[re.match(r"[A-Z]+", gr[0]).group()]["tab"][4:] if gr else None,
                 ", ".join(listed), facet_union(it["facets"] for _, it in o), None,
                 measure_type(ver, r[7], r[3] or ""), note])

# Bell (one item, 11 levels) and PGIC
for key, inst, ver in (("BELL", "Bell", "Bell CFIDS Disability Scale"), ("PGIC-1", "PGIC", "PGIC (full 7-point, own wording)")):
    o = occ[key]
    lv = [r for r in ITEMS if r[1] == ver]
    text = f"Single item, {len(lv)} levels 100–0 (see 'Instrument items')" if inst == "Bell" else lv[0][4]
    gr = union(g for _, it in o for g in granule_ids(it["granules"]))
    rows.append([key, inst, ver, None, text, lv[0][6], lv[0][8], lv[0][7], ", ".join(gr), "mapped",
                 BYPRE[re.match(r"[A-Z]+", gr[0]).group()]["tab"][4:],
                 ", ".join(union([BYPRE[p]["tab"][4:] for p, _ in o] + [f"{BYPRE[p]['tab'][4:]} ({b['goes']})" for p, b in bnd.get(key, [])])),
                 facet_union(it["facets"] for _, it in o), None,
                 "level 0–100 (anchored)" if inst == "Bell" else "global change (7-point)",
                 "; ".join(union(it["note"] for _, it in o))])

ALL_KEYS = {r[0] for r in rows}
missing = [k for k in occ if k not in ALL_KEYS]
assert not missing, f"Sec items not in 'Instrument items': {missing}"
unhandled = [r[0] for r in rows if r[9] == "UNHANDLED"]
assert not unhandled, unhandled
ITEM_FACETS = {r[0]: r[12] for r in rows}
ITEM_GRAN = {r[0]: granule_ids(r[8]) for r in rows}

# ============================================================ 2. TREE (merge)
BODY = ["SN", "NM", "AU", "NE", "IM"]
TOP = [  # (answer, target) – order = expected frequency of custom scores
    ("How I am overall", "GL"),
    ("Energy, exhaustion and crashes", "EN"),
    ("Thinking and concentration", "CG"),
    ("Sleep", "SL"),
    ("Pain", "PN"),
    ("Other body symptoms (senses, muscles, heart, stomach, temperature, feeling ill)", "BODY"),
    ("What I can do physically and in daily life", "PF"),
    ("Mood and emotions", "MO"),
]
BODY_LABEL = {"SN": "Senses and vision (light, noise, seeing)", "NM": "Muscles and movement",
              "AU": "Heart, breathing, stomach and bladder", "NE": "Temperature, sweating, appetite and weight",
              "IM": "Feeling ill, infections, sensitivities to smells or chemicals"}
# section-level redirects ('→ EN') resolved to one leaf
REDIRECT_TO = {("CG", "How mentally exhausted I get"): "EN3"}

FAC_RE = re.compile(r"\[([^\]]+)\]")


def leaf_parts(g):
    fac = {}
    m = FAC_RE.search(g or "")
    if m:
        for seg in m.group(1).split(";"):
            k, v = [x.strip() for x in seg.split(":", 1)]
            fac[k] = v
    flags = [f for f in re.findall(r"\(([^)]+)\)", g or "") if f != "redirect"]
    return granule_ids(g), fac, flags


def item_facets(key):
    d = defaultdict(list)
    for seg in (ITEM_FACETS.get(key) or "").split(";"):
        if ":" in seg:
            k, v = [x.strip() for x in seg.split(":", 1)]
            d[k].append(v)
    return d


WILD = ("several", "unspecified")
STRICT = {"activity"}  # context facet: items without it never match an activity leaf


def match(leaf_g, leaf_fac, node_keys, flags):
    if "measured, not rated" in flags: return []
    out = []
    for key, gr in ITEM_GRAN.items():
        if not set(gr) & set(leaf_g): continue
        if not leaf_fac:
            out.append(key); continue
        f = item_facets(key)
        spec = {k: [v for v in f[k] if "unspecified" not in v] for k in node_keys if f.get(k)}
        spec = {k: v for k, v in spec.items() if v}
        ok = True
        for k in STRICT & set(leaf_fac):
            if leaf_fac[k] not in WILD and not any(v.startswith(leaf_fac[k]) for v in f.get(k, [])): ok = False
        for k, vals in spec.items():
            lv = leaf_fac.get(k)
            if lv is None or (lv not in WILD and not any(v.startswith(lv) for v in vals)): ok = False
        if ok: out.append(key)
    return out


tree = []  # [node, parent, level, question, answer, to, granule, facets, flags, same_as, section, matched]
q0 = "Which area fits '<score name>' best?"
for i, (ans, tgt) in enumerate(TOP):
    to = "BD-N1" if tgt == "BODY" else f"{tgt}-N1"
    tree.append(["N0", "—", 0, q0 if i == 0 else None, ans, to, "", "", "", "", "—", ""])
tree.append(["N0", "—", 0, None, "Several of these areas", "multi-select", "composite", "", "walk each chosen branch", "", "—", ""])
for i, p in enumerate(BODY):
    tree.append(["BD-N1", "N0", 1, "Which fits '<score name>' best?" if i == 0 else None, BODY_LABEL[p], f"{p}-N1", "", "", "", "", "—", ""])
tree.append(["BD-N1", "N0", 1, None, "A mix of several of these", "multi-select", "composite", "", "", "", "—", ""])

home = {}  # (section, granule spec) -> (node, answer) of the leaf in its home section
for s in SECS:
    for t in s["tree"]:
        if t["to"] == "leaf" and "redirect" not in t["g"]:
            home.setdefault(t["g"].split(" (")[0].strip(), (t["node"], t["a"]))

order = [p for _, p in TOP if p != "BODY"]
order = order[:order.index("PN") + 1] + BODY + order[order.index("PN") + 1:]
for p in order:
    s = BYPRE[p]; off = 1 if p in BODY else 0
    node_keys = defaultdict(set)
    for t in s["tree"]:
        node_keys[t["node"]] |= set(leaf_parts(t["g"])[1])
    for t in s["tree"]:
        if t["node"] == "N0": continue
        par = "BD-N1" if (t["parent"] == "N0" and p in BODY) else t["parent"]
        to, g, same = t["to"], t["g"], ""
        if str(to).startswith("→") or "redirect" in g:
            tgt = REDIRECT_TO.get((p, t["a"])) or g.replace("(redirect)", "").strip()
            assert tgt in home, (p, t["a"], tgt)
            to, g, same = "leaf", tgt, "{} · {}".format(*home[tgt])
        gr, fac, flags = leaf_parts(g)
        matched = match(gr, fac, node_keys[t["node"]], flags) if to == "leaf" else []
        tree.append([t["node"], par, t["level"] + off, t["q"], t["a"], to, g.split(" (")[0].strip() if to == "leaf" else g,
                     "; ".join(f"{k}: {v}" for k, v in fac.items()), ", ".join(flags), same, s["tab"][4:], ", ".join(matched)])

# sanity: every non-root 'to' node exists, every leaf reaches ≥1 item or is a known item-less/measured leaf
nodes = {r[0] for r in tree}
for r in tree:
    assert r[5] in ("leaf", "multi-select") or r[5] in nodes, r
NO_ITEM_OK = {"MO4"}
empty = [(r[0], r[4], r[6]) for r in tree if r[5] == "leaf" and not r[11]
         and not ("measured" in r[8] or set(granule_ids(r[6])) <= NO_ITEM_OK)]
assert not empty, empty
depth = max(r[2] for r in tree) + 1

# ============================================================ 3. WRITE
for n in TABS:
    if n in wb.sheetnames: del wb[n]
idx = wb.sheetnames.index("Sec Global") + 1


def sheet(name, i):
    ws = wb.create_sheet(name, index=i)
    def put(row, vals, kind="body"):
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row, j, v); c.font, c.fill = copy.copy(ST[kind][0]), copy.copy(ST[kind][1])
            c.alignment = Alignment(vertical="top", wrap_text=True)
    return ws, put


# ---- All items
wi, put = sheet("All items", idx + 1)
put(1, ["All instrument items – merged and deduplicated"], "title")
put(2, ["One row per outcome item of the primary versions (DSQ-2, FUNCAP55, RAND-36, Bell, PGIC). DSQ-1 and FUNCAP27 in 'Other version'. "
        "Items listed in several Sec tabs are merged: granules = union, facets = union. Generated by merge.py from the Sec tabs – edit there, not here."], "note")
H_I = ["Item ID", "Instrument", "Version", "Other version", "Item (verbatim)", "Item type", "Timeframe", "Response format",
       "Granule(s)", "Status", "Primary section", "Listed in", "Facets", "Composite?", "Measure type", "Note"]
put(4, H_I, "hdr")
r0 = 5
for k, row in enumerate(rows):
    rr = r0 + k
    row[13] = f'=IF(LEN(I{rr})-LEN(SUBSTITUTE(I{rr},",",""))>0,"yes","")'
    put(rr, [v if not isinstance(v, str) or v.startswith("=") or len(v) < 32000 else v[:32000] for v in row])
    if row[9] == "mapped" and "," in row[8]: wi.cell(rr, 14).fill = WARN
r1 = r0 + len(rows) - 1
wi.freeze_panes = "B5"; wi.auto_filter.ref = f"A4:P{r1}"
for col, w in zip("ABCDEFGHIJKLMNOP", [11, 10, 14, 16, 60, 18, 16, 30, 16, 24, 16, 28, 36, 11, 24, 40]):
    wi.column_dimensions[col].width = w

# ---- Full tree
wt, put = sheet("Full tree", idx + 2)
put(1, ["Full decision tree – all sections merged"], "title")
put(2, ["N0 groups the 12 sections into 8 areas; five body-symptom sections sit one level deeper (BD-N1). Redirect leaves are resolved: 'Granule' holds the target, "
        "'Same leaf as' names the leaf in its home section, so both paths store the identical mapping. 'Matched items' = instrument items the leaf maps to "
        "(granule overlap + asked-facet filter, computed by merge.py). After any leaf the app asks the direction once."], "note")
H_T = ["Node ID", "Parent", "Level", "Question shown to the user", "Answer option", "Leads to", "Granule(s)", "Asked facet",
       "Flags", "Same leaf as", "Section", "Matched items (merge.py)", "# matched"]
put(4, H_T, "hdr")
t0 = 5
for k, row in enumerate(tree):
    rr = t0 + k
    put(rr, row + [f'=IF(L{rr}="",0,LEN(L{rr})-LEN(SUBSTITUTE(L{rr},",",""))+1)'])
    if row[8] and "measured" in row[8]: wt.cell(rr, 9).fill = WARN
t1 = t0 + len(tree) - 1
wt.freeze_panes = "A5"; wt.auto_filter.ref = f"A4:M{t1}"
for col, w in zip("ABCDEFGHIJKLM", [10, 9, 7, 34, 44, 12, 22, 20, 20, 26, 14, 40, 10]):
    wt.column_dimensions[col].width = w

# ---- All granules
wg, put = sheet("All granules", idx)
put(1, ["All granules – merged register"], "title")
put(2, ["All granules of the 12 sections. Counts are formulas over 'All items' (mapped items, incl. Bell and PGIC) and 'Full tree' (leaves). "
        "Generated by merge.py; edit the Sec tabs and rerun."], "note")
H_G = ["Granule ID", "Section", "Granule", "Plain-language definition", "User-facing wording", "Items mapped", "DSQ", "FUNCAP",
       "RAND-36", "Bell", "PGIC", "Instruments covering", "Tree leaves", "Flags"]
put(4, H_G, "hdr")
FLAGS = {"AU3": "Also nearest granule for heart rate from a watch/sensor: measured, not rated – not pooled with DSQ values",
         "NE7": "Also body weight from a scale: measured, not rated – not pooled with DSQ values"}
g0 = 5; gr_rows = []
IA = f"'All items'!$I${r0}:$I${r1}"; IB = f"'All items'!$B${r0}:$B${r1}"; TG = f"'Full tree'!$G${t0}:$G${t1}"; TF = f"'Full tree'!$F${t0}:$F${t1}"
rr = g0
for s in SECS:
    for g in s["granules"]:
        flag = FLAGS.get(g["id"], "")
        put(rr, [g["id"], s["tab"][4:], g["name"], g["definition"], g["wording"],
                 f'=COUNTIF({IA},"*"&A{rr}&"*")',
                 *[f'=COUNTIFS({IB},"{n}",{IA},"*"&A{rr}&"*")' for n in ("DSQ", "FUNCAP", "RAND-36", "Bell", "PGIC")],
                 f"=(G{rr}>0)+(H{rr}>0)+(I{rr}>0)+(J{rr}>0)+(K{rr}>0)",
                 f'=COUNTIFS({TG},"*"&A{rr}&"*",{TF},"leaf")', flag])
        if flag: wg.cell(rr, 14).fill = WARN
        gr_rows.append(rr); rr += 1
ge = rr - 1
rr += 1
put(rr, ["Totals"], "sec"); rr += 1
tot = [("Granules", f"=COUNTA(A{g0}:A{ge})"),
       ("Granules without any item", f'=COUNTIF(F{g0}:F{ge},0)'),
       ("Granules covered by ≥ 2 instruments", f'=COUNTIF(L{g0}:L{ge},">=2")'),
       ("Granules without a tree leaf", f'=COUNTIF(M{g0}:M{ge},0)'),
       ("Outcome items (rows in 'All items')", f"=COUNTA('All items'!A{r0}:A{r1})"),
       ("… mapped", f"=COUNTIF('All items'!J{r0}:J{r1},\"mapped\")"),
       ("… composite (≥ 2 granules)", f"=COUNTIF('All items'!N{r0}:N{r1},\"yes\")"),
       ("… excluded", f"=COUNTIF('All items'!J{r0}:J{r1},\"excluded\")"),
       ("… not an outcome (demographic, history, exclusion, attribution) or stem", f"=COUNTIF('All items'!J{r0}:J{r1},\"not an outcome*\")+COUNTIF('All items'!J{r0}:J{r1},\"stem*\")"),
       ("… UNHANDLED (must be 0)", f"=COUNTIF('All items'!J{r0}:J{r1},\"UNHANDLED\")"),
       ("Tree leaves", f"=COUNTIF('Full tree'!F{t0}:F{t1},\"leaf\")"),
       ("Leaves without matched items (MO4 + measured)", f"=COUNTIFS('Full tree'!F{t0}:F{t1},\"leaf\",'Full tree'!M{t0}:M{t1},0)"),
       ("Max. questions to a leaf (excl. direction)", f"=MAX('Full tree'!C{t0}:C{t1})+1")]
for lab, f in tot:
    put(rr, [lab, None, f]); rr += 1
rr += 1
put(rr, ["Merge findings"], "sec"); rr += 1
FINDINGS = [
    "• Dedupe: 6 items were listed in two Sec tabs (DSQ2-15, -18, -70; F55-32, -52; R36-33). Granules now = union, e.g. DSQ2-15 = EN4 + PN1, DSQ2-18 = EN4 + IM3, F55-32 = CG2/4/7 + SN2. No conflicting mappings, only incomplete ones.",
    "• Coverage: every outcome item of DSQ-2, FUNCAP55, RAND-36, Bell, PGIC is mapped or explicitly excluded; the rest are demographics, history, exclusion or attribution items. Bell and PGIC now count in all coverage columns (also in the Sec tabs).",
    "• N0 grouping: 12 categories → 8 areas + 'several'. Body-symptom sections with fewer expected custom scores (Senses, Muscles, Autonomic, Temperature, Immune) sit under 'Other body symptoms' (+1 question). Pain, Sleep, Cognition, Energy, Function, Mood, Overall stay top-level.",
    "• Redirects resolved: 8 redirect leaves now carry the target granule and point to the home leaf ('Same leaf as'). 'How mentally exhausted I get' (Cognition) → EN3 mental fatigability, formerly a jump to the Energy section.",
    "• Measured, not rated: heart rate from a watch/sensor (AU3) and weight from a scale (NE7) are own leaves with a flag; they map to the granule but to no instrument item (never pooled with DSQ values).",
    "• Facet matching for asked facets: an item matches if it carries the same value, the value 'unspecified', or none of the node's asked facets. Exception 'activity' (strict): only items with that activity match.",
]
for f in FINDINGS:
    put(rr, [f], "note"); rr += 1
wg.freeze_panes = "B5"
for col, w in zip("ABCDEFGHIJKLMN", [11, 15, 26, 46, 32, 9, 7, 8, 8, 7, 7, 10, 8, 40]):
    wg.column_dimensions[col].width = w

# ---- Method rules + Overview pointer
m = wb["Method"]
for k, v in [
    ("Merge (step 12)", "Tabs 'All granules', 'All items', 'Full tree' are generated by merge.py from the Sec tabs and never edited by hand. Items listed in several sections: granules and facets = union."),
    ("Tree grouping", "N0 offers 8 areas + 'several areas' (multi-select, each chosen branch is walked). Five body-symptom sections sit under 'Other body symptoms' (BD-N1)."),
    ("Redirects", "A leaf reached from another section stores the same granule + facets as its home leaf ('Same leaf as'); no section-level jumps."),
    ("Measured scores", "Device or scale values (heart rate, weight) get their own leaf, flag 'measured, not rated': granule only, no instrument item, never pooled with rated items."),
]:
    hit = [c for c in m["A"] if c.value == k]
    rrm = hit[0].row if hit else m.max_row + 1
    m.cell(rrm, 1, k).font = copy.copy(m["A4"].font); m.cell(rrm, 2, v)
    m.cell(rrm, 2).alignment = Alignment(wrap_text=True, vertical="top")
ov = wb["Overview"]
if not any(str(c.value or "").startswith("Merged tabs") for c in ov["A"]):
    ov.cell(ov.max_row + 1, 1, "Merged tabs (step 12): All granules, All items, Full tree – generated by merge.py from the Sec tabs.")

# tab order: the three merged tabs directly after 'Sec Global'
for n in TABS: wb._sheets.remove(wb[n])
pos = wb.sheetnames.index("Sec Global") + 1
wb._sheets[pos:pos] = [ws_ for ws_ in (wg, wi, wt)]
wb.save(WB)

# ---- JSON dump for SVG / later app export
json.dump(dict(granules=[dict(id=g["id"], section=s["tab"][4:], name=g["name"], wording=g["wording"])
                         for s in SECS for g in s["granules"]],
               tree=[dict(zip(["node", "parent", "level", "q", "a", "to", "g", "facet", "flags", "same", "section", "items"], r)) for r in tree]),
          open(WB.replace(".xlsx", "_merge.json"), "w"), ensure_ascii=False, indent=1)
from collections import Counter
print("items", len(rows), Counter(r[9].split(" (")[0] for r in rows))
print("tree rows", len(tree), "leaves", sum(r[5] == "leaf" for r in tree), "depth", depth)
