"""Render the merged tree + granule register as one SVG (from <xlsx>_merge.json written by merge.py)."""
import json, sys, textwrap, re
from html import escape

D = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
SEC_COL = {"Global": "#5B6C8F", "Energy": "#C0662B", "Cognition": "#7A5BA6", "Sleep": "#3F6FB0", "Pain": "#B8434A",
           "Sensory": "#2F8F8A", "Neuromuscular": "#8A6D3B", "Autonomic": "#B0487E", "Temperature": "#D08A1F",
           "Immune": "#4C8A3F", "Function": "#3D7D9E", "Mood": "#8C5A7A", "—": "#555555"}
PRE2SEC = {g["id"].rstrip("0123456789"): g["section"] for g in D["granules"]}
CONS = {c["id"]: c for c in D.get("constructs", [])}

CW, GAP, PAD = 380, 70, 24
LH, CH_HEAD, FS = 17, 22, 12
LV = 14  # line height of the small 'also via' hint
WRAP_Q = 50

nodes = {}
for r in D["tree"]:
    n = nodes.setdefault(r["node"], dict(id=r["node"], level=r["level"], q=None, opts=[], section=r["section"]))
    if r["q"]: n["q"] = r["q"]
    n["opts"].append(r)

# ---- double paths: same leaf reached from several places → each place names the other click path(s)
PARENT = {r["to"]: (r["node"], r["a"]) for r in D["tree"] if r["to"] in nodes}


def short(a):
    a = re.sub(r"\s*\([^)]*\)", "", a).strip()
    if len(a) <= 40: return a
    return a[:38].rsplit(" ", 1)[0].rstrip(" ,/") + " …"  # cut at a word boundary


def click_path(r):
    path, nid = [short(r["a"])], r["node"]
    while nid in PARENT:
        nid, a = PARENT[nid]; path.insert(0, short(a))
    return " › ".join(path)


GROUP = {}
for r in D["tree"]:
    if r["to"] == "leaf":
        key = r["same"] if r["same"] else f'{r["node"]} · {r["a"]}'
        GROUP.setdefault(key, []).append(r)
VIA = {}
for rs in GROUP.values():
    if len(rs) > 1:
        for r in rs:
            VIA[id(r)] = "also via: " + "  |  ".join(click_path(o) for o in rs if o is not r)


def lines(t, w): return textwrap.wrap(t, w) or [""]


import re
GLYPH = {"bipolar": "±", "good": "▲", "bad": "▼", "neutral": "○"}


def chip(o):
    """Chip = where the path ends: polarity glyph + granule (+ asked facet). Construct ID only at N0."""
    if o["to"] != "leaf":
        return o["area"] if o["node"] == "N0" and o["to"] != "multi-select" else None
    g = o["g"]; ids = ", ".join(re.findall(r"[A-Z]{2}\d+", g))
    lab = g if "construct level" in (o["flags"] or "") else ids  # facet is already in the answer text
    return GLYPH.get(o.get("polarity"), "") + " " + lab


def chip_w(lab): return 0 if not lab else int(6.4 * len(lab)) + 12


def chipcol(n): return max([chip_w(chip(o)) for o in n["opts"]] + [34])


def text_x(n): return 10 + (chipcol(n) + 8 if chipcol(n) else 8)


def wrap_n(n): return max(16, int((CW - text_x(n) - 14) / 6.4))


def facet_txt(o):
    return "facet · " + o["facet"].replace(": ", " = ") if o["to"] == "leaf" and o.get("facet") else ""


def opt_lines(n, o):
    t = lines(o["a"], wrap_n(n))
    v = ([facet_txt(o)] if facet_txt(o) else []) + (lines(VIA[id(o)], int((CW - text_x(n) - 14) / 5.6)) if id(o) in VIA else [])
    return t, v


def opt_h(n, o):
    t, v = opt_lines(n, o)
    return len(t) * LH + len(v) * LV + 5


def card_h(n):
    return CH_HEAD + len(lines(n["q"] or "", WRAP_Q)) * LH + 6 + sum(opt_h(n, o) for o in n["opts"]) + 6


col_y = {}
pos = {}  # node -> (x, y, h, option row spans)


def place(nid, min_y):
    n = nodes[nid]; lvl = n["level"]
    x = PAD + lvl * (CW + GAP)
    y = max(min_y, col_y.get(lvl, PAD + 60))
    h = card_h(n)
    rows = []; yy = y + CH_HEAD + len(lines(n["q"] or "", WRAP_Q)) * LH + 6
    for o in n["opts"]:
        hh = opt_h(n, o); rows.append((yy, yy + hh)); yy += hh
    pos[nid] = (x, y, h, rows)
    col_y[lvl] = y + h + 14
    for o, (a, b) in zip(n["opts"], rows):
        if o["to"] in nodes:
            place(o["to"], a - CH_HEAD)


place("N0", PAD + 118)
W = PAD + 4 * (CW + GAP) + 560
H_tree = max(y + h for x, y, h, _ in pos.values()) + PAD

svg = []
# links first (under cards): from the end of the option's first line to the child card header
for nid, n in nodes.items():
    x, y, h, rows = pos[nid]
    for o, (a, b) in zip(n["opts"], rows):
        if o["to"] in pos:
            cx, cy, _, _ = pos[o["to"]]
            y1 = a + LH / 2; y2 = cy + CH_HEAD / 2
            x1 = x + CW; x2 = cx
            svg.append(f'<path d="M{x1},{y1} C{x1+GAP/2},{y1} {x2-GAP/2},{y2} {x2},{y2}" class="link"/>')

for nid, n in nodes.items():
    x, y, h, rows = pos[nid]
    col = SEC_COL.get(n["section"], "#555")
    title = nid if nid != "N0" else "N0 · start"
    svg.append(f'<g><rect x="{x}" y="{y}" width="{CW}" height="{h}" rx="8" class="card" style="stroke:{col}"/>')
    svg.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH_HEAD}" rx="8" style="fill:{col}"/>'
               f'<rect x="{x}" y="{y+CH_HEAD-8}" width="{CW}" height="8" style="fill:{col}"/>')
    svg.append(f'<text x="{x+10}" y="{y+15}" class="hd">{escape(title)}  ·  {escape(n["section"] if n["section"]!="—" else "areas")}</text>')
    qy = y + CH_HEAD + LH - 3
    for ln in lines(n["q"] or "", WRAP_Q):
        svg.append(f'<text x="{x+10}" y="{qy}" class="q">{escape(ln)}</text>'); qy += LH
    tx = x + text_x(n)
    for k, (o, (a, b)) in enumerate(zip(n["opts"], rows)):
        if k % 2: svg.append(f'<rect x="{x+1}" y="{a}" width="{CW-2}" height="{b-a}" class="zebra"/>')
        t, v = opt_lines(n, o)
        mix = o["to"] == "multi-select"
        ty = a + LH - 4
        for ln in t:
            svg.append(f'<text x="{tx}" y="{ty}" class="{"mix" if mix else "a"}">{escape(ln)}</text>'); ty += LH
        for ln in v:
            svg.append(f'<text x="{tx}" y="{ty-2}" class="{"fac" if ln.startswith("facet ·") else "via"}">{escape(ln)}</text>'); ty += LV
        lab = chip(o); cx0 = x + 10
        if o["to"] == "leaf":
            w = chip_w(lab)
            if "construct level" in (o["flags"] or ""):
                st, fc = 'class="cl"', "#333"
            else:
                gc = SEC_COL.get(PRE2SEC.get(o["g"][:2], "—"), "#555")
                meas = "measured" in (o["flags"] or "")
                st, fc = f'style="fill:{gc};{"fill-opacity:.35" if meas else ""}"', ("#222" if meas else "#fff")
            svg.append(f'<rect x="{cx0}" y="{a+2}" width="{w}" height="{LH-2}" rx="4" {st}/>'
                       f'<text x="{cx0+6}" y="{a+LH-4}" class="chip" style="fill:{fc}">{escape(lab)}</text>')
        elif lab:
            w = chip_w(lab)
            svg.append(f'<rect x="{cx0}" y="{a+2}" width="{w}" height="{LH-2}" rx="4" class="cn"/>'
                       f'<text x="{cx0+6}" y="{a+LH-4}" class="chip" style="fill:#333">{escape(lab)}</text>')
        elif mix:
            svg.append(f'<text x="{cx0+2}" y="{a+LH-4}" class="mixr">multi</text>')
        else:
            svg.append(f'<text x="{tx-14}" y="{a+LH-4}" class="go">›</text>')
    svg.append("</g>")

# granule register (right)
gx = PAD + 4 * (CW + GAP); gy = PAD + 140
svg.append(f'<text x="{gx}" y="{gy-14}" class="h2">Constructs → granules ({len(D["granules"])})</text>')
GROUPS = [(c["id"], f'{c["id"]} · {c["name"]}  ({c["studies"]} of 58 studies)', [g for g in D["granules"] if g["construct"] == c["id"]])
          for c in D["constructs"]] + [("—", "Not in the check-in tree (periodic only)", [g for g in D["granules"] if not g["construct"]])]
cur = None
for cid, head, gs in GROUPS:
    gy += 8
    svg.append(f'<text x="{gx}" y="{gy+12}" class="gs">{escape(head)}</text>'); gy += LH + 2
    for g in gs:
        col = SEC_COL[g["section"]]
        svg.append(f'<rect x="{gx}" y="{gy}" width="40" height="{LH-2}" rx="4" style="fill:{col}"/>'
                   f'<text x="{gx+5}" y="{gy+LH-5}" class="chip">{g["id"]}</text>'
                   f'<text x="{gx+48}" y="{gy+LH-5}" class="gn">{escape(g["name"])}</text>')
        gy += LH
        for ln in lines(re.sub(r"\s*\([^)]*facet[^)]*\)|;[^;.]*facet[^;.]*", "", g.get("definition") or ""), 78):
            svg.append(f'<text x="{gx+48}" y="{gy+9}" class="gd">{escape(ln)}</text>'); gy += 13
        gy += 5
H = max(H_tree, gy + PAD + 60)

# ---- legend: three groups of real sample chips + 1–3 word labels, one row
def lchip(x, y, lab, kind, col="#5B6C8F"):
    w = chip_w(lab)
    if kind == "via":
        x0 = x + w + 6
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{LH-2}" rx="4" style="fill:#C0662B"/>'
                f'<text x="{x+6}" y="{y+LH-6}" class="chip">{escape(lab)}</text>'), w
    st = {"leaf": f'style="fill:{col}"', "con": 'class="cn"', "cl": 'class="cl"',
          "dev": f'style="fill:{col};fill-opacity:.35"',
          "same": f'style="fill:{col};fill-opacity:.55;stroke-dasharray:3 2;stroke:#222;stroke-width:1.2"'}[kind]
    dark = kind != "leaf"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{LH-2}" rx="4" {st}/>'
            f'<text x="{x+6}" y="{y+LH-6}" class="chip" style="{"fill:#222" if dark else ""}">{escape(lab)}</text>'), w


LG = [("End point (chip)", [("GL2", "leaf", "granule"), ("FAT", "con", "construct (N0)"), ("COG", "cl", "construct only"),
                             ("AU3", "dev", "measured by device")]),
      ("Polarity", [("±", "leaf", "label flips"), ("▲", "leaf", "ability"), ("▼", "leaf", "problem"), ("○", "leaf", "neutral")]),
      ("Same leaf, other way in", [("EN4", "via", "also via: Tiredness and energy › …")])]
ly = PAD + 34; lx = PAD; parts = []
for head, items in LG:
    gx0 = lx
    parts.append(f'<text x="{lx}" y="{ly}" class="lh">{head.upper()}</text>')
    cx = lx
    for lab, kind, txt in items:
        svgc, w = lchip(cx, ly + 8, lab, kind)
        parts.append(svgc)
        parts.append(f'<text x="{cx+w+6}" y="{ly+8+LH-6}" class="{"via" if kind == "via" else "lt"}">{escape(txt)}</text>')
        cx += w + 12 + int(6.3 * len(txt)) + 18
    lx = cx + 26
    parts.append(f'<line x1="{lx-22}" y1="{ly-10}" x2="{lx-22}" y2="{ly+LH+8}" class="sep"/>')
parts.pop()  # no separator after the last group
DEFS = [("Granule", "WHAT is felt or done – one sensation or ability (e.g. PN1 pain)."),
        ("Facet", "UNDER WHICH CIRCUMSTANCE – where, when, how much, which activity (e.g. region = head). Only some facets are asked in the tree; they appear as “facet · …” under the answer.")]
dy = ly + LH + 30
for k, (t, d) in enumerate(DEFS):
    parts.append(f'<text x="{PAD}" y="{dy + k*16}" class="dl"><tspan class="dk">{t}</tspan>  {escape(d)}</text>')
legend = (f'<text x="{PAD}" y="{PAD+8}" class="h1">ME/CFS symptom mapping – question tree and granules</text>' + "".join(parts))
style = """<style>
text{font-family:Inter,Helvetica,Arial,sans-serif}
.card{fill:#fff;stroke-width:1.4}.link{fill:none;stroke:#9aa0a6;stroke-width:1.2}
.hd{font-size:11px;font-weight:700;fill:#fff;letter-spacing:.3px}.q{font-size:12px;font-weight:600;fill:#222}
.a{font-size:12px;fill:#333}.mix{font-size:12px;fill:#777;font-style:italic}.mixr{font-size:10px;fill:#999}
.dot{fill:#bbb}.cl{fill:#fff;stroke:#333;stroke-width:1}.cn{fill:#e4e4e0}.chip{font-size:10.5px;font-weight:700;fill:#fff;font-family:Menlo,Consolas,monospace}
.h1{font-size:20px;font-weight:700;fill:#111}.h2{font-size:15px;font-weight:700;fill:#111}.lg{font-size:12px;fill:#555}
.gs{font-size:12px;font-weight:700;fill:#222}.lh{font-size:10px;font-weight:700;fill:#888;letter-spacing:.8px}.lt{font-size:12px;fill:#444}.sep{stroke:#ddd;stroke-width:1}.via{font-size:10.5px;fill:#8a8a8a;font-style:italic}.zebra{fill:#f4f4f1}.fac{font-size:10.5px;fill:#5d7f9e}.gd{font-size:10.5px;fill:#999}.dl{font-size:11.5px;fill:#777}.dk{font-weight:700;fill:#444}.go{font-size:14px;font-weight:700;fill:#aaa}.gn{font-size:12px;fill:#333}
</style>"""
open(OUT, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                     f'<rect width="100%" height="100%" fill="#fafaf8"/>{style}{legend}{"".join(svg)}</svg>')
print(W, H, len(nodes))
