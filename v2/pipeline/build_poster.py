"""Theory poster (Lernplakat) as one SVG. Numbers and examples come live from <xlsx>_merge.json via model.py.
usage: build_poster.py <merge.json> <out.svg>"""
import math, os, sys, datetime
from html import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model

SRC, OUT = sys.argv[1:3]
M = model.load(SRC)
I = {i["id"]: i for i in M["items"]}
G = {g["id"]: g for g in M["granules"]}
RES = {inst: model.resolution(M, inst) for inst in model.DRAWER_INSTRUMENTS}

W, H = 1680, 3800
INK, MUTED, LINE, PAPER, PANEL = "#1b2430", "#5b6876", "#cfd6de", "#eef1f4", "#ffffff"
ACC, ACC_S = "#1f5f8b", "#e1edf6"
COL = dict(wert=("#0f7a6c", "#d9f0ea"), format=("#6a5a9c", "#e9e5f5"), kontext=("#b4530b", "#fae5d2"), parallel=(ACC, ACC_S))
LAT = "#8a3f6f"   # latent variable colour
SANS = "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
MONO = "'IBM Plex Mono', Menlo, Consolas, monospace"
SERIF = "'Source Serif 4', Georgia, serif"

out = []
def add(s): out.append(s)
def T(x, y, s, size=15, fill=INK, weight=400, family=SANS, anchor="start", style=""):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" font-family="{family}" '
        f'text-anchor="{anchor}" {style}>{escape(str(s))}</text>')
def wrap(s, width, size, mono=False):
    cw = size * (0.6 if mono else 0.53)
    n = max(8, int(width / cw)); lines, cur = [], ""
    for w in str(s).split():
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines
def P(x, y, s, width, size=15, fill=INK, lh=None, weight=400, family=SANS):
    lh = lh or size * 1.42
    for k, line in enumerate(wrap(s, width, size, family == MONO)):
        T(x, y + k * lh, line, size, fill, weight, family)
    return y + len(wrap(s, width, size, family == MONO)) * lh
def R(x, y, w, h, fill=PANEL, stroke=LINE, rx=10, sw=1, dash=""):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>')
def C(x, y, r, fill="#fff", stroke=LAT, sw=2, dash=""):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash}/>')
def A(x1, y1, x2, y2, col=MUTED, sw=1.6, dash=""):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}" marker-end="url(#ar)" {dash}/>')
def L(x1, y1, x2, y2, col=LINE, sw=1, dash=""):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}" {dash}/>')
def chip(x, y, s, kind, size=12.5):
    fg, bg = COL[kind]; w = len(s) * size * 0.62 + 14
    R(x, y - size - 3, w, size + 9, bg, bg, 4); T(x + 7, y, s, size, fg, 500, MONO); return x + w + 6
def panel(x, y, w, h, num, title, sub=""):
    R(x, y, w, h, PANEL, LINE, 12)
    T(x + 26, y + 44, num, 15, ACC, 600, MONO)
    T(x + 62, y + 44, title, 25, INK, 600, SERIF)
    if sub: T(x + 26, y + 72, sub, 14.5, MUTED)
DASH = 'stroke-dasharray="6 5"'

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
add('<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,600&amp;display=swap");</style>')
add(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')
R(0, 0, W, H, PAPER, PAPER, 0)

# ================================================================ header
X0, CW = 60, 1560
T(X0, 92, "Vom Score zum Item", 58, INK, 600, SERIF)
T(X0, 132, "Ein Messmodell für den ME/CFS-Symptombaum: Fragen, Variablen, Facetten, Blätter und Schubladen", 20, MUTED)
x = X0; y = 176
T(x, y, "Status jeder Aussage:", 14, MUTED, 600); x += 160
for lab, txt in [("Regel", "steht im xlsx"), ("Hypothese", "aus Itemtexten abgeleitet"), ("Linse", "Theorie, passt, unbelegt"), ("Evidenz", "Testergebnis")]:
    R(x, y - 17, len(lab) * 8.2 + 18, 25, ACC_S, ACC_S, 5); T(x + 9, y, lab, 14, ACC, 600); x += len(lab) * 8.2 + 26
    T(x, y, txt, 14, MUTED); x += len(txt) * 7.4 + 26

# ================================================================ 1 Das Modell
y1, h1 = 220, 560
panel(X0, y1, CW, h1, "01", "Das Modell: eine Variable, viele Messungen",
      "Eine Frage ist eine Messung einer Variable unter einer Bedingung. Frage und Variable stehen in einer n:m-Beziehung.")
cx, cy = X0 + 380, y1 + 190
C(cx, cy, 58, "#f6edf3", LAT, 2.2, DASH)
T(cx, cy - 4, "θ", 34, LAT, 600, SERIF, "middle"); T(cx, cy + 22, "PF2", 13, LAT, 500, MONO, "middle")
T(cx - 78, cy - 20, "latente Variable (Granule)", 14, LAT, 600, anchor="end"); T(cx - 78, cy - 1, "„Wie weit kann ich gehen?“", 14, MUTED, anchor="end")
T(cx - 78, cy + 18, "nicht direkt beobachtbar", 14, MUTED, anchor="end")
ex = ["R36-11", "R36-9", "F55-9", "F55-11"]
SHORT = {"R36-11": "Walking one block", "R36-9": "Walking > 1 mile", "F55-9": "Walking ≈ 100 m", "F55-11": "Walking ≈ 1 km"}
bw, bh, gap = 165, 74, 22
bx0 = X0 + 40
for k, iid in enumerate(ex):
    it = I[iid]; bx = bx0 + k * (bw + gap); by = y1 + 340
    A(cx + (k - 1.5) * 26, cy + 58, bx + bw / 2, by - 4, MUTED)
    T((cx + bx + bw / 2) / 2 + (-14 if k < 2 else 8), (cy + 58 + by) / 2, f"λ", 14, MUTED, 500, SERIF)
    R(bx, by, bw, bh, "#fff", INK, 6, 1.4)
    T(bx + 10, by + 22, f"x  {iid}", 13.5, INK, 600, MONO)
    T(bx + 10, by + 42, SHORT[iid], 12.5, MUTED)
    chip(bx + 10, by + 66, it["f"][0][1][:18], "wert", 11.5)
    C(bx + bw / 2, by + bh + 46, 14, "#fff", MUTED, 1.2); T(bx + bw / 2, by + bh + 51, "ε", 14, MUTED, 400, SERIF, "middle")
    A(bx + bw / 2, by + bh + 32, bx + bw / 2, by + bh + 3, MUTED, 1.2)
T(bx0, y1 + 525, "Items: dieselbe Variable unter verschiedenen Bedingungen c_i (hier: Gehstrecke = Last).", 14, MUTED)
# score
sx, sy = X0 + 560, y1 + 120
A(cx + 58, cy - 8, sx + 160, sy + 60, ACC, 1.8)
R(sx + 160, sy + 52, 220, 78, ACC_S, ACC, 8, 1.5)
T(sx + 172, sy + 76, "s  User-Score", 14, ACC, 600, MONO); T(sx + 172, sy + 97, "„Gehstrecke heute (m)“", 13.5, INK)
T(sx + 172, sy + 117, "kennt nur π_A(c)", 13, MUTED, 400, MONO)
# formulas right
fx = X0 + 1010; fy = y1 + 120
T(fx, fy, "Die fünf Objekte", 17, INK, 600)
rows = [("θ_g", "Variable (Granule g): was wir wissen wollen"),
        ("c", "Bedingung: Facetten, Schlüssel → Wert"),
        ("i", "Item: trägt Granules M(i) und volle Facetten c_i"),
        ("S", "Skala: Aggregat über Items, das berichten Studien"),
        ("s", "User-Score: direkte Selbsteinschätzung über den Baum")]
for k, (sym, txt) in enumerate(rows):
    T(fx, fy + 34 + k * 27, sym, 15, LAT if k == 0 else INK, 600, MONO); T(fx + 52, fy + 34 + k * 27, txt, 14.5, INK)
fy += 34 + 5 * 27 + 18
R(fx - 12, fy, 552, 150, PAPER, PAPER, 8)
for k, (f, d) in enumerate([("x_i = f_i(θ, c_i) + ε_i", "Antwort auf Item i"), ("S   = (1/k) · Σ x_i", "Skala = Mittelwert"),
                            ("s   = h(θ, π_A(c)) + ε", "Score, nur gefragte Facetten")]):
    T(fx, fy + 36 + k * 44, f, 18, INK, 500, MONO); T(fx + 300, fy + 36 + k * 44, d, 13.5, MUTED)

# ================================================================ 2 Item-Typen
y2, h2 = y1 + h1 + 30, 760
panel(X0, y2, CW, h2, "02", "Sechs Item-Typen", "Die Typen unterscheiden sich in der Form von f. Mehrere Items pro Variable gibt es aus zwei Gründen: mitteln (1) oder abtasten (2).")
cw2, ch2, gx = 496, 300, 36
def card(k, title, formula, example, note):
    col, row = k % 3, k // 3
    x = X0 + 26 + col * (cw2 + gx * 0.5); y = y2 + 100 + row * (ch2 + 24)
    R(x, y, cw2, ch2, "#fbfcfd", LINE, 10)
    T(x + 18, y + 32, f"{k + 1}", 15, ACC, 600, MONO); T(x + 40, y + 32, title, 19, INK, 600, SERIF)
    T(x + 18, y + 218, formula, 15, INK, 500, MONO)
    P(x + 18, y + 244, example, cw2 - 36, 13, MUTED, 18)
    if note: T(x + 18, y + 286, note, 13, ACC, 600)
    return x, y
def mini_theta(x, y, lab="θ", r=20):
    C(x, y, r, "#f6edf3", LAT, 1.8, DASH); T(x, y + 6, lab, 17 if len(lab) < 3 else 13, LAT, 600, SERIF, "middle")
def mini_box(x, y, lab, w=58, h=30):
    R(x - w / 2, y, w, h, "#fff", INK, 4, 1.2); T(x, y + 20, lab, 12, INK, 500, MONO, "middle")
# 1 parallel
x, y = card(0, "Parallel: mitteln", "x_i = λ_i·θ + ε_i", "RAND-36 23 pep · 27 energy · 29 worn out · 31 tired → alle EN1", "Var(Mittel) = σ²/k: genauer, nicht enger")
mini_theta(x + 248, y + 74)
for j, lab in enumerate(["23", "27", "29", "31"]):
    bx = x + 110 + j * 92; A(x + 248, y + 94, bx, y + 140); mini_box(bx, y + 142, lab)
# 2 graded
x, y = card(1, "Gestuft: abtasten", "x_i = 1 wenn θ > b_i", "RAND-36 11 ein Block · 10 mehrere Blocks · 9 eine Meile → alle PF2", "Antwort (ja, ja, nein) → θ ∈ [b₁₀, b₉)")
ax0, ax1, ay = x + 30, x + 466, y + 128
A(ax0, ay, ax1, ay, INK, 1.4); T(ax1 - 4, ay + 24, "θ", 16, LAT, 600, SERIF, "end")
for j, (lab, px, ans) in enumerate([("b₁₁", 0.22, "ja"), ("b₁₀", 0.47, "ja"), ("b₉", 0.76, "nein")]):
    xx = ax0 + px * (ax1 - ax0); L(xx, ay - 26, xx, ay + 8, INK, 2)
    T(xx, ay + 28, lab, 14, INK, 500, MONO, "middle"); T(xx, ay - 34, ans, 13, COL["wert"][0], 600, anchor="middle")
add(f'<rect x="{ax0 + 0.47 * (ax1 - ax0):.1f}" y="{ay - 8}" width="{0.29 * (ax1 - ax0):.1f}" height="8" fill="{LAT}" opacity=".35"/>')
T(x + 30, y + 178, "Last-Facette = Position b_i auf der Achse", 13, MUTED)
# 3 composite
x, y = card(2, "Composite: mehrere Variablen", "Σ λ_g·θ_g   oder   min_g θ_g", "FUNCAP 32 „Dinner party“ → CG2, CG4, CG7, SN2 (+ CG6?)", "nicht identifizierbar: x ↛ einzelnes θ")
for j, lab in enumerate(["CG2", "CG4", "CG7", "SN2"]):
    tx = x + 110 + j * 92; mini_theta(tx, y + 74, lab, 22); A(tx, y + 96, x + 248, y + 140)
mini_box(x + 248, y + 142, "F55-32", 70)
# 4 global
x, y = card(3, "Global", "θ_GL ≈ g(θ_1, …, θ_n)", "RAND-36 1 „In general, your health is …“ → GL1", "Gesamturteil über viele Variablen")
for j in range(5):
    tx = x + 90 + j * 80; C(tx, y + 60, 11, "#f6edf3", LAT, 1.2, DASH); A(tx, y + 71, x + 248, y + 92, MUTED, 1)
mini_theta(x + 248, y + 112, "GL", 20); A(x + 248, y + 132, x + 248, y + 146); mini_box(x + 248, y + 148, "R36-1")
# 5 change
x, y = card(4, "Änderung", "x = f(θ_jetzt − θ_Anker)", "RAND-36 2 „Compared to one year ago …“, PGIC → nicht im Check-in-Baum", "periodische Fragebögen")
mini_theta(x + 150, y + 96, "θ₀"); mini_theta(x + 346, y + 96, "θ_t")
A(x + 172, y + 96, x + 322, y + 96, LAT, 1.6); T(x + 248, y + 86, "Δθ", 17, LAT, 600, SERIF, "middle")
A(x + 248, y + 102, x + 248, y + 140); mini_box(x + 248, y + 142, "R36-2")
# 6 measured
x, y = card(5, "Gemessen statt bewertet", "x = θ_phys + ε_Gerät", "Puls aus der Uhr (AU3), Gewicht von der Waage (NE7)", "eigene Einheit, nie mit Ratings gepoolt")
R(x + 196, y + 62, 104, 62, "#fff", MUTED, 14, 1.4); T(x + 248, y + 100, "♥ 72 bpm", 15, INK, 500, MONO, "middle")
A(x + 248, y + 126, x + 248, y + 140); mini_box(x + 248, y + 142, "Wert")

# ================================================================ 3 IRT + 4 Facetten
y3, h3 = y2 + h2 + 30, 560
hw = (CW - 30) / 2
panel(X0, y3, hw, h3, "03", "Gestufte Items als Wahrscheinlichkeit", "Antworten sind verrauscht: Wer an der Schwelle liegt, sagt mal ja, mal nein.")
px0, py0, pw, ph = X0 + 80, y3 + 120, hw - 140, 250
L(px0, py0 + ph, px0 + pw, py0 + ph, INK, 1.3); L(px0, py0, px0, py0 + ph, INK, 1.3)
for v, lab in [(0, "0"), (0.5, "0,5"), (1, "1")]:
    yy = py0 + ph - v * ph; L(px0 - 5, yy, px0, yy, INK); T(px0 - 10, yy + 5, lab, 12.5, MUTED, 400, MONO, "end")
    if v == 0.5: L(px0, yy, px0 + pw, yy, LINE, 1, 'stroke-dasharray="3 4"')
T(px0 - 10, py0 - 14, "P(x_i = 1)", 13.5, MUTED, 500, MONO)
T(px0 + pw, py0 + ph + 30, "θ", 17, LAT, 600, SERIF, "end")
def curve(b, a, col, dash=""):
    pts = []
    for k in range(121):
        t = k / 120; th = -4 + 8 * t
        p = 1 / (1 + math.exp(-a * (th - b))); pts.append(f"{px0 + t * pw:.1f},{py0 + ph - p * ph:.1f}")
    add(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.4" {dash}/>')
curve(-1.4, 1.6, COL["wert"][0]); curve(1.2, 1.6, ACC); curve(1.2, 6, INK, 'stroke-dasharray="5 4"')
for b, lab, col in [(-1.4, "b₁₁ (1 Block)", COL["wert"][0]), (1.2, "b₉ (1 Meile)", ACC)]:
    xx = px0 + (b + 4) / 8 * pw; L(xx, py0 + ph, xx, py0 + ph / 2, col, 1, 'stroke-dasharray="3 3"')
    T(xx, py0 + ph + 22, lab, 12.5, col, 600, anchor="middle")

fy = py0 + ph + 72
T(X0 + 26, fy, "P(x_i = 1) = σ(a · (θ − b_i)),   σ(z) = 1 / (1 + e^(−z))", 17, INK, 500, MONO)
P(X0 + 26, fy + 32, "b_i = Schwierigkeit: bei θ = b_i ist P = 0,5.  a = Trennschärfe: Steigung der Kurve. Gestrichelt: a groß, die Kurve wird zur Stufe (Guttman). RAND-36 hat 3 Antwortstufen, also 2 Schwellen pro Item (Graded Response Model).", hw - 52, 14, MUTED, 20)

fx0 = X0 + hw + 30
panel(fx0, y3, hw, h3, "04", "Facetten: drei Typen", "Der Typ entscheidet, ob der Baum die Facette fragen muss.")
fts = [("wert", "Wert", "Position auf der θ-Achse (= b_i)", "load", "1 Block · 1 Meile · 100 m", "verlustfrei: s enthält die Position"),
       ("format", "Format", "wie gefragt wird", "measure · pole · anchor · Zeitraum", "energy vs fatigue · gestern vs letzte Woche", "verlustfrei für die Bedeutung"),
       ("kontext", "Kontext", "Bedingung, unter der θ auftritt", "region · trigger · timing · modality · activity · quality", "Schwindel nach dem Aufstehen", "verliert Information, wenn ungefragt")]
for k, (kind, name, what, keys, ex_, verdict) in enumerate(fts):
    fg, bg = COL[kind]; yy = y3 + 100 + k * 140
    R(fx0 + 26, yy, hw - 52, 124, bg, bg, 10)
    T(fx0 + 46, yy + 34, name, 21, fg, 600, SERIF); T(fx0 + 170, yy + 34, what, 15, INK, 500)
    T(fx0 + 46, yy + 62, "Schlüssel", 12.5, MUTED); T(fx0 + 130, yy + 62, keys, 13, INK, 400, MONO)
    T(fx0 + 46, yy + 86, "Beispiel", 12.5, MUTED); T(fx0 + 130, yy + 86, ex_, 13.5, INK)
    T(fx0 + 46, yy + 110, ("✓ " if kind != "kontext" else "✗ ") + verdict, 13.5, fg, 600)
P(fx0 + 26, y3 + 535, "Messtyp-Regel: DSQ misst Symptomlast, FUNCAP Kapazität/Kosten, RAND-36 Niveau. Gleiche Bedeutung, Zahlen nicht 1:1 vergleichbar.", hw - 52, 13, MUTED, 18)

# ================================================================ 5 Baum/Projektion + 6 Schubladen
y4, h4 = y3 + h3 + 30, 640
panel(X0, y4, hw, h4, "05", "Der Baum: Projektion der Facetten", "Ein Blatt sieht nur die gefragten Facetten A. Alles andere wirft die Projektion π_A weg.")
bx = X0 + 26; by = y4 + 106
for k, iid in enumerate(["DSQ2-71", "DSQ2-51"]):
    it = I[iid]; yy = by + k * 118
    R(bx, yy, 360, 100, "#fff", INK, 7, 1.2)
    T(bx + 12, yy + 22, iid, 13.5, INK, 600, MONO); T(bx + 92, yy + 22, it["text"] if len(it["text"]) < 36 else it["text"][:34] + "…", 12.5, MUTED)
    T(bx + 12, yy + 46, "M(i) = {" + ", ".join(it["g"]) + "}", 13, INK, 500, MONO)
    cx_ = bx + 12
    for kk, v in it["f"]: cx_ = chip(cx_, yy + 76, f"{kk}: {v}"[:26], model.ftype(kk), 10.5)
    A(bx + 362, yy + 50, bx + 400, by + 110, MUTED)
fxp = bx + 404
add(f'<path d="M{fxp},{by + 50} L{fxp + 120},{by + 80} L{fxp + 120},{by + 140} L{fxp},{by + 170} Z" fill="{ACC_S}" stroke="{ACC}" stroke-width="1.4"/>')
T(fxp + 54, by + 106, "π_A", 21, ACC, 600, MONO, "middle"); T(fxp + 54, by + 128, "Filter", 12, ACC, 500, anchor="middle")
A(fxp + 122, by + 110, fxp + 160, by + 110, ACC)
R(fxp + 162, by + 64, 150, 92, ACC_S, ACC, 8, 1.5)
T(fxp + 174, by + 88, "Blatt ℓ", 14, ACC, 600, MONO); T(fxp + 174, by + 110, "G = {AU2}", 13, INK, 500, MONO)
T(fxp + 174, by + 130, "c|A = { }", 13, INK, 500, MONO); T(fxp + 174, by + 148, "dizzy or faint", 12, MUTED)
T(fxp, by + 196, "A = {region, activity,", 12.5, MUTED, 400, MONO); T(fxp, by + 214, "     bladder, sweating}", 12.5, MUTED, 400, MONO)
fy = by + 268
R(X0 + 26, fy - 30, hw - 52, 106, PAPER, PAPER, 8)
T(X0 + 44, fy, "trifft(ℓ, i)  ⇔  G_ℓ ∩ M(i) ≠ ∅  ∧  π_A(c_i) ~ c_ℓ", 16.5, INK, 500, MONO)
T(X0 + 44, fy + 28, "verträglich = gleicher Wert ∨ 'unspecified' ∨ Schlüssel fehlt", 13.5, MUTED, 400, MONO)
T(X0 + 44, fy + 52, "L(i) = { ℓ | trifft(ℓ, i) }   Etikett eines Items", 13.5, MUTED, 400, MONO)
fy += 112
P(X0 + 26, fy, "Doppelpfade: mehrere Klickwege führen zum selben Mapping (Heimat-Blatt + „Same leaf as“). |Pfade| ≥ |Mappings|, die Information ändert sich nicht.", hw - 52, 14, INK, 20)
P(X0 + 26, fy + 66, "Konstrukt-Blätter („… in general“) speichern nur das Konstrukt und treffen keine Items.", hw - 52, 14, MUTED, 20)

panel(fx0, y4, hw, h4, "06", "Schubladen: die Auflösung des Baums", "i ~ j  ⇔  L(i) = L(j): gleiches Etikett, gleiche Schublade.")
T(fx0 + 26, y4 + 106, "Der Baum unterscheidet Schubladen, aber keine Items innerhalb einer Schublade.", 14.5, INK)
T(fx0 + 26, y4 + 136, "|Items|  ≥  |Granule + alle Facetten|  ≥  |Schubladen|", 15.5, INK, 500, MONO)
bmax = max(r["items"] for r in RES.values())
barw = hw - 230
for k, (inst, r) in enumerate(RES.items()):
    yy = y4 + 164 + k * 98
    T(fx0 + 26, yy + 16, inst, 15, INK, 600)
    for j, (val, lab, col) in enumerate([(r["items"], "Items", "#c3ccd5"), (r["full"], "Granule + Facetten", "#8fa3b6"), (r["drawers"], "Schubladen", ACC)]):
        w_ = val / bmax * barw; y_ = yy + 30 + j * 22
        R(fx0 + 130, y_ - 13, w_, 17, col, col, 3); T(fx0 + 136 + w_, y_, f"{val}", 13, INK, 600, MONO)
        if k == 0: T(fx0 + 26, y_, lab, 11.5, MUTED)
yy = y4 + 164 + 3 * 98 + 10
T(fx0 + 26, yy, "Schubladen mit > 1 Item, nach Typ der unterscheidenden Facette", 14, INK, 600)
for k, (inst, r) in enumerate(RES.items()):
    y_ = yy + 32 + k * 30; T(fx0 + 26, y_ + 4, inst, 13.5, INK, 500)
    x_ = fx0 + 130
    for kind in ("kontext", "wert", "format", "parallel"):
        n = r[kind]
        if not n: continue
        w_ = n * 16; fg, bg = COL[kind]; R(x_, y_ - 12, w_, 22, bg, fg, 3, 1); T(x_ + w_ / 2, y_ + 4, n, 12.5, fg, 600, MONO, "middle"); x_ += w_ + 4
x_ = fx0 + 26; y_ = yy + 128
for kind, lab in (("kontext", "Kontext"), ("wert", "Wert"), ("format", "Format"), ("parallel", "parallel")):
    x_ = chip(x_, y_, lab, kind, 12) + 6
P(fx0 + 26, y_ + 28, "Typ automatisch nach Facetten-Schlüssel (Heuristik). Interaktiv prüfen: out/mapping-explorer.html", hw - 52, 13, MUTED, 18)

# ================================================================ 7 Kriterium
y5, h5 = y4 + h4 + 30, 300
R(X0, y5, CW, h5, "#fff8ef", COL["kontext"][0], 12, 1.6)
T(X0 + 26, y5 + 44, "07", 15, COL["kontext"][0], 600, MONO); T(X0 + 62, y5 + 44, "Das Kriterium: wann der Baum eine Facette weglassen darf", 25, INK, 600, SERIF)
P(X0 + 26, y5 + 86, "Formal: Der Baum darf eine Facette f unbefragt lassen, wenn sich in jeder Schublade alle Items, die sich nur in f unterscheiden, durch einen θ-Wert (Wert) oder eine Formulierung (Format) unterscheiden. Unterscheiden sie sich durch eine Bedingung (Kontext), muss f gefragt werden, oder der Verlust wird bewusst in Kauf genommen.", 900, 15.5, INK, 23)
P(X0 + 26, y5 + 210, "Locker: Eine Schublade ist harmlos, wenn ihre Items sich nur durch Wert oder Format unterscheiden. Bei Kontext verliert der Baum Information.", 900, 15.5, COL["kontext"][0], 23, 600)
ex_d = next(d for d in model.drawers(M, "DSQ") if any("EN4" in l for l in [", ".join(I[i["id"]]["g"]) for i in d["items"]]) and len(d["items"]) > 3)
ex_x = X0 + 990
R(ex_x, y5 + 70, 540, 200, PANEL, LINE, 10)
T(ex_x + 18, y5 + 98, f"Beispiel: Schublade EN4 im DSQ ({len(ex_d['items'])} Items)", 14.5, INK, 600)
cy_ = y5 + 128
for it in ex_d["items"][:5]:
    trg = next((v for k, v in it["f"] if k == "trigger"), None)
    T(ex_x + 18, cy_, it["id"], 12.5, INK, 500, MONO)
    if trg: chip(ex_x + 110, cy_, f"trigger: {trg}"[:40], "kontext", 11)
    else: chip(ex_x + 110, cy_, " · ".join(f"{k}: {v}" for k, v in it["f"])[:40] or "–", "format", 11)
    cy_ += 24
T(ex_x + 18, y5 + 258, "→ Zusatzfrage nach EN4 (körperlich / geistig) hebt den Verlust auf.", 13, COL["kontext"][0], 600)

# ================================================================ 8 Jaccard + Polarität + Glossar
y6, h6 = y5 + h5 + 30, 420
tw = (CW - 60) / 3
panel(X0, y6, tw, h6, "08", "Überlappung")
vx, vy = X0 + tw / 2, y6 + 170
add(f'<circle cx="{vx - 50}" cy="{vy}" r="80" fill="{ACC}" fill-opacity=".14" stroke="{ACC}" stroke-width="1.5"/>')
add(f'<circle cx="{vx + 50}" cy="{vy}" r="80" fill="{LAT}" fill-opacity=".12" stroke="{LAT}" stroke-width="1.5"/>')
T(vx - 92, vy - 92, "S (Score)", 13, ACC, 600, anchor="middle"); T(vx + 92, vy - 92, "M(i) (Item)", 13, LAT, 600, anchor="middle")
T(vx - 88, vy + 5, "CG1 CG3", 11.5, INK, 400, MONO, "middle"); T(vx - 88, vy + 22, "CG5 CG6", 11.5, INK, 400, MONO, "middle")
T(vx, vy - 10, "CG2", 11.5, INK, 600, MONO, "middle"); T(vx, vy + 7, "CG4", 11.5, INK, 600, MONO, "middle"); T(vx, vy + 24, "CG7", 11.5, INK, 600, MONO, "middle")
T(vx + 92, vy + 7, "SN2", 11.5, INK, 400, MONO, "middle")
T(X0 + 26, y6 + 300, "J(S, M(i)) = |S ∩ M(i)| / |S ∪ M(i)|", 15, INK, 500, MONO)
P(X0 + 26, y6 + 330, "User wählt CG1–CG7, FUNCAP 32 trägt {CG2, CG4, CG7, SN2}: J = 3/8. Abdeckung einer Skala: erreichte Items / Items der Skala.", tw - 52, 13.5, MUTED, 19)

px_ = X0 + tw + 30
panel(px_, y6, tw, h6, "09", "Polarität")
P(px_ + 26, y6 + 90, "Die Richtung wird vor dem Mapping gesetzt (Standard: hoch = besser). Gespeichert wird ein Vorzeichen:", tw - 52, 14.5, INK, 21)
T(px_ + 26, y6 + 170, "sgn(s) = +1  wenn hoch = gesünder", 15, INK, 500, MONO); T(px_ + 26, y6 + 196, "sgn(s) = −1  sonst", 15, INK, 500, MONO)
for k, (g_, txt) in enumerate([("±", "bipolar: Label passt sich an, keine Frage"), ("▲▼", "good / bad: bei Widerspruch einmal bestätigen"), ("○", "neutral: nie fragen (Geräte, EN5)")]):
    T(px_ + 26, y6 + 248 + k * 32, g_, 16, ACC, 600, MONO); T(px_ + 70, y6 + 248 + k * 32, txt, 14, INK)

gx_ = X0 + 2 * (tw + 30)
panel(gx_, y6, tw, h6, "10", "Symbole")
gl = [("θ_g", "latente Variable"), ("c, c_i", "Facetten (Bedingung)"), ("A", "gefragte Facetten-Schlüssel"), ("π_A", "Projektion auf A"),
      ("M(i)", "Granules von Item i"), ("L(i)", "Blätter, die i treffen"), ("~", "gleiche Schublade"), ("λ", "Ladung / Gewicht"),
      ("b_i, a", "Schwierigkeit, Trennschärfe"), ("ε", "Rauschen"), ("Δθ", "Änderung zum Anker"), ("J", "Jaccard-Index")]
for k, (s, d) in enumerate(gl):
    T(gx_ + 26, y6 + 86 + k * 27, s, 14.5, LAT if k == 0 else INK, 600, MONO); T(gx_ + 120, y6 + 86 + k * 27, d, 14, INK)

# ================================================================ footer
fy = y6 + h6 + 46
T(X0, fy, f"Generiert aus data/mecfs-criteria.xlsx → merge.json mit pipeline/build_poster.py · {datetime.date.today().isoformat()} · "
          f"{len(M['granules'])} Granules · {sum(1 for l in M['leaves'])} Blätter · Text: THEORY.md", 13, MUTED)
add("</svg>")
H_used = fy + 30
svg = "\n".join(out).replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {H_used:.0f}" width="{W}" height="{H_used:.0f}"')
open(OUT, "w", encoding="utf-8").write(svg)
print("poster:", OUT, f"{W}x{H_used:.0f}")
