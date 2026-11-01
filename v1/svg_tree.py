"""Render the merged tree + granule register as one SVG (from <xlsx>_merge.json written by merge.py)."""
import json, sys, textwrap
from html import escape

D = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
SEC_COL = {"Global": "#5B6C8F", "Energy": "#C0662B", "Cognition": "#7A5BA6", "Sleep": "#3F6FB0", "Pain": "#B8434A",
           "Sensory": "#2F8F8A", "Neuromuscular": "#8A6D3B", "Autonomic": "#B0487E", "Temperature": "#D08A1F",
           "Immune": "#4C8A3F", "Function": "#3D7D9E", "Mood": "#8C5A7A", "—": "#555555"}
PRE2SEC = {g["id"].rstrip("0123456789"): g["section"] for g in D["granules"]}

CW, GAP, PAD = 330, 70, 24
LH, CH_HEAD, FS = 17, 22, 12
WRAP_Q, WRAP_A = 44, 40

nodes = {}
for r in D["tree"]:
    n = nodes.setdefault(r["node"], dict(id=r["node"], level=r["level"], q=None, opts=[], section=r["section"]))
    if r["q"]: n["q"] = r["q"]
    n["opts"].append(r)


def lines(t, w): return textwrap.wrap(t, w) or [""]


import re
def chip(o):
    if o["to"] != "leaf": return None
    g = o["g"]; ids = ", ".join(re.findall(r"[A-Z]{2}\d+", g))
    m = re.search(r"\[[^:]+:\s*([^\]]+)\]", g)
    lab = ids + (" · " + m.group(1) if m else "")
    if "measured" in (o["flags"] or ""): lab = ids + " · device"
    return lab


def chip_w(lab): return 0 if not lab else int(6.4 * len(lab)) + 12


def awrap(o):
    return max(14, int((CW - 30 - chip_w(chip(o))) / 6.5))


def card_h(n):
    h = CH_HEAD + len(lines(n["q"] or "", WRAP_Q)) * LH + 6
    for o in n["opts"]:
        h += max(1, len(lines(o["a"], awrap(o)))) * LH + 4
    return h + 6


col_y = {}
pos = {}  # node -> (x, y, option row y-centres)
out = []


def place(nid, min_y):
    n = nodes[nid]; lvl = n["level"]
    x = PAD + lvl * (CW + GAP)
    y = max(min_y, col_y.get(lvl, PAD + 60))
    h = card_h(n)
    rows = []; yy = y + CH_HEAD + len(lines(n["q"] or "", WRAP_Q)) * LH + 6
    for o in n["opts"]:
        k = max(1, len(lines(o["a"], awrap(o))))
        rows.append((yy, yy + k * LH + 4)); yy += k * LH + 4
    pos[nid] = (x, y, h, rows)
    col_y[lvl] = y + h + 14
    for o, (a, b) in zip(n["opts"], rows):
        if o["to"] in nodes:
            place(o["to"], a - CH_HEAD)
    # keep parent column below its deepest child to avoid crossing links
    return


place("N0", PAD + 60)
W = PAD + 4 * (CW + GAP) + 520
H_tree = max(y + h for x, y, h, _ in pos.values()) + PAD


def sec_of(n):
    s = n["section"]
    if s == "—": return "—"
    return s


svg = []
# links first (under cards)
for nid, n in nodes.items():
    x, y, h, rows = pos[nid]
    for o, (a, b) in zip(n["opts"], rows):
        if o["to"] in pos:
            cx, cy, _, _ = pos[o["to"]]
            y1 = (a + b) / 2; y2 = cy + CH_HEAD / 2
            x1 = x + CW; x2 = cx
            svg.append(f'<path d="M{x1},{y1} C{x1+GAP/2},{y1} {x2-GAP/2},{y2} {x2},{y2}" class="link"/>')

for nid, n in nodes.items():
    x, y, h, rows = pos[nid]
    col = SEC_COL.get(sec_of(n), "#555")
    title = nid if nid != "N0" else "N0 · start"
    svg.append(f'<g><rect x="{x}" y="{y}" width="{CW}" height="{h}" rx="8" class="card" style="stroke:{col}"/>')
    svg.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH_HEAD}" rx="8" style="fill:{col}"/>'
               f'<rect x="{x}" y="{y+CH_HEAD-8}" width="{CW}" height="8" style="fill:{col}"/>')
    svg.append(f'<text x="{x+10}" y="{y+15}" class="hd">{escape(title)}  ·  {escape(n["section"] if n["section"]!="—" else "areas")}</text>')
    qy = y + CH_HEAD + LH - 3
    for ln in lines(n["q"] or "", WRAP_Q):
        svg.append(f'<text x="{x+10}" y="{qy}" class="q">{escape(ln)}</text>'); qy += LH
    for o, (a, b) in zip(n["opts"], rows):
        ty = a + LH - 4
        italic = o["to"] == "multi-select"
        for ln in lines(o["a"], awrap(o)):
            svg.append(f'<text x="{x+18}" y="{ty}" class="{"mix" if italic else "a"}">{escape(ln)}</text>'); ty += LH
        svg.append(f'<circle cx="{x+10}" cy="{a+LH/2+1}" r="2.6" class="dot"/>')
        if o["to"] == "leaf":
            g = o["g"]; gc = SEC_COL.get(PRE2SEC.get(g[:2], "—"), "#555")
            meas = "measured" in (o["flags"] or "")
            red = bool(o["same"])
            lab = chip(o); wpx = chip_w(lab)
            svg.append(f'<rect x="{x+CW-wpx-6}" y="{a+2}" width="{wpx}" height="{LH-2}" rx="4" '
                       f'style="fill:{gc};{"fill-opacity:.35;" if meas else ""}{"stroke-dasharray:3 2;stroke:#222;" if red else ""}"/>')
            svg.append(f'<text x="{x+CW-wpx}" y="{a+LH-4}" class="chip" style="{"fill:#333" if meas else ""}">{escape(lab)}</text>')
        elif italic:
            svg.append(f'<text x="{x+CW-8}" y="{a+LH-4}" class="mixr" text-anchor="end">multi-select</text>')
    svg.append("</g>")

# granule register (right)
gx = PAD + 4 * (CW + GAP); gy = PAD + 60
svg.append(f'<text x="{gx}" y="{gy-14}" class="h2">Granules ({len(D["granules"])})</text>')
cur = None
for g in D["granules"]:
    if g["section"] != cur:
        cur = g["section"]; gy += 8
        svg.append(f'<text x="{gx}" y="{gy+12}" class="gs" style="fill:{SEC_COL[cur]}">{escape(cur)}</text>'); gy += LH + 2
    col = SEC_COL[cur]
    svg.append(f'<rect x="{gx}" y="{gy}" width="40" height="{LH-2}" rx="4" style="fill:{col}"/>'
               f'<text x="{gx+5}" y="{gy+LH-5}" class="chip">{g["id"]}</text>'
               f'<text x="{gx+48}" y="{gy+LH-5}" class="gn">{escape(g["name"])}</text>')
    gy += LH + 1
H = max(H_tree, gy + PAD + 60)

legend = (f'<text x="{PAD}" y="{PAD+8}" class="h1">ME/CFS symptom mapping – full question tree and granules</text>'
          f'<text x="{PAD}" y="{PAD+30}" class="lg">Each card = one question. Coloured chip = leaf (granule [asked facet]). '
          f'Dashed chip = redirect into another section (same leaf as there). Pale chip = measured, not rated (no instrument item). '
          f'After any leaf the app asks: “Is a high value good or bad for you?”</text>')
style = """<style>
text{font-family:Inter,Helvetica,Arial,sans-serif}
.card{fill:#fff;stroke-width:1.4}.link{fill:none;stroke:#9aa0a6;stroke-width:1.2}
.hd{font-size:11px;font-weight:700;fill:#fff;letter-spacing:.3px}.q{font-size:12px;font-weight:600;fill:#222}
.a{font-size:12px;fill:#333}.mix{font-size:12px;fill:#777;font-style:italic}.mixr{font-size:10px;fill:#999}
.dot{fill:#bbb}.chip{font-size:10.5px;font-weight:700;fill:#fff;font-family:Menlo,Consolas,monospace}
.h1{font-size:20px;font-weight:700;fill:#111}.h2{font-size:15px;font-weight:700;fill:#111}.lg{font-size:12px;fill:#555}
.gs{font-size:12px;font-weight:700}.gn{font-size:12px;fill:#333}
</style>"""
open(OUT, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                     f'<rect width="100%" height="100%" fill="#fafaf8"/>{style}{legend}{"".join(svg)}</svg>')
print(W, H, len(nodes))
