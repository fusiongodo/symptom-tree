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
    "activity": "kontext", "quality": "kontext", "type": "kontext",
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
