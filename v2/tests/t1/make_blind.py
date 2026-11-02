"""T1: build the blind tree (no granule IDs, neutral node IDs, no multi-select options) + item set for one instrument.
usage: make_blind.py <merge.json> <instrument: DSQ | RAND-36 | FUNCAP> <out.json>"""
import json, sys
D = json.load(open(sys.argv[1])); INST = sys.argv[2]; OUT = sys.argv[3]
nodes = []
for r in D["tree"]:
    if r["node"] not in nodes: nodes.append(r["node"])
QID = {n: f"Q{i:02d}" for i, n in enumerate(nodes, 1)}
lines, key = [], {}
for n in nodes:
    rows = [r for r in D["tree"] if r["node"] == n and r["to"] != "multi-select"]
    q = next(r["q"] for r in D["tree"] if r["node"] == n and r["q"]).replace("'<score name>'", "the score")
    lines.append(f"[{QID[n]}] {q}")
    for k, r in enumerate(rows, 1):
        dest = f"→ {QID[r['to']]}" if r["to"] in QID else "→ END"
        lines.append(f"   {k}. {r['a']}  {dest}")
        key[f"{QID[n]}.{k}"] = dict(node=n, a=r["a"], to=r["to"], g=r["g"], facet=r["facet"], construct=r["construct"], flags=r["flags"])
    lines.append("")
items = [dict(id=r["Item ID"], text=r["Item (verbatim)"], expected=r["Granule(s)"], facets=r["Facets"])
         for r in D["items"] if r["Instrument"] == INST and r["Status"] == "mapped"]
json.dump(dict(blind="\n".join(lines), key=key, items=items, qid=QID), open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(nodes), "nodes", len(key), "options", len(items), "items", len("\n".join(lines)), "chars")
