"""Shared measurement-model logic on top of <xlsx>_merge.json (written by merge.py).

Used by build_explorer.py and build_poster.py, so the explorer, the poster numbers and THEORY.md
examples all come from the same ground truth (the Sec tabs of mecfs-criteria.xlsx).

Terms (see THEORY.md):
  item i     -> granules M(i) + full facets c_i
  leaf l     -> granules G_l + asked facets (projection pi_A)
  drawer     -> equivalence class of items hit by exactly the same set of (home) leaves
  facet type -> 'wert' (position on the theta axis), 'format' (how it is asked), 'kontext' (condition)
"""
import json, re
from collections import defaultdict

# Facet type by facet key. Heuristic: some single values deviate (e.g. 'load: bending' is closer to context).
FACET_TYPE = {
    "load": "wert",
    "measure": "format", "pole": "format", "anchor": "format", "zeitraum": "format",
    "region": "kontext", "trigger": "kontext", "timing": "kontext", "modality": "kontext",
    "activity": "kontext", "quality": "kontext", "type": "kontext", "load type": "kontext",
}
INSTRUMENTS = ["DSQ", "RAND-36", "FUNCAP", "Bell", "PGIC"]
DRAWER_INSTRUMENTS = ["DSQ", "RAND-36", "FUNCAP"]


def ftype(key):
    return FACET_TYPE.get(key, "kontext")


def parse_facets(s):
    out = []
    for p in str(s or "").split(";"):
        p = p.strip()
        if p:
            k, _, v = p.partition(":")
            out.append([k.strip(), v.strip()])
    return out


def leaf_granules(g):
    return [x.strip() for x in re.sub(r"\[.*?\]", "", g or "").split(",") if x.strip()]


def load(path):
    D = json.load(open(path, encoding="utf-8"))
    items = []
    for r in D["items"]:
        items.append(dict(
            id=r["Item ID"], inst=r["Instrument"], text=r["Item (verbatim)"], resp=r["Response format"],
            g=[x.strip() for x in str(r["Granule(s)"] or "").split(",") if x.strip()],
            f=parse_facets(r["Facets"]), status=r["Status"], comp=r["Composite?"],
            mt=r["Measure type"], tf=r["Timeframe"], other=r["Other version"]))
    into = defaultdict(list)
    for t in D["tree"]:
        if t["to"] and t["to"] not in ("leaf", "multi-select"):
            into[t["to"]].append(t)

    def path(t):
        p, n = [t["a"]], t["node"]
        for _ in range(10):
            if n == "N0" or not into.get(n): break
            par = into[n][0]; p.insert(0, par["a"]); n = par["node"]
        return p

    leaves = []
    for k, t in enumerate(D["tree"]):
        if t["to"] == "leaf":
            leaves.append(dict(id=f"L{k}", node=t["node"], a=t["a"], g=t["g"], gl=leaf_granules(t["g"]), facet=t["facet"],
                               flags=t["flags"], same=t["same"], items=[x for x in t["items"].split(", ") if x],
                               construct=t["construct"], pol=t["polarity"], path=path(t)))
    return dict(constructs=D["constructs"], granules=D["granules"], leaves=leaves, items=items)


def facets_with_timeframe(i):
    f = [list(x) for x in i["f"]]
    if i["tf"] and i["tf"] != "—":
        f.append(["zeitraum", i["tf"]])
    return f


def drawers(M, inst):
    """Equivalence classes of mapped items of one instrument under 'hit by the same home leaves'."""
    home = [l for l in M["leaves"] if not l["same"]]
    hit = defaultdict(list)
    for l in home:
        for i in l["items"]:
            hit[i].append(l["id"])
    cls = defaultdict(list)
    for i in M["items"]:
        if i["inst"] == inst and i["status"] == "mapped":
            cls["|".join(sorted(hit[i["id"]])) or "-"].append(i)
    out = []
    for key, its in cls.items():
        keys = []
        for i in its:
            for k, _ in facets_with_timeframe(i):
                if k not in keys: keys.append(k)
        diff = [k for k in keys
                if len({" / ".join(v for kk, v in facets_with_timeframe(i) if kk == k) or "—" for i in its}) > 1]
        types = {ftype(k) for k in diff}
        verdict = "kontext" if "kontext" in types else "wert" if "wert" in types else "format" if "format" in types else "parallel"
        out.append(dict(key=key, items=its, diff=diff, verdict=verdict,
                        gdiff=len({",".join(sorted(i["g"])) for i in its}) > 1,
                        leaves=[] if key == "-" else key.split("|")))
    out.sort(key=lambda d: -len(d["items"]))
    return out


def resolution(M, inst):
    """|items| >= |distinct (granules, all facets)| >= |drawers|  (the information chain of the tree)."""
    its = [i for i in M["items"] if i["inst"] == inst and i["status"] == "mapped"]
    full = {(frozenset(i["g"]), frozenset(tuple(f) for f in i["f"])) for i in its}
    ds = drawers(M, inst)
    multi = [d for d in ds if len(d["items"]) > 1]
    by = {v: sum(d["verdict"] == v for d in multi) for v in ("kontext", "wert", "format", "parallel")}
    return dict(items=len(its), full=len(full), drawers=len(ds), multi=len(multi), **by)


def partitions(M, inst):
    """Three nested partitions of the mapped items of one instrument (see THEORY.md §5):
    E0 = items, E1 = same granules + same facets (annotation), E2 = same leaves (drawers).
    Returns the losses: e1 = E1 groups with > 1 item (lost by the annotation),
    e2 = drawers holding > 1 E1 group (lost by the tree), each as a list of E1 groups."""
    its = [i for i in M["items"] if i["inst"] == inst and i["status"] == "mapped"]
    key1 = lambda i: (tuple(sorted(i["g"])), tuple(sorted(tuple(f) for f in i["f"])))
    g1 = defaultdict(list)
    for i in its: g1[key1(i)].append(i)
    e2 = []
    for d in drawers(M, inst):
        groups = []
        for i in d["items"]:
            for g in groups:
                if key1(g[0]) == key1(i): g.append(i); break
            else: groups.append([i])
        assert all(len(g1[key1(g[0])]) == len(g) for g in groups), "partitions not nested"
        if len(groups) > 1: e2.append(dict(drawer=d, groups=groups))
    return dict(n0=len(its), n1=len(g1), n2=len(drawers(M, inst)),
                e1=[g for g in g1.values() if len(g) > 1], e2=e2)


ITEM_TYPES = ["einzeln", "parallel", "gestuft", "kontext", "composite", "global", "änderung"]


def item_types(M, inst):
    """Item type per mapped item of one instrument (THEORY.md §2.7). Rule, in this order:
    änderung (GL3) > global (GL1/GL2) > composite (> 1 granule) > relation to the other items of the same drawer
    with the same granules: none -> einzeln; differ by a context facet -> kontext (variant, lost if not asked);
    by a value facet -> gestuft; only by format or not at all -> parallel."""
    out = {}
    for d in drawers(M, inst):
        for i in d["items"]:
            g = set(i["g"])
            if "GL3" in g: out[i["id"]] = "änderung"; continue
            if g & {"GL1", "GL2"}: out[i["id"]] = "global"; continue
            if len(g) > 1: out[i["id"]] = "composite"; continue
            peers = [j for j in d["items"] if j is not i and set(j["g"]) == g]
            if not peers: out[i["id"]] = "einzeln"; continue
            mine = {k: v for k, v in facets_with_timeframe(i)}
            types = set()
            for j in peers:
                theirs = {k: v for k, v in facets_with_timeframe(j)}
                types |= {ftype(k) for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k)}
            out[i["id"]] = "kontext" if "kontext" in types else "gestuft" if "wert" in types else "parallel"
    return out


def profile(M, inst):
    """Numbers for the instrument characterisation: items, granules, items per granule, drawers, type counts, measure types."""
    from collections import Counter
    its = [i for i in M["items"] if i["inst"] == inst and i["status"] == "mapped"]
    gs = Counter(g for i in its for g in i["g"])
    t = item_types(M, inst) if inst in DRAWER_INSTRUMENTS else {}
    if not t:
        for i in its:
            g = set(i["g"]); t[i["id"]] = "änderung" if "GL3" in g else "global" if g & {"GL1", "GL2"} else "einzeln"
    return dict(items=len(its), granules=len(gs), per_granule=(len(its) / len(gs)) if gs else 0,
                max_granule=gs.most_common(1)[0] if gs else None,
                drawers=len(drawers(M, inst)) if inst in DRAWER_INSTRUMENTS else len(its),
                types=Counter(t.values()), mt=Counter(i["mt"] for i in its), comp=sum(len(i["g"]) > 1 for i in its))
