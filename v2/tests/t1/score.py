"""T1 scoring + HTML report. usage: score.py <blind.json> <run.json> <merge.json> <out.html> <label>"""
import json, sys, csv, re, os
from html import escape
B = json.load(open(sys.argv[1])); RUN = json.load(open(sys.argv[2])); M = json.load(open(sys.argv[3]))
OUT, LABEL = sys.argv[4], sys.argv[5]
KEY, ITEMS = B["key"], {i["id"]: i for i in B["items"]}
QTEXT = {}
for line in B["blind"].splitlines():
    m = re.match(r"\[(Q\d+)\] (.*)", line)
    if m: QTEXT[m.group(1)] = m.group(2)
ROW = {(r["node"], r["a"]): r for r in M["tree"]}
CON = {g["id"]: g["construct"] for g in M["granules"]}
GNAME = {g["id"]: g["name"] for g in M["granules"]}
gids = lambda s: re.findall(r"[A-Z]{2}\d+", s or "")

res, steps_csv = [], []
for it in RUN:
    item = ITEMS[it["id"]]; exp = gids(item["expected"])
    leaves, errors, visited = [], [], set()
    for k, st in enumerate(it["steps"]):
        visited.add(st["q"])
        for p in st["picked"]:
            o = KEY.get(f'{st["q"]}.{p}')
            if not o: errors.append(f'{st["q"]}.{p} does not exist'); continue
            steps_csv.append([it["id"], item["text"], k + 1, st["q"], o["node"], QTEXT[st["q"]], p, o["a"],
                              "END" if o["to"] == "leaf" else B["qid"][o["to"]], ROW[(o["node"], o["a"])]["g"] if o["to"] == "leaf" else "", st["why"]])
            if o["to"] == "leaf":
                r = ROW[(o["node"], o["a"])]
                leaves.append(dict(a=o["a"], g=r["g"], construct=r["construct"], items=[x.strip() for x in r["items"].split(",") if x.strip()]))
            elif B["qid"][o["to"]] not in [s["q"] for s in it["steps"]]:
                errors.append(f'branch {st["q"]}.{p} → {B["qid"][o["to"]]} not followed')
    got_g = {g for l in leaves for g in gids(l["g"])}
    if any(it["id"] in l["items"] for l in leaves): v = "exact"
    elif got_g & set(exp): v = "granule"
    elif {l["construct"] for l in leaves} & {CON.get(g) for g in exp}: v = "construct"
    else: v = "miss"
    res.append(dict(id=it["id"], text=item["text"], expected=exp, leaves=leaves, verdict=v, steps=it["steps"], errors=errors,
                    multi=sum(len(s["picked"]) > 1 for s in it["steps"])))

base = os.path.splitext(OUT)[0]
num = lambda iid: (re.sub(r"[\d\-]+[a-z]?$", "", iid), int((re.findall(r"\d+", iid.split("-", 1)[-1]) or [0])[0]), iid)
steps_csv.sort(key=lambda r: (num(r[0]), r[2]))
VERDICT = {r["id"]: r["verdict"] for r in res}
with open(base + "_steps.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item id", "item text (= score name)", "verdict", "step", "question id (blind)", "tree node", "question", "picked option",
                "answer", "leads to", "granule reached", "why (agent)"])
    w.writerows([r[:2] + [VERDICT[r[0]]] + r[2:] for r in steps_csv])
with open(base + "_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item id", "item text (= score name)", "verdict", "reached granule(s)", "expected granule(s)", "click path", "steps", "multi-pick steps"])
    for r in sorted(res, key=lambda r: num(r["id"])):
        path = " › ".join(" + ".join(KEY[f'{st["q"]}.{p}']["a"] for p in st["picked"] if f'{st["q"]}.{p}' in KEY) for st in r["steps"])
        w.writerow([r["id"], r["text"], r["verdict"], ", ".join(l["g"] for l in r["leaves"]), ", ".join(r["expected"]), path, len(r["steps"]), r["multi"]])

# ------------------------------------------------------------------ HTML
VC = {"exact": ("Exact", "item reached"), "granule": ("Granule", "right granule, item filtered out by facet"),
      "construct": ("Construct", "right construct, other granule"), "miss": ("Miss", "wrong construct")}
n = len(res); cnt = {k: sum(r["verdict"] == k for r in res) for k in VC}
skipped = [i for i in B["items"] if i["id"] not in {r["id"] for r in res}]
tiles = "".join(f'<div class="tile v-{k}"><div class="num">{cnt[k]}</div><div class="lab">{VC[k][0]}</div><div class="sub">{VC[k][1]}</div></div>' for k in VC)
bar = "".join(f'<span class="seg v-{k}" style="flex:{cnt[k]}" title="{VC[k][0]}: {cnt[k]}"></span>' for k in VC if cnt[k])
order = {"miss": 0, "construct": 1, "granule": 2, "exact": 3}


def chip(g, cls=""):
    return f'<span class="chip {cls}" title="{escape(GNAME.get(g, g))}">{g}</span>'


rows = []
for r in sorted(res, key=lambda r: (order[r["verdict"]], int(re.sub(r"\D", "", r["id"]) or 0))):
    path = []
    for st in r["steps"]:
        picks = " + ".join(escape(KEY[f'{st["q"]}.{p}']["a"]) for p in st["picked"] if f'{st["q"]}.{p}' in KEY)
        path.append(f'<li><span class="q">{escape(QTEXT[st["q"]])}</span><span class="pick">{picks}</span><span class="why">{escape(st["why"])}</span></li>')
    got = "".join(chip(g, "ok" if g in r["expected"] else "") for l in r["leaves"] for g in gids(l["g"])) or \
          "".join(f'<span class="chip cl">{escape(l["g"])}</span>' for l in r["leaves"])
    exp = "".join(chip(g) for g in r["expected"])
    err = f'<div class="err">{"; ".join(map(escape, r["errors"]))}</div>' if r["errors"] else ""
    rows.append(f'''<tr class="r-{r["verdict"]}"><td class="id">{r["id"]}</td>
<td><div class="item">{escape(r["text"])}</div><details><summary>{len(r["steps"])} steps</summary><ol class="path">{"".join(path)}</ol></details>{err}</td>
<td>{got}</td><td>{exp}</td><td><span class="badge v-{r["verdict"]}">{VC[r["verdict"]][0]}</span></td></tr>''')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tree Validation T1</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fafaf8;--fg:#1d1d1b;--mut:#76766f;--line:#e6e5df;--card:#fff;
--exact:#2f7d5b;--granule:#7fa94c;--construct:#d39b2a;--miss:#c0473d}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161614;--fg:#ecebe6;--mut:#9a9a92;--line:#2c2c29;--card:#1f1f1c}}}}
:root[data-theme="dark"]{{--bg:#161614;--fg:#ecebe6;--mut:#9a9a92;--line:#2c2c29;--card:#1f1f1c}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 Inter,system-ui,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:22px;margin:0 0 4px}}.meta{{color:var(--mut);margin-bottom:24px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
.tile{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;border-top:4px solid}}
.tile .num{{font-size:30px;font-weight:700;font-variant-numeric:tabular-nums}}.tile .lab{{font-weight:600}}.tile .sub{{color:var(--mut);font-size:12px}}
.v-exact{{border-color:var(--exact)}}.v-granule{{border-color:var(--granule)}}.v-construct{{border-color:var(--construct)}}.v-miss{{border-color:var(--miss)}}
.bar{{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:16px 0 28px;gap:2px}}
.seg.v-exact{{background:var(--exact)}}.seg.v-granule{{background:var(--granule)}}.seg.v-construct{{background:var(--construct)}}.seg.v-miss{{background:var(--miss)}}
.tablewrap{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}}
table{{border-collapse:collapse;width:100%;min-width:760px}}th,td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}}
th{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600}}
td.id{{font-family:"JetBrains Mono",monospace;font-weight:700;white-space:nowrap}}
.item{{max-width:560px}}details{{margin-top:4px}}summary{{color:var(--mut);cursor:pointer;font-size:12px}}
.path{{margin:6px 0 0;padding-left:18px;font-size:12.5px}}.path li{{margin:3px 0}}
.path .q{{color:var(--mut)}}.path .pick{{font-weight:600;margin-left:6px}}.path .pick::before{{content:"→ ";color:var(--mut);font-weight:400}}
.path .why{{display:block;color:var(--mut);font-style:italic;font-size:12px}}
.chip{{display:inline-block;font:700 11px "JetBrains Mono",monospace;padding:2px 7px;border-radius:5px;background:#e9e8e2;color:#333;margin:0 4px 4px 0}}
.chip.ok{{background:var(--exact);color:#fff}}.chip.cl{{background:transparent;border:1px solid var(--mut);color:var(--fg)}}
.badge{{font-size:12px;font-weight:700;padding:3px 9px;border-radius:20px;color:#fff;white-space:nowrap}}
.badge.v-exact{{background:var(--exact)}}.badge.v-granule{{background:var(--granule)}}.badge.v-construct{{background:var(--construct)}}.badge.v-miss{{background:var(--miss)}}
.err{{color:var(--miss);font-size:12px}}.note{{color:var(--mut);font-size:12.5px;margin-top:18px}}
</style></head><body><main>
<h1>Tree validation · T1 · {escape(LABEL)}</h1>
<div class="meta">Blind agent walks the question tree with each instrument item as score name (multi-select allowed). Verdict compares the leaves it reached with the item's mapping in mecfs-criteria.xlsx. {n} items scored{f", {len(skipped)} skipped (not in check-in tree: " + ", ".join(i["id"] for i in skipped) + ")" if skipped else ""}. Multi-pick steps: {sum(r["multi"] for r in res)}.</div>
<div class="tiles">{tiles}</div><div class="bar">{bar}</div>
<div class="tablewrap"><table><thead><tr><th>Item</th><th>Item text · click path</th><th>Reached</th><th>Expected</th><th>Verdict</th></tr></thead><tbody>
{"".join(rows)}</tbody></table></div>
<div class="note">Green chip = reached granule that is also expected. Sorted: misses first. One row per item: {escape(os.path.basename(base))}_results.csv · every step: {escape(os.path.basename(base))}_steps.csv</div>
</main></body></html>'''
open(OUT, "w").write(html)
print(cnt, "skipped", [i["id"] for i in skipped])
for r in res:
    if r["verdict"] != "exact": print(r["id"], r["verdict"], r["expected"], [l["g"] for l in r["leaves"]], r["errors"])
