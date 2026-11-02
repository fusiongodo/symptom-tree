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

W, H = 1680, 5600
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
def fit(s, maxw, size, k=0.6):
    """font size so that s fits into maxw (no truncation)"""
    return min(size, maxw / max(1, len(str(s)) * k))
def chip(x, y, s, kind, size=12.5, maxw=None):
    if maxw: size = fit(s, maxw - 14, size, 0.62)
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
y1, h1 = 220, 590
panel(X0, y1, CW, h1, "01", "Das Modell: eine Variable, viele Messungen",
      "Eine Frage ist eine Messung einer Variable unter einer Bedingung. Frage und Variable stehen in einer n:m-Beziehung.")
cx, cy = X0 + 380, y1 + 190
C(cx, cy, 58, "#f6edf3", LAT, 2.2, DASH)
T(cx, cy - 4, "θ", 34, LAT, 600, SERIF, "middle"); T(cx, cy + 22, "PF2", 13, LAT, 500, MONO, "middle")
T(cx - 78, cy - 20, "latente Variable (Granule)", 14, LAT, 600, anchor="end"); T(cx - 78, cy - 1, "„Wie weit kann ich gehen?“", 14, MUTED, anchor="end")
T(cx - 78, cy + 18, "nicht direkt beobachtbar", 14, MUTED, anchor="end")
ex = ["R36-11", "R36-10", "R36-7", "R36-9"]
SHORT = {"R36-11": "Walking one block", "R36-10": "Several blocks", "R36-7": "One flight of stairs", "R36-9": "Walking > 1 mile"}
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
T(bx0, y1 + 530, "Items: dieselbe Variable unter verschiedenen Bedingungen c_i (hier: Gehstrecke = Last).", 14, MUTED)
T(bx0, y1 + 556, "λ = Ladung: wie stark θ in die Antwort eingeht.   ε = Rauschen.", 14, MUTED)
# score
sx, sy = X0 + 560, y1 + 120
A(cx + 58, cy - 8, sx + 160, sy + 60, ACC, 1.8)
R(sx + 160, sy + 52, 220, 78, ACC_S, ACC, 8, 1.5)
T(sx + 172, sy + 76, "s  User-Score", 14, ACC, 600, MONO); T(sx + 172, sy + 97, "„Gehstrecke heute (m)“", 13.5, INK)
T(sx + 172, sy + 117, "Baum speichert π_A(c_s)", 13, MUTED, 400, MONO)
# formulas right
fx = X0 + 1010; fy = y1 + 120
T(fx, fy, "Die fünf Objekte", 17, INK, 600)
rows = [("θ_g", "Variable (Granule g): was wir wissen wollen"),
        ("c", "Bedingung: Facetten; Index einer Variablenfamilie θ_g(c)"),
        ("i", "Item: trägt Granules M(i) und volle Facetten c_i"),
        ("S", "Skala: Mittelwert über k Items, das berichten Studien"),
        ("s", "User-Score: die Zahl, die der User einträgt (Slider)")]
for k, (sym, txt) in enumerate(rows):
    T(fx, fy + 34 + k * 27, sym, 15, LAT if k == 0 else INK, 600, MONO); T(fx + 52, fy + 34 + k * 27, txt, 14.5, INK)
fy += 34 + 5 * 27 + 18
R(fx - 12, fy, 552, 194, PAPER, PAPER, 8)
for k, (f, d) in enumerate([("x_i = f_i(θ, c_i) + ε_i", "f_i: wie Item i θ in eine Antwort übersetzt"), ("S   = (1/k) · Σ x_i", "Skala über k Items"),
                            ("s   = h(θ_g(c_s)) + ε", "c_s: was der User meint · h: seine Skala"),
                            ("π_A(c_s) = c_s|A", "gespeichert: nur gefragte Facetten (A)")]):
    T(fx, fy + 36 + k * 44, f, 17, INK, 500, MONO); T(fx + 268, fy + 36 + k * 44, d, 12.5, MUTED)

# ================================================================ 2 Item-Typen
y2, h2 = y1 + h1 + 30, 760
panel(X0, y2, CW, h2, "02", "Sechs Item-Typen", "Die Typen unterscheiden sich in der Form von f. Mehrere Items pro Variable: mitteln (1) oder abtasten (2). FUNCAP ist ganz Typ 2, auf EN6.")
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
x, y = card(0, "Parallel: mitteln", "x_i = λ_i·θ + ε_i", "RAND-36 23 pep · 27 energy · 29 worn out · 31 tired → alle EN1", "Var(Mittel) = Var(ε)/k: genauer, nicht enger")
mini_theta(x + 248, y + 74)
for j, lab in enumerate(["23", "27", "29", "31"]):
    bx = x + 110 + j * 92; A(x + 248, y + 94, bx, y + 140); mini_box(bx, y + 142, lab)
# 2 graded
x, y = card(1, "Gestuft: abtasten", "x_i = 1 wenn θ > b_i", "RAND-36 11 ein Block · 10 mehrere Blocks · 9 eine Meile → PF2. FUNCAP: 55 Kosten-Items auf EN6, die Aktivität ist b_i.", "Antwort (ja, ja, nein) → θ ∈ [b₁₀, b₉)")
ax0, ax1, ay = x + 30, x + 466, y + 128
A(ax0, ay, ax1, ay, INK, 1.4); T(ax1 - 4, ay + 24, "θ", 16, LAT, 600, SERIF, "end")
for j, (lab, px, ans) in enumerate([("b₁₁", 0.22, "ja"), ("b₁₀", 0.47, "ja"), ("b₉", 0.76, "nein")]):
    xx = ax0 + px * (ax1 - ax0); L(xx, ay - 26, xx, ay + 8, INK, 2)
    T(xx, ay + 28, lab, 14, INK, 500, MONO, "middle"); T(xx, ay - 34, ans, 13, COL["wert"][0], 600, anchor="middle")
add(f'<rect x="{ax0 + 0.47 * (ax1 - ax0):.1f}" y="{ay - 8}" width="{0.29 * (ax1 - ax0):.1f}" height="8" fill="{LAT}" opacity=".35"/>')
T(x + 30, y + 178, "b_i = Schwierigkeit: Stufe von Item i auf der θ-Achse", 13, MUTED)
# 3 composite
x, y = card(2, "Composite: mehrere Variablen", "Σ λ_g·θ_g   oder   min_g θ_g", "DSQ2-38 „finding the right word to say or expressing thoughts“ → CG6, CG7", "nicht identifizierbar: x ↛ einzelnes θ")
for j, lab in enumerate(["CG6", "CG7"]):
    tx = x + 196 + j * 104; mini_theta(tx, y + 74, lab, 22); A(tx, y + 96, x + 248, y + 140)
mini_box(x + 248, y + 142, "DSQ2-38", 76)
# 4 global
x, y = card(3, "Global", "θ_GL ≈ agg(θ_1, …, θ_n)", "RAND-36 1 „In general, your health is …“ → GL1", "Gesamturteil über viele Variablen")
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
P(X0 + 26, fy + 32, "Bei θ = b_i ist P = 0,5.  a = Trennschärfe (Steigung), σ = logistische S-Kurve. Gestrichelt: a groß, die Kurve wird zur Stufe (Guttman). RAND-36 hat 3 Antwortstufen, also 2 Schwellen pro Item (Graded Response Model).", hw - 52, 14, MUTED, 20)

fx0 = X0 + hw + 30
panel(fx0, y3, hw, h3, "04", "Facetten: drei Typen", "Der Typ entscheidet, ob der Baum die Facette fragen muss.")
fts = [("wert", "Wert", "Position auf der θ-Achse (= b_i)", "load", "1 Block · 1 Meile · 100 m", "verlustfrei: s enthält die Position"),
       ("format", "Format", "wie gefragt wird", "measure · pole · anchor · Zeitraum", "energy vs fatigue · gestern vs letzte Woche", "verlustfrei für die Bedeutung"),
       ("kontext", "Kontext", "Bedingung, unter der θ auftritt", "region · trigger · timing · load type · activity · quality", "Schwindel nach dem Aufstehen", "verliert Information, wenn ungefragt")]
yy = y3 + 96
for kind, name, what, keys, ex_, verdict in fts:
    fg, bg = COL[kind]; hh = 150 if kind == "format" else 122
    R(fx0 + 26, yy, hw - 52, hh, bg, bg, 10)
    T(fx0 + 46, yy + 34, name, 21, fg, 600, SERIF); T(fx0 + 170, yy + 34, what, 15, INK, 500)
    T(fx0 + 46, yy + 62, "Schlüssel", 12.5, MUTED); T(fx0 + 130, yy + 62, keys, 13, INK, 400, MONO)
    T(fx0 + 46, yy + 86, "Beispiel", 12.5, MUTED); T(fx0 + 130, yy + 86, ex_, 13.5, INK)
    if kind == "format":
        T(fx0 + 46, yy + 110, "pro Instrument", 12.5, MUTED)
        T(fx0 + 150, yy + 110, "Messtyp: DSQ Symptomlast · RAND-36 Niveau · FUNCAP Kosten = eigene Variable (EN6)", 13.5, INK)
        T(fx0 + 46, yy + 136, "✓ Baum muss nicht fragen (gleiche Bedeutung)   ✗ Werte nicht über Instrumente hinweg mitteln", 13.5, fg, 600)
    else:
        T(fx0 + 46, yy + 110, ("✓ " if kind != "kontext" else "✗ ") + verdict, 13.5, fg, 600)
    yy += hh + 14

# ================================================================ 5 Baum/Projektion + 6 Schubladen
y4, h4 = y3 + h3 + 30, 1250
panel(X0, y4, hw, h4, "05", "Der Baum: Knoten, Blätter, Projektion", "Jeder Knoten trägt einen Zustand. Ein Blatt sieht nur die gefragten Facetten.")
yy = y4 + 108
for key, val in [("Knoten n", "Zustand (G_n, c_n). G_n = Granules, die unter n noch erreichbar sind. c_n = bisher beantwortete Facetten (Schlüssel aus A)."),
                 ("Blatt ℓ", "Endknoten. (G_ℓ, c_ℓ) ist das gespeicherte Mapping."),
                 ("D(n)", "{ i | trifft(n, i) }: die Items, die Knoten n trifft. Für ein Blatt ist D(ℓ) seine Schublade.")]:
    T(X0 + 26, yy, key, 14, ACC, 600, MONO)
    yy = P(X0 + 120, yy, val, hw - 150, 13.5, INK, 19) + 10
by = yy + 8
leafAU2 = next(l for l in M["leaves"] if not l["same"] and l["g"] == "AU2")
T(X0 + 26, by + 6, "Score → Fragen → Blatt", 13, ACC, 600); T(X0 + hw - 26, by + 6, "Item → π_A → Blatt", 13, LAT, 600, anchor="end")
ux, uw = X0 + 26, 210
R(ux, by + 22, uw, 50, ACC_S, ACC, 8, 1.4); T(ux + 12, by + 42, "Score", 11.5, ACC, 600); T(ux + 12, by + 62, "„Schwindel“ 0–10", 13.5, INK)
qy = by + 72
for k, ans in enumerate(leafAU2["path"]):
    A(ux + uw / 2, qy + 2, ux + uw / 2, qy + 24, ACC)
    T(ux + 12, qy + 40, f"Frage {k + 1}", 11.5, MUTED, 600)
    R(ux, qy + 48, uw, 26, "#fff", ACC, 13, 1.2); T(ux + uw / 2, qy + 66, ans, fit(ans, uw - 12, 11, 0.55), INK, 500, anchor="middle")
    qy += 78
lx_, lw_ = X0 + 26 + 250, 200; ly_ = by + 120
A(ux + uw + 2, qy - 17, lx_ - 4, ly_ + 60, ACC, 1.6)
R(lx_, ly_, lw_, 116, ACC_S, ACC, 8, 1.8)
T(lx_ + 14, ly_ + 26, "Blatt ℓ", 15, ACC, 600, MONO); T(lx_ + 14, ly_ + 50, "G_ℓ = {AU2}", 13.5, INK, 500, MONO)
T(lx_ + 14, ly_ + 72, "c_ℓ = { }", 13.5, INK, 500, MONO); T(lx_ + 14, ly_ + 96, "hier fragt der Baum", 11.5, MUTED); T(lx_ + 14, ly_ + 110, "keine Facette", 11.5, MUTED)
ix, iw = X0 + 26 + 490, hw - 52 - 490
for k, iid in enumerate(["DSQ2-71", "DSQ2-51"]):
    it = I[iid]; y = by + 22 + k * 150
    R(ix, y, iw, 136, "#fff", INK, 7, 1.2)
    T(ix + 10, y + 20, iid, 13, INK, 600, MONO); T(ix + 10, y + 40, "M(i) = {" + ", ".join(it["g"]) + "}", 12.5, INK, 500, MONO)
    yy2 = y + 62
    for kk, v in it["f"]:
        chip(ix + 10, yy2, f"{kk}: {v}", model.ftype(kk), 10, maxw=iw - 20); yy2 += 22
    T(ix + 10, y + 126, "π_A(c_i) = { }", 12.5, ACC, 600, MONO)
    A(ix - 2, y + 70, lx_ + lw_ + 4, ly_ + 40 + k * 36, LAT, 1.4)
T((ix + lx_ + lw_) / 2 + 4, ly_ + 58, "trifft ✓", 12.5, LAT, 600, anchor="middle")
P(X0 + 26, by + 330, "Das Blatt ist der Treffpunkt: Der User erreicht es über Fragen, Items treffen es über ihre Granules und die gefragten Facetten. Facetten, die der Baum nicht fragt, wirft π_A weg (hier trigger und quality).", hw - 52, 13, MUTED, 18)
fy = by + 420
R(X0 + 26, fy - 30, hw - 52, 106, PAPER, PAPER, 8)
T(X0 + 44, fy, "trifft(n, i)  ⇔  G_n ∩ M(i) ≠ ∅  ∧  π_A(c_i) ≃ c_n", 16.5, INK, 500, MONO)
T(X0 + 44, fy + 28, "≃ verträglich: gleicher Wert ∨ 'unspecified' ∨ Schlüssel fehlt", 13.5, MUTED, 400, MONO)
T(X0 + 44, fy + 52, "L(i) = { ℓ | trifft(ℓ, i) }: Etikett eines Items (nur Blätter)", 13.5, MUTED, 400, MONO)
ry = fy + 112
T(X0 + 26, ry, "Regeln für Knoten", 16, INK, 600)
RULES = [("R1", "Regel", "Monotonie: Für ein Kind m von n gilt G_m ⊆ G_n und c_m ⊇ c_n, ohne Widerspruch."),
         ("R2", "Lemma", "Aus R1 folgt D(m) ⊆ D(n). Jeder Knoten ist ein gültiger Endpunkt der Konfiguration, tiefer heißt feiner."),
         ("R3", "Regel", "Eine Facette wird nur gefragt, wenn sie Kontext ist und Items in D(n) trennt. Jeder Schlüssel höchstens einmal pro Pfad."),
         ("R4", "zulässig", "Facette an einem inneren Knoten, wenn sie Items mehrerer Granules teilt: trigger: standing → AU2, AU3, SN4 (DSQ2-71, -69, -70). Heute nicht genutzt.")]
ry += 30
for rid, stat, txt in RULES:
    T(X0 + 26, ry, rid, 14, ACC, 600, MONO)
    R(X0 + 58, ry - 14, 66, 19, ACC_S, ACC_S, 4); T(X0 + 91, ry, stat, 11.5, ACC, 600, anchor="middle")
    ry = P(X0 + 136, ry, txt, hw - 166, 13.5, INK, 19) + 10
ry += 6
ry = P(X0 + 26, ry, "Doppelpfade: mehrere Klickwege führen zum selben Mapping (Heimat-Blatt + „Same leaf as“). |Pfade| ≥ |Mappings|, die Information ändert sich nicht.", hw - 52, 13.5, INK, 19) + 8
ry = P(X0 + 26, ry, "Konstrukt-Blätter („… in general“) speichern heute nur das Konstrukt. Nach R2 hätten sie D(n) = alle Items der Konstrukt-Granules.", hw - 52, 13.5, MUTED, 19)
# --- R1/R2 at a real path (live): node state shrinks/grows, D(n) shrinks
JT = __import__("json").load(open(SRC, encoding="utf-8"))["tree"]
def below(node):
    gs, its = set(), set()
    for t in JT:
        if t["node"] != node or t["to"] == "multi-select": continue
        if t["to"] == "leaf":
            if t["same"]: continue
            gs |= set(model.leaf_granules(t["g"])); its |= {x for x in t["items"].split(", ") if x}
        else:
            g2, i2 = below(t["to"]); gs |= g2; its |= i2
    return gs, its
leafH = next(t for t in JT if t["node"] == "PN-N2" and t["a"] == "Headache")
chain = [("PN-N1", "Schmerz: was bewerten?", *below("PN-N1"), "{ }"),
         ("PN-N2", "Wo ist der Schmerz?", *below("PN-N2"), "{ }"),
         ("Blatt", "Headache", set(model.leaf_granules(leafH["g"])), {x for x in leafH["items"].split(", ") if x}, "{" + leafH["facet"] + "}")]
ry += 30
T(X0 + 26, ry, "R1 und R2 an einem echten Pfad (Items aller Instrumente)", 14.5, INK, 600)
bw5 = (hw - 52 - 2 * 30) / 3
for k, (nid, q_, gs, its, cn) in enumerate(chain):
    x = X0 + 26 + k * (bw5 + 30); y = ry + 14
    R(x, y, bw5, 112, ACC_S if k == 2 else "#fbfcfd", ACC if k == 2 else LINE, 8, 1.2)
    T(x + 12, y + 22, nid, 13, ACC, 600, MONO); T(x + 12, y + 40, q_, 12, MUTED)
    gtxt = "{" + ", ".join(sorted(gs)) + "}"
    T(x + 12, y + 62, "G_n = " + gtxt, 12.5, INK, 500, MONO)
    T(x + 12, y + 82, "c_n = " + cn, 12.5, INK, 500, MONO)
    T(x + 12, y + 102, f"|D(n)| = {len(its)} Items", 12.5, COL["kontext"][0], 600, MONO)
    if k < 2: A(x + bw5 + 2, y + 56, x + bw5 + 28, y + 56, ACC)
ry += 14 + 112
P05_END = ry

panel(fx0, y4, hw, h4, "06", "Einteilungen: Schubladen, Sektionen, Konstrukte", "Drei Einteilungen der Items (E₀–E₂) und zwei der Granules.")
PART = {inst: model.partitions(M, inst) for inst in model.DRAWER_INSTRUMENTS}
rows6 = [("E₀", "Items", "dasselbe Item"), ("E₁", "Annotation", "gleiche Granules M(i) und gleiche Facetten c_i"),
         ("E₂", "Schubladen", "gleiche Blätter L(i), also i ~ j ⇔ L(i) = L(j)")]
T(fx0 + 26, y4 + 106, "Zwei Items liegen zusammen, wenn sie … haben:", 13, MUTED)
for k, (e, name, rule) in enumerate(rows6):
    yy = y4 + 136 + k * 28
    T(fx0 + 26, yy, e, 16, ACC, 600, MONO); T(fx0 + 66, yy, name, 14.5, INK, 600); T(fx0 + 180, yy, rule, 14, INK)
ly = y4 + 228
R(fx0 + 26, ly, hw - 52, 64, ACC_S, ACC_S, 8)
T(fx0 + 42, ly + 26, "Lemma: E₀ ⊑ E₁ ⊑ E₂ (geschachtelt)", 15, ACC, 600, MONO)
T(fx0 + 42, ly + 49, "Gleiche Granules + Facetten ⇒ gleiche Blätter. Jede E₁-Gruppe liegt ganz in einer Schublade.", 13.5, INK)
bmax = max(p["n0"] for p in PART.values()); barw = hw - 330
for k, (inst, P_) in enumerate(PART.items()):
    yy = y4 + 324 + k * 92
    T(fx0 + 26, yy + 16, inst, 15, INK, 600)
    vals = [(P_["n0"], "E₀ Items", "#c3ccd5", ""), (P_["n1"], "E₁ Annotation", "#8fa3b6", f"−{P_['n0'] - P_['n1']} Annotation"),
            (P_["n2"], "E₂ Schubladen", ACC, f"−{P_['n1'] - P_['n2']} Baum")]
    for j, (val, lab, col, loss) in enumerate(vals):
        w_ = val / bmax * barw; y_ = yy + 30 + j * 22
        R(fx0 + 140, y_ - 13, w_, 17, col, col, 3); T(fx0 + 146 + w_, y_, f"{val}", 13, INK, 600, MONO)
        if loss: T(fx0 + 182 + w_, y_, loss, 12.5, COL["kontext"][0], 600)
        if k == 0: T(fx0 + 26, y_, lab, 11.5, MUTED)
yy = y4 + 324 + 3 * 92 + 6
T(fx0 + 26, yy, "Schubladen mit > 1 Item, nach Typ der unterscheidenden Facette", 14, INK, 600)
for k, (inst, r) in enumerate(RES.items()):
    y_ = yy + 32 + k * 30; T(fx0 + 26, y_ + 4, inst, 13.5, INK, 500)
    x_ = fx0 + 140
    for kind in ("kontext", "wert", "format", "parallel"):
        n = r[kind]
        if not n: continue
        w_ = n * 16; fg, bg = COL[kind]; R(x_, y_ - 12, w_, 22, bg, fg, 3, 1); T(x_ + w_ / 2, y_ + 4, n, 12.5, fg, 600, MONO, "middle"); x_ += w_ + 4
x_ = fx0 + 26; y_ = yy + 128
for kind, lab in (("kontext", "Kontext"), ("wert", "Wert"), ("format", "Format"), ("parallel", "parallel")):
    x_ = chip(x_, y_, lab, kind, 12) + 6
P(fx0 + 26, y_ + 28, "Typ per Facetten-Schlüssel (Heuristik). Prüfen im Explorer, Ansicht „Verluste“.", hw - 52, 13, MUTED, 18)
# --- Sektion vs Konstrukt: zwei Einteilungen der Granules (live)
sy = y_ + 120
L(fx0 + 26, sy - 22, fx0 + hw - 26, sy - 22, LINE)
T(fx0 + 26, sy, "Sektion vs. Konstrukt: zwei Einteilungen der Granules", 16, INK, 600)
T(fx0 + 26, sy + 24, "Sektion (Präfix)", 13.5, INK, 600); T(fx0 + 150, sy + 24, "Herkunft: wo die Granule entstand. CG-N3 = 3. Knoten der Sektion, nicht Tiefe 3.", 13, MUTED)
T(fx0 + 26, sy + 46, "Konstrukt", 13.5, INK, 600); T(fx0 + 150, sy + 46, "Darstellung: was Studien berichten. N0 zeigt die 10 Konstrukte.", 13, MUTED)
T(fx0 + 26, sy + 70, "Beide teilen dieselben Granules ein: Eine Sektion verteilt sich auf mehrere Konstrukte und umgekehrt.", 13, INK)
SECS = ["EN", "PF", "MO", "GL"]
CON_OF = {g["id"]: g["construct"] for g in M["granules"]}
edges = {}
for g in M["granules"]:
    pre = g["id"].rstrip("0123456789")
    if pre in SECS and CON_OF[g["id"]]: edges.setdefault((pre, CON_OF[g["id"]]), []).append(g["id"])
cons = []
for (pre, c) in edges:
    if c not in cons: cons.append(c)
CN = {c["id"]: c["name"] for c in M["constructs"]}
lx, rx, ty = fx0 + 70, fx0 + hw - 250, sy + 106
ys = {p_: ty + k * (126 / (len(SECS) - 1)) for k, p_ in enumerate(SECS)}
yc = {c: ty + k * (126 / (len(cons) - 1)) for k, c in enumerate(cons)}
placed = []
for (pre, c), gs in edges.items():
    L(lx + 34, ys[pre], rx - 8, yc[c], "#9aa8b6", 1.3)
    lab_ = ", ".join(gs) if len(gs) <= 3 else f"{gs[0]}–{gs[-1]}"
    wl = len(lab_) * 6.8 + 8
    for t_ in (0.5, 0.3, 0.7, 0.18, 0.82):
        mx = lx + 34 + t_ * (rx - 8 - lx - 34) - wl / 2; my = ys[pre] + t_ * (yc[c] - ys[pre])
        box = (mx - 4, my - 11, mx + wl, my + 6)
        if not any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in placed): break
    placed.append(box)
    R(mx - 4, my - 11, wl, 16, PANEL, PANEL, 3); T(mx, my + 2, lab_, 11, LAT, 500, MONO)
for pre in SECS:
    R(lx - 4, ys[pre] - 13, 42, 22, ACC_S, ACC, 4); T(lx + 17, ys[pre] + 3, pre, 13, ACC, 600, MONO, "middle")
for c in cons:
    R(rx - 6, yc[c] - 13, 230, 22, PAPER, LINE, 4); T(rx + 2, yc[c] + 3, f"{c}  {CN[c]}", fit(f"{c}  {CN[c]}", 214, 12.5, 0.55), INK, 500)
T(lx - 4, ty + 152, "Sektion", 11.5, MUTED, 600); T(rx - 6, ty + 152, "Konstrukt", 11.5, MUTED, 600)




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
    if trg: chip(ex_x + 110, cy_, f"trigger: {trg}", "kontext", 11, maxw=410)
    else: chip(ex_x + 110, cy_, " · ".join(f"{k}: {v}" for k, v in it["f"]) or "–", "format", 11, maxw=410)
    cy_ += 24
T(ex_x + 18, y5 + 258, "→ Zusatzfrage nach EN4 (körperlich / geistig) hebt den Verlust auf.", 13, COL["kontext"][0], 600)


# ================================================================ 8 Die Instrumente (live from model.profile)
yI, hI = y5 + h5 + 30, 580
panel(X0, yI, CW, hI, "08", "Die Instrumente: was ihre Items messen",
      "Gleiche Granule heißt nicht gleiche Zahl. Jedes Instrument hat eigene Frage, Messtyp und Item-Mischung (Typen aus 02; Kontext-Variante = gleiche Variable, andere Bedingung).")
TYPE_COL = {"einzeln": ("#7d8894", "#e3e7eb"), "parallel": COL["parallel"], "gestuft": COL["wert"], "kontext": COL["kontext"],
            "composite": (LAT, "#f3e3ee"), "global": COL["format"], "änderung": ("#8a6a1f", "#f4ead2")}
TYPE_LAB = {"einzeln": "einzeln", "parallel": "parallel", "gestuft": "gestuft", "kontext": "Kontext-Variante",
            "composite": "composite", "global": "global", "änderung": "Änderung"}
PROF = {inst: model.profile(M, inst) for inst in model.INSTRUMENTS}
NFMT = {inst: len({i["resp"] for i in M["items"] if i["inst"] == inst and i["status"] == "mapped"}) for inst in model.INSTRUMENTS}
INFO = {
    "DSQ": ("DSQ-2|Messtyp: Symptomlast", "„How often … / How severe … in the past 6 months?“ Häufigkeit 0–4 × Stärke 0–4",
            "Viele Variablen, je ein bis zwei Items. Zwei Items derselben Variable unterscheiden sich meist durch eine Bedingung (Auslöser, Körperregion), kaum durch Stufen."),
    "RAND-36": ("RAND-36|Messtyp: Niveau, Einschränkung, Häufigkeit", f"„Does your health now limit you …?“, „How much of the time …?“ u. a.: {NFMT['RAND-36']} Antwortformate",
                "Wenige Variablen, mehrere Items pro Skala: mitteln (Energie, Stimmung, Gesundheit) und abtasten (Gehstrecke, Treppen). Studien berichten 8 Skalen."),
    "FUNCAP": ("FUNCAP55|Messtyp: Kosten einer Aktivität", "„What are the consequences for you if you perform …? How much else can you do?“ 0–6, gleich für alle Items",
               "Eine Variable, viele Aktivitäten. Jedes Item fragt die Kosten derselben Belastbarkeit θ_budget (EN6). Die Aktivität setzt die Schwierigkeit: x = f(θ_budget − d(Aktivität)) + ε."),
}
cwI = (CW - 52 - 3 * 16 - 260) / 3
for k, inst in enumerate(["DSQ", "RAND-36", "FUNCAP"]):
    pr, (head, stem, prof) = PROF[inst], INFO[inst]; r_ = RES[inst]
    x = X0 + 26 + k * (cwI + 16); y = yI + 100
    R(x, y, cwI, 450, "#fbfcfd", LINE, 10)
    nm_, mt_ = head.split("|")
    T(x + 18, y + 32, nm_, 20, INK, 600, SERIF); T(x + 18, y + 54, mt_, 13.5, ACC, 600)
    yy = P(x + 18, y + 78, stem, cwI - 36, 12.5, MUTED, 17) + 8
    stats = [(pr["items"], "Items"), (pr["granules"], "Granules"), (f"{pr['per_granule']:.1f}".replace(".", ","), "Items/Granule"), (pr["drawers"], "Schubladen")]
    sw_ = (cwI - 36) / 4
    for j, (v, lab_) in enumerate(stats):
        T(x + 18 + j * sw_, yy + 24, v, 24, ACC, 600, MONO); T(x + 18 + j * sw_, yy + 42, lab_, 11.5, MUTED)
    yy += 66
    T(x + 18, yy, "Item-Typen (Anteil der Items)", 12, MUTED, 600); yy += 10
    bx_, bw_ = x + 18, cwI - 36
    for t_ in model.ITEM_TYPES:
        n = pr["types"].get(t_, 0)
        if not n: continue
        w_ = n / pr["items"] * bw_; fg, bg = TYPE_COL[t_]
        R(bx_, yy, w_, 22, fg, "#fff", 0, 1)
        if w_ > 26: T(bx_ + w_ / 2, yy + 16, n, 11.5, "#fff", 600, MONO, "middle")
        bx_ += w_
    yy += 42
    lx_ = x + 18
    for t_ in model.ITEM_TYPES:
        n = pr["types"].get(t_, 0)
        if not n: continue
        lab_ = f"{TYPE_LAB[t_]} {n}"; wl = len(lab_) * 6.6 + 22
        if lx_ + wl > x + cwI - 18: lx_ = x + 18; yy += 20
        R(lx_, yy - 10, 10, 10, TYPE_COL[t_][0], TYPE_COL[t_][0], 2); T(lx_ + 14, yy, lab_, 11.5, INK); lx_ += wl
    yy += 30
    yy = P(x + 18, yy, prof, cwI - 36, 13.5, INK, 19) + 10
    loss = (f"Baum: {r_['kontext']} von {r_['multi']} Schubladen mit > 1 Item trennen Kontext → Verlust (z. B. Auslöser bei EN4)" if inst == "DSQ" else
            f"Baum: {r_['kontext']} Kontext-Schubladen, Rest Wert/Format → fast verlustfrei" if inst == "RAND-36" else
            f"Baum: Lastart wird gefragt (= Domäne A–H), Last ist Wert → {r_['kontext']} Kontext-Verluste")
    P(x + 18, y + 428 - 19 * (len(wrap(loss, cwI - 36, 13)) - 1), loss, cwI - 36, 13, COL["kontext"][0] if r_["kontext"] else COL["wert"][0], 19, 600)
x = X0 + 26 + 3 * (cwI + 16); y = yI + 100
R(x, y, 260, 450, "#fbfcfd", LINE, 10)
T(x + 18, y + 32, "Bell · PGIC", 20, INK, 600, SERIF)
yy = y + 64
for name_, typ, txt in [("Bell", "global", "Ein Item: Gesamtniveau 0–100 in Zehnerstufen (GL2). Mischt Symptome und Funktion."),
                        ("PGIC", "änderung", "Ein Item: Änderung seit Protokollstart, 7 Stufen (GL3). Misst Δθ, steht nicht im Check-in-Baum.")]:
    fg, bg = TYPE_COL[typ]; R(x + 18, yy - 14, 12, 12, fg, fg, 2); T(x + 36, yy - 3, f"{name_} · {TYPE_LAB[typ]}", 14, INK, 600)
    yy = P(x + 18, yy + 22, txt, 224, 13, INK, 18) + 22
P(x + 18, yy + 10, "Typzuordnung je Item: Regel in model.item_types (Granules, Schublade, Facettentyp). Heuristik wie in 06.", 224, 12, MUTED, 17)

# ================================================================ 9 Polarität, 10 Überlappung, 11 Symbolindex
y7, h7 = yI + hI + 30, 440
y6, h6 = y7 + h7 + 30, 420
tw = hw
panel(X0, y6, tw, h6, "10", "Überlappung")
vx, vy = X0 + tw / 2, y6 + 170
add(f'<circle cx="{vx - 50}" cy="{vy}" r="80" fill="{ACC}" fill-opacity=".14" stroke="{ACC}" stroke-width="1.5"/>')
add(f'<circle cx="{vx + 50}" cy="{vy}" r="80" fill="{LAT}" fill-opacity=".12" stroke="{LAT}" stroke-width="1.5"/>')
T(vx - 92, vy - 92, "G_s (Score)", 13, ACC, 600, anchor="middle"); T(vx + 92, vy - 92, "M(i) (Item)", 13, LAT, 600, anchor="middle")
T(vx - 92, vy - 12, "CG1 CG2", 11.5, INK, 400, MONO, "middle"); T(vx - 92, vy + 5, "CG3 CG5", 11.5, INK, 400, MONO, "middle"); T(vx - 92, vy + 22, "CG6 CG7", 11.5, INK, 400, MONO, "middle")
T(vx, vy + 7, "CG4", 11.5, INK, 600, MONO, "middle")
T(vx + 92, vy + 7, "EN4", 11.5, INK, 400, MONO, "middle")
T(X0 + 26, y6 + 300, "J(G_s, M(i)) = |G_s ∩ M(i)| / |G_s ∪ M(i)|", 15, INK, 500, MONO)
P(X0 + 26, y6 + 330, "G_s = Granule-Menge des Scores. User wählt CG1–CG7, DSQ2-80 („reading after mild activity“) trägt {CG4, EN4}: J = 1/8. Abdeckung einer Skala: erreichte Items / Items der Skala.", tw - 52, 13.5, MUTED, 19)

gx_ = X0 + tw + 30
panel(gx_, y6, tw, h6, "11", "Symbolindex", "Wo jedes Symbol definiert ist (Panel-Nummer).")
IDX = [("θ_g, g", "01"), ("c, c_i", "01"), ("i, M(i)", "01"), ("x_i, f_i, h", "01"), ("λ, ε", "01"), ("S, k", "01"), ("s", "01"),
       ("c_s, A, π_A", "01"), ("b_i", "02"), ("agg, Δθ", "02"), ("a, σ(z)", "03"), ("n, G_n, c_n", "05"), ("ℓ, G_ℓ, c_ℓ", "05"), ("D(n)", "05"),
       ("trifft, ≃", "05"), ("L(i)", "05"), ("R1–R4", "05"), ("~, E₀–E₂", "06"), ("θ_budget, d", "08"), ("sgn(s)", "09"), ("G_s, J", "10"),
       ("t, s_t, log_t", "12"), ("ĉ_t, D_t, θ_t", "12"), ("γ, n_γ, κ, w", "12")]
half = (len(IDX) + 1) // 2
for k, (sym, pn) in enumerate(IDX):
    col, row = divmod(k, half)
    xx = gx_ + 26 + col * (tw / 2 - 10); yy = y6 + 112 + row * 24
    T(xx, yy, sym, 13.5, INK, 600, MONO); T(xx + tw / 2 - 70, yy, pn, 13.5, ACC, 600, MONO, "end")


# ================================================================ 9 Polarität (full width, live labels)
panel(X0, y7, CW, h7, "09", "Polarität",
      "Die Richtung des Scores wird vor dem Mapping gesetzt (Standard: hoch = besser). Gespeichert wird nur ein Vorzeichen.")
T(X0 + 26, y7 + 108, "sgn(s) = +1  wenn ein hoher Wert gesünder ist,   sgn(s) = −1  sonst", 16, INK, 500, MONO)
LEAFS = {}
for l in M["leaves"]:
    if not l["same"]: LEAFS.setdefault(l["g"], l)
TREE = {(t["node"], t["a"]): t for t in __import__("json").load(open(SRC, encoding="utf-8"))["tree"]}
JS = __import__("json").load(open(SRC, encoding="utf-8")); Q = JS["confirm_question"]
def lab(g, side):
    t = next(t for t in JS["tree"] if t["to"] == "leaf" and not t["same"] and t["g"] == g)
    return t["label_high_better" if side == "better" else "label_high_worse"]
cards = [
    ("±", "bipolar", "EN1 Fatigue / Energie", "Zwei Pole, beide Formulierungen existieren. Das Label folgt der Richtung.", [
        [("Score", "„Energie“ · hoch = besser"), ("App", f"zeigt „{lab('EN1', 'better')}“"), ("→", "keine Frage · sgn = +1")],
        [("Score", "„Erschöpfung“ · hoch = schlechter"), ("App", f"zeigt „{lab('EN1', 'worse')}“"), ("→", "keine Frage · sgn = −1")]]),
    ("▲", "good", "PF2 Gehen", "Der Pol ist eine Fähigkeit: mehr ist gesünder.", [
        [("Score", "„Gehstrecke“ · hoch = besser"), ("→", "passt zum Pol · keine Frage · sgn = +1")],
        [("Score", "„Gehprobleme“ · hoch = schlechter"), ("App", f"Widerspruch, fragt „{Q}“"), ("→", "Ja · sgn = −1")]]),
    ("▼", "bad", "PN1 Kopfschmerz", "Der Pol ist ein Symptom: mehr ist kränker.", [
        [("Score", "„Kopfschmerz“ · Standard hoch = besser"), ("App", f"Widerspruch, fragt „{Q}“"), ("→", "Nein · Richtung kippt · sgn = −1")],
        [("Score", "„Kopf frei“ · hoch = besser"), ("App", "fragt dieselbe Frage"), ("→", "Ja · sgn = +1")]]),
    ("○", "neutral", "AU3 Puls (Gerät) · EN5 Aktivität", "Mehr ist weder gut noch schlecht. Das entscheidet erst die Analyse.", [
        [("Score", "„Ruhepuls von der Uhr“"), ("→", "nie fragen · sgn = +1 heißt nur „mehr Schläge“")],
        [("Score", "„Wie viel ich gemacht habe“"), ("→", "nie fragen · mehr Aktivität kann gut sein oder einen Crash auslösen")]]),
]
cw4 = (CW - 52 - 3 * 18) / 4
for k, (glyph, kind, gran, rule, scen) in enumerate(cards):
    x = X0 + 26 + k * (cw4 + 18); y = y7 + 136
    R(x, y, cw4, 278, "#fbfcfd", LINE, 10)
    T(x + 16, y + 32, glyph, 22, ACC, 600, MONO); T(x + 50, y + 30, kind, 18, INK, 600, SERIF)
    T(x + 50, y + 50, gran, 12.5, MUTED, 500, MONO)
    yy = P(x + 16, y + 76, rule, cw4 - 32, 12.5, MUTED, 17) + 4
    for j, sc in enumerate(scen):
        L(x + 16, yy - 6, x + cw4 - 16, yy - 6, LINE)
        for key, val in sc:
            T(x + 16, yy + 12, key, 11.5, MUTED, 600)
            yy = P(x + 64, yy + 12, val, cw4 - 80, 12.5, INK if key != "→" else ACC, 17, 400 if key != "→" else 600) - 12 + 2
        yy += 14
# ================================================================ 11 Ausblick: Facetten pro Check-in
y8, h8 = y6 + h6 + 30, 960
R(X0, y8, CW, h8, PANEL, ACC, 12, 1.4, 'stroke-dasharray="8 6"')
T(X0 + 26, y8 + 44, "12", 15, ACC, 600, MONO); T(X0 + 62, y8 + 44, "Nach App V1: Facetten pro Check-in · neuer Workflow", 25, INK, 600, SERIF)
T(X0 + 26, y8 + 72, "Der User konfiguriert bis zu einem Knoten n, meist einem Blatt. Optional nennt er in der Sprachnotiz Facetten, die D(n) pro Check-in verfeinern.", 14.5, MUTED)
EN4 = next(d for d in model.drawers(M, "DSQ") if len(d["items"]) > 5 and all("EN4" in i["g"] for i in d["items"]))
trig = lambda i: next((v for k, v in i["f"] if k == "trigger"), None)
dx, dy = X0 + 26, y8 + 104
# 1 configuration
R(dx, dy, 220, 100, ACC_S, ACC, 8, 1.4)
T(dx + 12, dy + 22, "einmal: Konfiguration", 12, ACC, 600); T(dx + 12, dy + 44, "Score „Crash-Schwere“ 0–10", 13.5, INK)
T(dx + 12, dy + 64, "Baum endet an Knoten n:", 12.5, MUTED)
T(dx + 12, dy + 86, "(G_n, c_n) = ({EN4}, { })", 13, INK, 500, MONO)
A(dx + 222, dy + 50, dx + 262, dy + 50, ACC)
# 2 drawer with groups
bx, by, bw, bh = dx + 266, dy - 6, 470, 238
R(bx, by, bw, bh, "#fbfcfd", INK, 8, 1.4)
T(bx + 12, by + 22, "D = D(n): Schublade EN4 im DSQ", 13.5, INK, 600); T(bx + bw - 12, by + 22, f"{len(EN4['items'])} Items", 12.5, MUTED, anchor="end")
yy = by + 44
for it in EN4["items"]:
    hit = trig(it) and "mental" in trig(it)
    if hit: R(bx + 8, yy - 15, bw - 16, 21, COL["kontext"][1], COL["kontext"][1], 4)
    T(bx + 16, yy, it["id"], 12, INK, 600 if hit else 400, MONO)
    lab_ = f"trigger: {trig(it)}" if trig(it) else " · ".join(f"{k}: {v}" for k, v in it["f"])
    T(bx + 110, yy, lab_, fit(lab_, bw - 120, 12, 0.6), COL["kontext"][0] if trig(it) else MUTED, 600 if hit else 400, MONO)
    yy += 23
# 3 check-in with voice log
cx_, cy_ = dx, dy + 124
R(cx_, cy_, 220, 150, "#fff", INK, 8, 1.2)
T(cx_ + 12, cy_ + 22, "Check-in t", 12, INK, 600)
T(cx_ + 12, cy_ + 46, "s_t = 7", 17, INK, 500, MONO); T(cx_ + 92, cy_ + 46, "Slider-Wert", 12, MUTED)
T(cx_ + 12, cy_ + 72, "log_t: Sprachnotiz (optional)", 12, MUTED)
for k, line in enumerate(["„Crash, weil ich gestern bei", "der Verabredung zu lange", "geredet habe.“"]):
    T(cx_ + 12, cy_ + 92 + k * 17, line, 12.5, INK, 400, SERIF, style='font-style="italic"')
A(cx_ + 222, cy_ + 75, bx - 4, cy_ + 75, COL["kontext"][0])
T((cx_ + 222 + bx) / 2, cy_ + 66, "LLM", 12, COL["kontext"][0], 600, anchor="middle")
T(bx, by + bh + 26, "ĉ_t = {trigger: mental}  →  D_t = markierte Items", 14, COL["kontext"][0], 600, MONO)
T(dx, by + bh + 58, "Ohne Notiz: ĉ_t = ∅, D_t = D. Die Messung zählt dann auf Schubladen-Ebene.", 13.5, MUTED)
T(dx, by + bh + 82, "Wert-Facetten („kann nicht mal staubsaugen“) verfeinern nicht D, sondern verankern den Zahlenwert s_t.", 13.5, MUTED)
# formulas right
fx = X0 + 800; fy = y8 + 116
R(fx - 16, fy - 26, CW - 800 + 26 - 26, 530, PAPER, PAPER, 8)
rows = [("Konfiguration", "s endet an Knoten n:  (G_n, c_n),  D = D(n)", "Blatt oder früherer Knoten (R2)"),
        ("Check-in", "(s_t, log_t)", "t Zeitpunkt · s_t Slider-Wert · log_t Sprachnotiz, optional"),
        ("Extraktion", "ĉ_t = LLM(log_t),   ĉ_t = ∅ ohne Log", "ĉ_t: Facetten dieses Check-ins"),
        ("Verfeinerung", "D_t = { i ∈ D | c_i ≃ ĉ_t }  ⊆  D", "D_t: Items, die zu diesem Check-in passen"),
        ("Messmodell", "s_t = h(θ_t, c_n ∪ ĉ_t) + ε_t", "θ_t: Zustand am Tag t"),
        ("Auswertung", "x̂_γ = w·x̄_γ + (1 − w)·x̄_D,   w = n_γ / (n_γ + κ)", "γ Facetten-Gruppe · x̄ Mittelwert · n_γ Check-ins in γ · κ Glättung"),
        ("Falle", "P(Facette erwähnt | θ_t) hängt von θ_t ab", "Trigger werden vor allem an schlechten Tagen erwähnt")]
for k, (lab_, f, d) in enumerate(rows):
    yy = fy + k * 70
    T(fx, yy, lab_, 12.5, MUTED, 600); T(fx, yy + 22, f, 15, COL["kontext"][0] if lab_ == "Falle" else INK, 500, MONO)
    T(fx, yy + 42, d, 12.5, MUTED)

# --- after App V1: new granularisation workflow (user, 2 Nov 2026)
wy = y8 + 680
L(X0 + 26, wy - 24, X0 + CW - 26, wy - 24, LINE)
T(X0 + 26, wy + 8, "Nach App V1: neuer Workflow für die Granularisierung", 19, INK, 600, SERIF)
T(X0 + 26, wy + 34, "Der Entwickler ist näher dran: systematisch, mit Review-Schritt vor jeder Sektion (oder jedem Konstrukt).", 14, MUTED)
STEPS = [("1", "Instrumente verstehen", "Paper der Instrumente lesen: allgemeines Verständnis (Konstrukt, Frage, Skala, Auswertung)."),
         ("2", "Verbindung modellieren", "Grob skizzieren, wie der Baum an diesen Instrumenttyp anschließt und worauf zu achten ist (z. B. Kosten statt Fähigkeit)."),
         ("3", "KI schlägt vor", "Anwendung: KI schlägt die Granularisierung vor, pro Sektion oder Konstrukt, instrumentübergreifend. Der Reviewer sieht alle Items mit Originalfrage und Skala."),
         ("4", "Reviewer approved", "Erst nach Freigabe geht es zur nächsten Sektion bzw. zum nächsten Konstrukt."),
         ("5", "Tests", "Blinder Agent (T1) und ein zweiter Test, z. B. blinder Zweit-Annotator für das Mapping.")]
sw5 = (CW - 52 - 4 * 24) / 5
for k, (n_, t_, d_) in enumerate(STEPS):
    x = X0 + 26 + k * (sw5 + 24); y = wy + 56
    R(x, y, sw5, 140, "#fff", ACC if k == 3 else LINE, 8, 1.6 if k == 3 else 1)
    T(x + 14, y + 28, n_, 16, ACC, 600, MONO); T(x + 36, y + 28, t_, 15, INK, 600)
    P(x + 14, y + 54, d_, sw5 - 28, 12.5, MUTED, 17)
    if k < 4: A(x + sw5 + 2, y + 70, x + sw5 + 22, y + 70, ACC)
P(X0 + 26, wy + 232, "Außerdem nach App V1: die eigene Theorie in die Konventionen von Psychometrie und Statistik übersetzen (Facet Theory, Generalisierbarkeitstheorie, IRT) · Schmerzregionen als eigene Granules statt Facetten von PN1 · Kontext-Schubladen im DSQ entscheiden (z. B. Zusatzfrage nach EN4).", CW - 52, 13.5, INK, 19)

# ================================================================ footer
fy = y8 + h8 + 46
T(X0, fy, f"Generiert aus data/mecfs-criteria.xlsx → merge.json mit pipeline/build_poster.py · {datetime.date.today().isoformat()} · "
          f"{len(M['granules'])} Granules · {sum(1 for l in M['leaves'])} Blätter · Text: THEORY.md", 13, MUTED)
add("</svg>")
H_used = fy + 30
svg = "\n".join(out).replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {H_used:.0f}" width="{W}" height="{H_used:.0f}"')
open(OUT, "w", encoding="utf-8").write(svg)
print("poster:", OUT, f"{W}x{H_used:.0f}")
