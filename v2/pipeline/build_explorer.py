"""Build the self-contained mapping explorer (one HTML file) from <xlsx>_merge.json.
usage: build_explorer.py <merge.json> <out.html>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model

src, out = sys.argv[1:3]
M = model.load(src)
data = dict(constructs=M["constructs"], granules=M["granules"], leaves=M["leaves"],
            items=[{k: i[k] for k in ("id", "inst", "text", "resp", "g", "f", "status", "comp", "mt", "tf")} for i in M["items"]],
            drawers={inst: [dict(items=[i["id"] for i in d["items"]], diff=d["diff"], gdiff=d["gdiff"], verdict=d["verdict"], leaves=d["leaves"])
                            for d in model.drawers(M, inst)] for inst in model.DRAWER_INSTRUMENTS},
            resolution={inst: model.resolution(M, inst) for inst in model.DRAWER_INSTRUMENTS},
            losses={inst: (lambda P: dict(n0=P["n0"], n1=P["n1"], n2=P["n2"], e1=[[i["id"] for i in g] for g in P["e1"]],
                                          e2=[dict(leaves=x["drawer"]["leaves"], verdict=x["drawer"]["verdict"],
                                                   groups=[[i["id"] for i in g] for g in x["groups"]]) for x in P["e2"]]))(model.partitions(M, inst))
                    for inst in model.DRAWER_INSTRUMENTS})
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "explorer_template.html"), encoding="utf-8").read()
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
open(out, "w", encoding="utf-8").write(tpl.replace("__DATA__", blob))
print("explorer:", out, {k: v["drawers"] for k, v in data["resolution"].items()}, "drawers")
