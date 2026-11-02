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
TABS = ("Constructs", "All granules", "All items", "Full tree")

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
    if ver == "FUNCAP55": return "cost of an activity (consequence 0–6)"
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

# ============================================================ 2. CONSTRUCT LAYER (step 14)
# Middle level = constructs that studies report. N0 offers the constructs; granules stay the finest level below.
# (id, construct, N0 answer shown to the user, granules, repository constructs pooled for the study count)
CONSTRUCTS = [
    ("GLO", "Overall health", "How I am overall", ["GL1", "GL2"],
     ["quality of life", "global health / severity"]),
    ("FAT", "Fatigue / energy", "Tiredness and energy", ["EN1", "EN2", "EN3"],
     ["fatigue", "cognitive fatigue", "fatigue + cognition (composite)"]),
    ("PEM", "Crash / PEM", "How bad my crashes are after doing too much", ["EN4"],
     ["post-exertional malaise", "exercise intolerance (self-report)"]),
    ("COG", "Brain fog / thinking", "Thinking and concentration (brain fog)", [f"CG{i}" for i in range(1, 10) if i != 8],
     ["cognitive dysfunction", "fatigue + cognition (composite)"]),
    ("SLP", "Sleep", "Sleep", [f"SL{i}" for i in range(1, 7)],
     ["sleep disturbance / quality", "unrefreshing sleep"]),
    ("PAI", "Pain (incl. head, chest)", "Pain (also headache, chest pain)", ["PN1", "PN2", "PN3", "PN4"],
     ["pain", "headache", "chest pain / symptoms"]),
    ("CAR", "Heart, circulation, breathing", "Heart, circulation and breathing", ["AU1", "AU2", "AU3", "AU4"],
     ["autonomic / orthostatic symptoms", "dyspnea"]),
    ("FUN", "Daily functioning", "What I can do in daily life", ["PF1", "PF2", "PF3", "PF4", "PF5", "EN5", "EN6", "MO3", "GL4"],
     ["daily functioning", "physical functioning", "social participation", "physical activity"]),
    ("MOO", "Mood", "Mood and emotions", ["MO1", "MO2", "MO4"],
     ["mood/depression", "anxiety", "psychological distress / PTSD"]),
    ("BOD", "Other body symptoms", "Other body symptoms (senses, muscles, stomach, temperature, feeling ill)", None,
     ["smell/taste", "gastrointestinal symptoms", "cough", "skin symptoms", "hair loss", "general malaise", "immune symptoms"]),
]
NOT_IN_TREE = {"GL3": "Global change is a delta question: periodic questionnaires (PGIC, RAND-36 2), not the check-in tree"}
NOT_A_NODE = [("—", "Symptom burden", "computed index over constructs 1–7, not a node", ["symptom burden (composite)"]),
              ("—", "Global change", "periodic questionnaire (GL3)", ["global impression of change / recovery"])]
BODY = ["SN", "NM", "AU", "NE", "IM"]
CON_OF = {}
for cid, _, _, gs, _ in CONSTRUCTS:
    for g in gs or []: CON_OF[g] = cid
for s in SECS:
    for g in s["granules"]:
        if g["id"] not in CON_OF and g["id"] not in NOT_IN_TREE:
            assert s["prefix"] in BODY, g["id"]
            CON_OF[g["id"]] = "BOD"
CON = {c[0]: c for c in CONSTRUCTS}
N0_TARGET = {"GLO": "GL-N1", "FAT": "EN-N1", "PEM": "EN4", "COG": "CG-N1", "SLP": "SL-N1", "PAI": "PN-N1",
             "CAR": "AU-N2", "FUN": "PF-N1", "MOO": "MO-N1", "BOD": "BD-N1"}

# ---- section trees as nodes (from the Sec tabs)
nodes = OrderedDict()  # id -> dict(q, parent, section, opts=[dict(a, to, g)])
for s in SECS:
    for t in s["tree"]:
        if t["node"] == "N0": continue
        n = nodes.setdefault(t["node"], dict(q=None, parent=t["parent"], section=s["tab"][4:], opts=[]))
        n["q"] = n["q"] or t["q"]
        n["opts"].append(dict(a=t["a"], to=t["to"], g=t["g"]))


def opt(nid, a):
    return next(o for o in nodes[nid]["opts"] if o["a"] == a)


def add(nid, a, to, g="", before=None):
    """Insert an option before 'before' (answer text), default: before the trailing multi-select options."""
    os_ = nodes[nid]["opts"]
    if before:
        i = os_.index(opt(nid, before))
    else:
        i = len(os_)
        while i and os_[i - 1]["to"] == "multi-select": i -= 1
    os_.insert(i, dict(a=a, to=to, g=g))


def gen(cid, what="general"):
    return f"{cid} (construct level{' · other' if what == 'other' else ''})"


# ---- construct-layer patches (full tree only; section trees in the Sec tabs stay as they are)
# Overall: GL3 leaves the check-in tree (periodic only); GL4 home moves to Daily functioning
nodes["GL-N1"]["opts"].remove(opt("GL-N1", "How much better or worse I am than before"))
opt("GL-N1", "How much my health limits my social life")["g"] = "GL4 (redirect)"
# Heart, circulation, breathing: AU-N2 becomes the construct node; stomach/bladder go under 'Other body symptoms'
del nodes["AU-N1"]
nodes["AU-N2"]["parent"] = "N0"
nodes["AU-N3"]["parent"] = nodes["AU-N4"]["parent"] = "BD-N1"
add("AU-N2", "Shortness of breath", "leaf", "AU4")
add("AU-N2", "Heart, circulation or breathing problems in general", "leaf", gen("CAR"))
# Daily functioning: limitation node PF-N4 = role-physical (PF4), role-emotional (MO3), social (GL4)
o = opt("PF-N1", "How much my health limits my work or daily life")
o.update(a="How much my health or emotions limit me", to="PF-N4", g="")
nodes["PF-N4"] = dict(q="Which one does '<score name>' measure?", parent="PF-N1", section="Function", opts=[
    dict(a="How much my health limits my work or daily tasks", to="leaf", g="PF4"),
    dict(a="How much my emotions limit my work or daily tasks", to="leaf", g="MO3"),
    dict(a="How much my health limits my social life", to="leaf", g="GL4"),
    dict(a="A mix of several of these", to="multi-select", g="composite")])
opt("PF-N1", "How much I did")["g"] = "EN5"  # home of EN5 is now Daily functioning
opt("EN-N1", "How much I did / how much energy I used")["g"] = "EN5 (redirect)"
opt("EN-N1", "How bad my crash is after doing too much")["g"] = "EN4 (redirect)"
# Mood: MO3 stays reachable here (second path, same leaf as PF-N4)
opt("MO-N1", "How much my emotions limit my daily life").update(g="MO3 (redirect)", a="How much my emotions limit my work or daily tasks")
# same granule → same answer text on every path (only where the context of the node does not change the meaning)
opt("PF-N1", "How much I did")["a"] = "How much I did (activity / energy used)"
opt("EN-N1", "How much I did / how much energy I used")["a"] = "How much I did (activity / energy used)"
# home leaves worded so they stand on their own (their text is copied to every other path, see 'one text per leaf')
HOME_TEXT = {
    ("PN-N2", "Muscles"): "Muscle pain", ("PN-N2", "Joints"): "Joint pain", ("PN-N2", "Head"): "Headache",
    ("PN-N2", "Eyes"): "Pain in or behind my eyes", ("PN-N2", "Chest"): "Chest pain", ("PN-N2", "Belly"): "Belly pain",
    ("PN-N2", "All over / it moves around"): "Pain all over / it moves around",
    ("EN-N2", "Something physical"): "How fast my body tires", ("EN-N2", "Thinking or concentrating"): "How fast my mind tires",
}
for (nid, a), b in HOME_TEXT.items():
    opt(nid, a)["a"] = b
nodes["EN-N2"]["q"] = "Which one does '<score name>' measure?"
add("MO-N1", "How I feel emotionally in general", "leaf", gen("MOO"))
# Construct-level leaves: user stops early, value still comparable at construct level
o = opt("CG-N1", "General brain fog / a mix of several"); o["a"] = "A mix of several of these"
add("CG-N1", "Brain fog in general", "leaf", gen("COG"))
add("SL-N1", "My sleep in general", "leaf", gen("SLP"))

# ---- N0 and BD-N1
nodes["N0"] = dict(q="Which area fits '<score name>' best?", parent="—", section="—", opts=[])
for cid, _, ans, _, _ in CONSTRUCTS:
    t = N0_TARGET[cid]
    nodes["N0"]["opts"].append(dict(a=ans, to=t, g="") if t in nodes or t == "BD-N1" else dict(a=ans, to="leaf", g=t))
nodes["N0"]["opts"].append(dict(a="Several of these areas", to="multi-select", g="composite", flags="walk each chosen branch"))
BODY_OPTS = [("Senses and vision (light, noise, seeing, smell, taste)", "SN-N1"), ("Muscles and movement", "NM-N1"),
             ("Stomach and bowel", "AU-N3"), ("Bladder", "AU-N4"),
             ("Temperature, sweating, appetite and weight", "NE-N1"),
             ("Feeling ill, infections, sensitivities to smells or chemicals", "IM-N1")]
nodes["BD-N1"] = dict(q="Which fits '<score name>' best?", parent="N0", section="—",
                      opts=[dict(a=a, to=t, g="") for a, t in BODY_OPTS]
                      + [dict(a="Something else (e.g. cough, skin, hair loss)", to="leaf", g=gen("BOD", "other")),
                         dict(a="A mix of several of these", to="multi-select", g="composite")])

# section-level redirects ('→ EN') resolved to a granule
REDIRECT_TO = {("CG-N1", "How mentally exhausted I get"): "EN3"}
FAC_RE = re.compile(r"\[([^\]]+)\]")
CL_RE = re.compile(r"^([A-Z]{3}) \(construct level")


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


WILD = ("several", "unspecified", "per check-in")  # per check-in: facet named at each check-in, mapping matches all
STRICT = {"load type"}  # context facet: items without it never match a load-type leaf


def match(leaf_g, leaf_fac, node_keys, flags):
    if "measured, not rated" in flags or any(f.startswith("construct level") for f in flags): return []
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


# ---- walk from N0: levels, area (construct of the N0 option), resolved leaves
tree = []  # [node, parent, level, question, answer, to, granule, facets, flags, same_as, section, matched, construct, area]
seen = set()


def walk(nid, level, area, parent="—"):
    assert nid not in seen, f"node reached twice: {nid}"
    seen.add(nid); n = nodes[nid]
    keys = set()
    for o in n["opts"]:
        if o["to"] == "leaf": keys |= set(leaf_parts(o["g"])[1])
    for i, o in enumerate(n["opts"]):
        ar = area or next((c for c, t in N0_TARGET.items() if t in (o["to"], o["g"])), "—")
        to, g = o["to"], o["g"]
        redir = str(to).startswith("→") or "redirect" in g
        if redir:
            to, g = "leaf", REDIRECT_TO.get((nid, o["a"])) or g.replace("(redirect)", "").strip()
        gr, fac, flags = leaf_parts(g)
        flags += [o["flags"]] if o.get("flags") else []
        if to == "leaf":
            cl = CL_RE.match(g)
            con = cl.group(1) if cl else "+".join(OrderedDict.fromkeys(CON_OF[x] for x in gr))
            gshow = g.split(" (")[0].strip() if not cl else cl.group(1)
        else:
            con, gshow = (ar if to == "multi-select" else ""), g
        tree.append([nid, parent, level, n["q"] if i == 0 else None, o["a"], to, gshow,
                     "; ".join(f"{k}: {v}" for k, v in fac.items()), ", ".join(flags), "", n["section"],
                     ", ".join(match(gr, fac, keys, flags)) if to == "leaf" else "", con, ar])
        if to in nodes: walk(to, level + 1, ar, nid)


walk("N0", 0, None)
assert seen == set(nodes), set(nodes) - seen

# ---- double paths: one home leaf per mapping, every other leaf with the same mapping = 'Same leaf as'
SEC_OF = {g["id"]: s["tab"][4:] for s in SECS for g in s["granules"]}
by_key = defaultdict(list)
for r in tree:
    if r[5] == "leaf" and granule_ids(r[6]):
        by_key[(r[6], r[7], r[8])].append(r)
for key, rs in by_key.items():
    gr = granule_ids(key[0])
    def score(r): return (r[13] == r[12]) * 2 + (r[10] == SEC_OF[gr[0]])
    home = max(rs, key=score)  # max keeps the first of equals
    assert home[13] == home[12], f"no home leaf inside its construct: {key}"
    for r in rs:
        if r is not home:
            r[9] = f"{home[0]} · {home[4]}"; r[11] = home[11]
            r[4] = home[4]  # one text per leaf: every path shows the home wording


# ---- polarity (step 14, decision 2) – direction is set before mapping (default: higher = better)
# good    = leaf text names an ability / positive state (more = healthier)
# bad     = leaf text names a problem (more = worse)
# bipolar = genuine two-pole granule: the app shows the label matching the user's direction, no confirmation
# neutral = no healthier pole (amount, device value): sign basis 'more', never confirmed
POL_GOOD = {"CG1", "CG2", "CG3", "CG4", "CG5", "CG6", "CG7", "CG8", "SN4", "SN5", "PF1", "PF2", "PF3", "PF5", "GL1"}
POL_NEUTRAL = {"EN5"}
BIPOLAR = {  # granule / construct-level leaf -> (label if high = better, label if high = worse)
    "EN1": ("How energetic I feel overall", "How tired or exhausted I feel overall"),
    "MO1": ("How calm and relaxed I feel", "How anxious or tense I feel"),
    "MO2": ("How good my mood is", "How low my mood is"),
    "IM5": ("How well I fight off infections", "How often I get infections"),
    "SLP": ("How well I sleep in general", "How badly I sleep in general"),
    "MOO": ("How well I feel emotionally in general", "How bad I feel emotionally in general"),
}
CONFIRM_Q = "So a high value means less of this?"


def polarity(g, flags):
    ids = granule_ids(g) or [g]
    if "measured" in flags: return "neutral"
    if len(ids) == 1 and ids[0] in BIPOLAR: return "bipolar"
    kinds = {"good" if x in POL_GOOD else "neutral" if x in POL_NEUTRAL else "bad" for x in ids}
    assert len(kinds) == 1, (g, kinds)  # a leaf never mixes poles
    return kinds.pop()


for r in tree:
    if r[5] != "leaf":
        r += ["", "", "", ""]; continue
    pol = polarity(r[6], r[8])
    lg, lb = BIPOLAR.get((granule_ids(r[6]) or [r[6]])[0], (r[4], r[4])) if pol == "bipolar" else (r[4], r[4])
    confirm = {"bad": "higher = better", "good": "higher = worse"}.get(pol, "never")
    r += [pol, lg, lb, confirm]
GPOL = {}
for s in SECS:
    for g in s["granules"]:
        GPOL[g["id"]] = polarity(g["id"], "")

# sanity
for r in tree:
    assert r[5] in ("leaf", "multi-select") or r[5] in nodes, r
NO_ITEM_OK = {"MO4", "SN6"}
empty = [(r[0], r[4], r[6]) for r in tree if r[5] == "leaf" and not r[11]
         and not ("measured" in r[8] or "construct level" in r[8] or set(granule_ids(r[6])) <= NO_ITEM_OK)]
assert not empty, empty
leaf_g = {g for r in tree if r[5] == "leaf" for g in granule_ids(r[6])}
missing_g = [g for g in SEC_OF if g not in leaf_g and g not in NOT_IN_TREE]
assert not missing_g, missing_g
depth = max(r[2] for r in tree) + 1

# study counts per construct (LC_MECFS_outcome_repository.xlsx, 'Outcomes' col C = construct)
import os
REPO = os.path.join(os.path.dirname(os.path.abspath(WB)), "LC_MECFS_outcome_repository.xlsx")
STUDIES = defaultdict(set)
if os.path.exists(REPO):
    for r in openpyxl.load_workbook(REPO, read_only=True)["Outcomes"].iter_rows(min_row=2, values_only=True):
        if r[0] and r[2]: STUDIES[r[2]].add(r[0])
    known = set(STUDIES)
    for c in CONSTRUCTS + NOT_A_NODE:
        assert set(c[-1]) <= known, set(c[-1]) - known


def n_studies(names): return len(set().union(*[STUDIES[x] for x in names])) if STUDIES else None

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
put(2, ["N0 offers the 10 constructs (tab 'Constructs'); granules are the finest level below. 'Other body symptoms' (BD-N1) holds senses, muscles, stomach/bladder, "
        "temperature and immune. Double paths: a mapping reachable from several places has ONE home leaf (inside its construct); every other leaf with the same "
        "mapping names it in 'Same leaf as' (dashed chip in the SVG) and stores the identical granule, facets and items. 'Construct' = construct the leaf stores; "
        "'Area' = N0 option the path started from. 'Construct level' leaves store only the construct (user stops early). 'Matched items' = granule overlap + asked-facet filter. "
        "Polarity (Method 'Polarity'): direction is set before mapping; bipolar leaves show the label matching it, unipolar leaves ask the confirm question "
        "'" + CONFIRM_Q + "' when the direction is the one in the last column."], "note")
H_T = ["Node ID", "Parent", "Level", "Question shown to the user", "Answer option", "Leads to", "Granule(s)", "Asked facet",
       "Flags", "Same leaf as", "Section", "Matched items (merge.py)", "# matched", "Construct", "Area (N0)",
       "Polarity", "Shown if high = better", "Shown if high = worse", "Confirm question if"]
put(4, H_T, "hdr")
t0 = 5
for k, row in enumerate(tree):
    rr = t0 + k
    put(rr, row[:12] + [f'=IF(L{rr}="",0,LEN(L{rr})-LEN(SUBSTITUTE(L{rr},",",""))+1)'] + row[12:])
    if row[8] and ("measured" in row[8] or "construct level" in row[8]): wt.cell(rr, 9).fill = WARN
    if row[9]: wt.cell(rr, 10).fill = WARN
t1 = t0 + len(tree) - 1
wt.freeze_panes = "A5"; wt.auto_filter.ref = f"A4:S{t1}"
for col, w in zip("ABCDEFGHIJKLMNOPQRS", [10, 9, 7, 34, 44, 12, 22, 20, 20, 26, 14, 40, 10, 10, 10, 10, 34, 34, 16]):
    wt.column_dimensions[col].width = w

# ---- All granules
wg, put = sheet("All granules", idx)
put(1, ["All granules – merged register"], "title")
put(2, ["All granules of the 12 sections. Counts are formulas over 'All items' (mapped items, incl. Bell and PGIC) and 'Full tree' (leaves). "
        "Generated by merge.py; edit the Sec tabs and rerun."], "note")
H_G = ["Granule ID", "Section", "Granule", "Plain-language definition", "User-facing wording", "Items mapped", "DSQ", "FUNCAP",
       "RAND-36", "Bell", "PGIC", "Instruments covering", "Tree leaves", "Flags", "Construct", "Polarity", "Label if high = better", "Label if high = worse"]
put(4, H_G, "hdr")
FLAGS = {"AU3": "Also nearest granule for heart rate from a watch/sensor: measured, not rated – not pooled with DSQ values",
         "NE7": "Also body weight from a scale: measured, not rated – not pooled with DSQ values",
         **NOT_IN_TREE}
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
                 f'=COUNTIFS({TG},"*"&A{rr}&"*",{TF},"leaf")', flag, CON_OF.get(g["id"], "— (periodic)"), GPOL[g["id"]],
                 *(BIPOLAR.get(g["id"], (None, None)))])
        if flag: wg.cell(rr, 14).fill = WARN
        gr_rows.append(rr); rr += 1
ge = rr - 1
rr += 1
put(rr, ["Totals"], "sec"); rr += 1
tot = [("Granules", f"=COUNTA(A{g0}:A{ge})"),
       ("Granules without any item", f'=COUNTIF(F{g0}:F{ge},0)'),
       ("Granules covered by ≥ 2 instruments", f'=COUNTIF(L{g0}:L{ge},">=2")'),
       ("Granules without a tree leaf (GL3: periodic only)", f'=COUNTIF(M{g0}:M{ge},0)'),
       ("Outcome items (rows in 'All items')", f"=COUNTA('All items'!A{r0}:A{r1})"),
       ("… mapped", f"=COUNTIF('All items'!J{r0}:J{r1},\"mapped\")"),
       ("… composite (≥ 2 granules)", f"=COUNTIF('All items'!N{r0}:N{r1},\"yes\")"),
       ("… excluded", f"=COUNTIF('All items'!J{r0}:J{r1},\"excluded\")"),
       ("… not an outcome (demographic, history, exclusion, attribution) or stem", f"=COUNTIF('All items'!J{r0}:J{r1},\"not an outcome*\")+COUNTIF('All items'!J{r0}:J{r1},\"stem*\")"),
       ("… UNHANDLED (must be 0)", f"=COUNTIF('All items'!J{r0}:J{r1},\"UNHANDLED\")"),
       ("Tree leaves", f"=COUNTIF('Full tree'!F{t0}:F{t1},\"leaf\")"),
       ("Leaves without matched items (MO4, SN6, measured, construct level)", f"=COUNTIFS('Full tree'!F{t0}:F{t1},\"leaf\",'Full tree'!M{t0}:M{t1},0)"),
       ("Leaves on a second path ('Same leaf as')", f"=COUNTIFS('Full tree'!F{t0}:F{t1},\"leaf\",'Full tree'!J{t0}:J{t1},\"?*\")"),
       ("Max. questions to a leaf (excl. confirm question)", f"=MAX('Full tree'!C{t0}:C{t1})+1"),
       ("Granules bipolar / good / bad / neutral", f'=COUNTIF(P{g0}:P{ge},"bipolar")&" / "&COUNTIF(P{g0}:P{ge},"good")&" / "&COUNTIF(P{g0}:P{ge},"bad")&" / "&COUNTIF(P{g0}:P{ge},"neutral")')]
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
    "• Facet matching for asked facets: an item matches if it carries the same value, the value 'unspecified', or none of the node's asked facets. Exception 'load type' (strict, cost node EN6): only items with that load type match; 'per check-in' and 'unspecified' match all.",
    "• Step 14 – construct layer: N0 = 10 constructs that studies report (fatigue 40/58 studies, cognition 25, …; tab 'Constructs'). Energy splits into Fatigue (EN1–3), Crash/PEM (EN4, direct leaf at N0) and Daily functioning (EN5). AU1–4 form 'Heart, circulation and breathing' (AU-N2 moved to N0); stomach and bladder sit directly under 'Other body symptoms'.",
    "• Step 14 – double paths: MO3 (emotional role limitation) has its home in Daily functioning (PF-N4, with PF4 role-physical and GL4 social) and stays reachable under Mood. Same pattern for GL4 (Overall), EN4/EN5 (Tiredness and energy). The home leaf is always inside the granule's construct; asserted in merge.py.",
    "• Step 14 – polarity: direction is set before mapping (default higher = better). 6 bipolar leaf types (EN1, MO1, MO2, IM5 + sleep/mood in general) show the matching label; unipolar leaves (good = ability, bad = problem) ask '" + CONFIRM_Q + "' only on a mismatch. NE7 is NOT bipolar: its poles (loss/gain) are not good/bad and are already split into two 'bad' leaves; weight and heart rate from devices are 'neutral' (sign basis 'more').",
    "• Step 14 – construct-level leaves ('… in general': brain fog, sleep, mood, heart/circulation/breathing; 'Something else' under Other body symptoms) store only the construct: comparable with study constructs, never pooled with item values. GL3 left the check-in tree (periodic questionnaires).",
]
for f in FINDINGS:
    put(rr, [f], "note"); rr += 1
wg.freeze_panes = "B5"
for col, w in zip("ABCDEFGHIJKLMNOPQR", [11, 15, 26, 46, 32, 9, 7, 8, 8, 7, 7, 10, 8, 40, 10, 10, 30, 30]):
    wg.column_dimensions[col].width = w

# ---- Method rules + Overview pointer
m = wb["Method"]
for k, v in [
    ("Merge (step 12)", "Tabs 'All granules', 'All items', 'Full tree' are generated by merge.py from the Sec tabs and never edited by hand. Items listed in several sections: granules and facets = union."),
    ("Tree grouping", "N0 offers the 10 constructs (tab 'Constructs') + 'several areas' (multi-select, each chosen branch is walked). Senses, muscles, stomach/bladder, temperature and immune sit under 'Other body symptoms' (BD-N1)."),
    ("Construct layer", "Each granule belongs to exactly one construct (= what studies report). The full tree is generated in merge.py: section trees from the Sec tabs + construct patches. Construct-level leaves store only the construct, never pooled with item values."),
    ("Direction", "Superseded in step 14 by 'Polarity': no post-leaf direction question any more."),
    ("Polarity", "Replaces 'Direction' (post-leaf question). The score's direction is set before mapping (default higher = better). Per leaf: bipolar → show label matching the direction; good/bad → if direction mismatches the named pole, ask once 'So a high value means less of this?' (No = flip direction); neutral → never asked. Stored sign: +1 if a high value = healthier, −1 otherwise (neutral: +1 = more). If the user later flips the direction, the sign flips and the confirm question is asked again whenever a new mismatch arises."),
    ("Double paths", "A mapping may be reachable from several places for usability (e.g. MO3 under Daily functioning and Mood). Exactly one home leaf, inside the granule's construct; all others are 'Same leaf as' and store the identical mapping."),
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
# ---- Constructs
wc, put = sheet("Constructs", idx)
put(1, ["Constructs – middle level of the tree (step 14)"], "title")
put(2, ["Constructs = what LC/ME-CFS studies report (LC_MECFS_outcome_repository.xlsx, 58 studies). N0 offers them; a user who stops at construct level still has a "
        "study-comparable value. Counts are formulas over 'All granules' (col O) and 'Full tree' (cols F, N); '# studies' = distinct studies over the pooled repository "
        "constructs, computed by merge.py. Generated by merge.py – edit CONSTRUCTS there."], "note")
put(4, ["Construct ID", "Construct", "N0 answer (user-facing)", "Granules", "# granules", "# leaves storing it", "# studies (of 58)",
        "Repository constructs pooled", "Note"], "hdr")
NOTE_C = {"PEM": "Direct leaf at N0 (one granule)", "FUN": "MO3 also reachable under Mood, GL4 under Overall, EN5 and the EN6 cost node (load type) also under Tiredness (same leaves)",
          "BOD": "Senses, muscles, stomach/bowel, bladder, temperature, immune + 'Something else' catch-all",
          "GLO": "Quality of life pooled here (QoL scales rate health as a whole); GL3 change → periodic"}
GA = f"'All granules'!$O${g0}:$O${ge}"; TN = f"'Full tree'!$N${t0}:$N${t1}"
rr = 5
for cid, name, ans, _, repo in CONSTRUCTS:
    gs = [g for g in CON_OF if CON_OF[g] == cid]
    put(rr, [cid, name, ans, ", ".join(gs), f'=COUNTIF({GA},A{rr})', f'=COUNTIFS({TN},A{rr},{TF},"leaf")',
             n_studies(repo), "; ".join(repo), NOTE_C.get(cid, "")]); rr += 1
c1 = rr - 1; rr += 1
put(rr, ["Not a tree node"], "sec"); rr += 1
for cid, name, why, repo in NOT_A_NODE:
    put(rr, [cid, name, why, "GL3" if "GL3" in why else "", None, None, n_studies(repo), "; ".join(repo), ""]); rr += 1
rr += 1
put(rr, ["Check: granules with a construct (+ GL3 periodic = register)", None, None, None, f"=SUM(E5:E{c1})+1"], "body"); rr += 1
put(rr, ["Check: granules in register", None, None, None, f"=COUNTA('All granules'!A{g0}:A{ge})"], "body")
wc.freeze_panes = "B5"
for col, w in zip("ABCDEFGHI", [11, 26, 40, 44, 10, 12, 12, 50, 50]):
    wc.column_dimensions[col].width = w

for n in TABS: wb._sheets.remove(wb[n])
pos = wb.sheetnames.index("Sec Global") + 1
wb._sheets[pos:pos] = [ws_ for ws_ in (wc, wg, wi, wt)]
wb.save(WB)

# ---- JSON dump for SVG / later app export
json.dump(dict(constructs=[dict(id=c[0], name=c[1], label=c[2], granules=[g for g in CON_OF if CON_OF[g] == c[0]], studies=n_studies(c[4]))
                           for c in CONSTRUCTS],
               granules=[dict(id=g["id"], section=s["tab"][4:], name=g["name"], wording=g["wording"], definition=g["definition"], construct=CON_OF.get(g["id"]), polarity=GPOL[g["id"]])
                         for s in SECS for g in s["granules"]],
               tree=[dict(zip(["node", "parent", "level", "q", "a", "to", "g", "facet", "flags", "same", "section", "items", "construct", "area",
                               "polarity", "label_high_better", "label_high_worse", "confirm_if"], r)) for r in tree],
               items=[{**dict(zip(H_I, r)), "Composite?": "yes" if r[9] == "mapped" and "," in (r[8] or "") else ""} for r in rows],
               confirm_question=CONFIRM_Q),
          open(WB.replace(".xlsx", "_merge.json"), "w"), ensure_ascii=False, indent=1)
from collections import Counter
print("items", len(rows), Counter(r[9].split(" (")[0] for r in rows))
print("tree rows", len(tree), "leaves", sum(r[5] == "leaf" for r in tree), "depth", depth,
      "same-as", sum(bool(r[9]) for r in tree), "constructs", {c[0]: n_studies(c[4]) for c in CONSTRUCTS})
