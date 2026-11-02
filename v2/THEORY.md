# Theorie: Vom Check-in-Score zum Instrument-Item

Ein Messmodell für den ME/CFS-Symptombaum. Es erklärt, was Fragen, Variablen, Facetten, Blätter und Schubladen sind
und wann der Baum Information verliert. Das Plakat `out/theory-poster.svg` fasst diesen Text zusammen. Die Zahlen hier
stammen aus dem Stand vom 2. Nov 2026. Aktuelle Zahlen stehen im Plakat und im Explorer, beide werden aus dem xlsx generiert.

---

## 0. Status der Aussagen

Nicht jede Aussage in diesem Modell ist gleich sicher. Jede gehört zu genau einer von vier Ebenen:

| Ebene | Bedeutung | Beispiel |
|---|---|---|
| **Regel** | festgelegt, steht im xlsx (Tab `Method`) | „Eine fehlende Facette ist nie ein Widerspruch“ |
| **Hypothese** | begründete Annahme, aus Itemtexten abgeleitet | die 69 Granules und das Mapping M |
| **Linse** | Theorie, die zu den Daten passt, aber nicht belegt ist | „Granule = latente Variable θ“ |
| **Evidenz** | Ergebnis eines Tests | T1-Pilot RAND-36: 32/35 exakt |

Die Granules wurden aus den Itemtexten nach Mechanismus abgeleitet. Ob sie wirklich latente Variablen sind, könnte erst
eine Faktorenanalyse auf echten Antwortdaten zeigen.

---

## 1. Die fünf Objekte

| Symbol | Objekt | Bedeutung |
|---|---|---|
| θ_g | **Variable** (Granule g) | was wir wissen wollen, nicht direkt beobachtbar. Beispiel PF2 „wie weit kann ich gehen“ |
| c | **Bedingung** (Facetten) | Schlüssel → Wert: wo, wann, unter welcher Last, bei welcher Aktivität |
| i | **Item** | eine Frage eines Instruments. Sie trägt Granules M(i) und volle Facetten c_i |
| S | **Skala** | Aggregat über eine Itemmenge, z. B. der Mittelwert. Das berichten Studien |
| s | **User-Score** | direkte Selbsteinschätzung über den Baum. Kennt nur die *gefragten* Facetten |

Antwortmodelle:

```
Item:   x_i = f_i(θ, c_i) + ε_i          Antwort = Funktion der Variable unter Bedingung c_i, plus Rauschen
Skala:  S   = (1/k) · Σ_{i∈S} x_i         Mittelwert über k Items
Score:  s   = h(θ, π_A(c)) + ε            Selbsteinschätzung, nur mit den Facetten, die der Baum fragt
```

**Kernsatz:** Eine Frage ist eine *Messung* einer Variable unter einer Bedingung. Frage und Variable stehen in einer
**n:m-Beziehung**. Mehrere Fragen pro Variable sind normal, auch innerhalb eines Instruments.

---

## 2. Sechs Item-Typen

Die Typen unterscheiden sich in der Form von f. Der triviale Fall „ein Item für eine Variable“ ist Typ 1 mit k = 1.

### 2.1 Parallel: Rauschen mitteln
Gleiche Variable, gleiche Bedingung, andere Formulierung.
```
x_i = λ_i · θ + ε_i          Var(Mittelwert über k Items) = σ²/k   (für λ_i = 1)
```
*Beispiel:* RAND-36 23 pep · 27 energy · 29 worn out · 31 tired → alle EN1.
**Hier wird nicht eingegrenzt.** θ wird nur genauer gemessen.

### 2.2 Gestuft: einen Bereich abtasten
Gleiche Variable, Bedingungen mit steigender Schwierigkeit b_i.
```
hart (Guttman):   x_i = 1  wenn θ > b_i
weich (IRT):      P(x_i = 1) = σ(a · (θ − b_i)),   σ(z) = 1 / (1 + e^(−z))
```
- **b_i = Schwierigkeit.** Für θ = b_i ist P = 0,5.
- **a = Trennschärfe**, also die Steigung. Für a → ∞ wird die S-Kurve zur Stufe (Guttman).
- Mehrstufige Antworten (RAND-36: a lot / a little / not at all) haben pro Item mehrere Schwellen (Graded Response Model).

*Beispiel:* RAND-36 11 ein Block (b klein) · 10 mehrere Blocks · 9 eine Meile (b groß) → alle PF2.
Das Antwortmuster (ja, ja, nein) heißt: θ liegt zwischen b₁₀ und b₉. **Das ist Eingrenzen.**

### 2.3 Composite: ein Item, mehrere Variablen
```
x = f(θ_1, …, θ_m) + ε
kompensatorisch:  f = Σ λ_g · θ_g      eine Stärke gleicht eine Schwäche aus
Engpass:          f = min_g θ_g         die schwächste Fähigkeit entscheidet
```
*Beispiel:* FUNCAP 32 „Dinner party“ → CG2, CG4, CG7, SN2 (CG6 ist Kandidat).
**Nicht identifizierbar:** Dieselbe Antwort kann verschiedene Ursachen haben, man kann x nicht auf ein einzelnes θ
zurückrechnen. Die Gewichte λ sind nur aus Antwortdaten schätzbar. Bis dahin gilt die Regel: ungewichtet, allen Granules zugeordnet.

### 2.4 Global
θ_GL ist eine übergeordnete Variable, wahrgenommen als Gesamturteil über viele θ. *Beispiel:* RAND-36 1, GL1.

### 2.5 Änderung
Gemessen wird Δθ = θ_jetzt − θ_Anker, nicht θ. *Beispiel:* RAND-36 2, PGIC. Diese Items stehen nicht im Check-in-Baum,
sie gehören in periodische Fragebögen.

### 2.6 Gemessen statt bewertet
x = θ_phys + ε_Gerät. Es gibt keine Selbsteinschätzung, die Einheit ist eine andere. *Beispiel:* Puls (AU3), Gewicht (NE7).
Diese Werte werden nie mit bewerteten Items gepoolt.

---

## 3. Facetten: drei Typen

Eine Facette ist ein Paar Schlüssel → Wert. Ihr **Typ** entscheidet, ob man sie im Baum fragen muss.

| Typ | Was sie beschreibt | Schlüssel (Heuristik) | Beispiel | Geht verloren, wenn ungefragt? |
|---|---|---|---|---|
| **Wert** | Position auf der θ-Achse (= b_i) | load | ein Block / eine Meile | **nein**, s enthält die Position |
| **Format** | wie gefragt wird | measure, pole, anchor, Zeitraum | energy vs fatigue; gestern vs letzte Woche | **nein** für die Bedeutung |
| **Kontext** | Bedingung, unter der θ auftritt | region, trigger, timing, modality, activity, quality, type | Schwindel *nach dem Aufstehen* | **ja** |

**Lemma (Wert-Facetten).** Wenn sich Items nur in einer Wert-Facette unterscheiden, sind sie Stufen b_i desselben θ.
Ein Score s = h(θ) trägt die Position auf der Achse direkt, deshalb geht nichts verloren.

**Messtyp-Regel (Format auf Instrumentebene).** DSQ fragt nach der Symptomlast (Häufigkeit und Stärke), FUNCAP nach
Kapazität und Kosten, RAND-36 nach dem Niveau. Die Bedeutung ist gleich, die Zahlen sind aber nicht 1:1 vergleichbar.
Ausgewertet wird deshalb innerhalb einer Person (standardisiert); Studien werden auf Skalenebene verglichen.

Die Typzuordnung nach Schlüssel ist eine Heuristik. Einzelwerte können abweichen, z. B. ist „load: bending“ eher Kontext.

---

## 4. Der Baum

- **Struktur.** Der Baum ist ein gerichteter Graph. Jeder innere Knoten stellt eine Frage, jede Antwort führt zu einem
  Knoten oder zu einem Blatt.
- **Blatt.** ℓ = (G_ℓ, c_ℓ). G_ℓ ist die Granule-Menge, c_ℓ enthält nur Werte der *gefragten* Facetten-Schlüssel A
  (heute: Region bei Schmerz, Aktivität bei Funktion, Blase, Schwitzen).
- **Projektion.** π_A(c) = c, eingeschränkt auf die Schlüssel in A. Beispiel: π_A({trigger: standing, quality: greying}) = {}.
- **Trefferregel.**
  ```
  trifft(ℓ, i)  ⇔  G_ℓ ∩ M(i) ≠ ∅   ∧   π_A(c_i) verträglich mit c_ℓ
  verträglich   =  gleicher Wert  ∨  'unspecified'  ∨  Item trägt den Schlüssel gar nicht
  ```
- **Doppelpfade.** Mehrere Pfade können zum selben Mapping führen (Heimat-Blatt + „Same leaf as“). Es gilt
  |Pfade| ≥ |Mappings|. Das dient der Bedienbarkeit und ändert die Information nicht.
- **Konstrukt-Blätter.** „… in general“ speichert nur das Konstrukt und trifft keine Items.

Als Interface:
```ts
interface Item { granules: Set<G>; facets: Map<Key, Value> }   // vollständig, aus dem Itemtext
interface Leaf { granules: Set<G>; asked:  Map<Key, Value> }   // nur Schlüssel aus A
L(i) = { ℓ | trifft(ℓ, i) }                                     // Etikett eines Items
```

---

## 5. Schubladen (Äquivalenzklassen)

**Definition.** i ~ j ⇔ L(i) = L(j), also wenn genau dieselben Blätter beide Items treffen.

Die Relation ~ ist reflexiv, symmetrisch und transitiv, also eine **Äquivalenzrelation**. Ihre Klassen heißen
**Schubladen**. Jedes Item liegt in genau einer Schublade.

**Intuition.** Jedes Item bekommt als Etikett „welche Blätter treffen mich?“. Items mit gleichem Etikett liegen in derselben Schublade.

**Lemma (Restriktion).** Schränkt man ~ auf ein Instrument ein, bleibt sie eine Äquivalenzrelation. Die Schubladen pro
Instrument sind also die Schnitte der globalen Schubladen mit dem Instrument.

**Satz (Auflösung des Baums).** Der Baum kann Schubladen unterscheiden, aber keine Items innerhalb einer Schublade.
Jede Stufe der folgenden Kette wirft Information weg:

```
|Items|  ≥  |Items / (Granule + alle Facetten)|  ≥  |Items / ~|  = Schubladen
```

| Instrument | Items | Granule + alle Facetten | Schubladen | davon > 1 Item |
|---|---|---|---|---|
| DSQ | 104 | 99 | 66 | 20 |
| RAND-36 | 36 | 33 | 17 | 9 |
| FUNCAP | 55 | 55 | 25 | 13 |

*Beispiel:* DSQ2-51 „dizziness“ und DSQ2-71 „greying out after standing“ liegen beide in der Schublade
„Feeling dizzy or faint“ (AU2), weil der Baum den Trigger nicht fragt.

---

## 6. Das Kriterium (Verlustfreiheit)

**Formal.** Der Baum darf eine Facette f unbefragt lassen, wenn sich in jeder Schublade alle Items, die sich nur in f
unterscheiden, durch einen θ-Wert (Wert-Typ) oder eine Formulierung (Format-Typ) unterscheiden. Unterscheiden sie sich
durch eine Bedingung (Kontext-Typ), muss f gefragt werden, oder man nimmt den Verlust bewusst in Kauf.

**Locker.** Eine Schublade ist harmlos, wenn ihre Items sich nur durch Wert oder Format unterscheiden. Unterscheiden sie
sich durch Kontext, verliert der Baum Information.

*Anwendung:* EN4 (Crash) vereint im DSQ Items mit trigger: physical / mental / exercise. Das ist ein Kontext-Verlust.
Eine Zusatzfrage nach dem Blatt EN4 würde ihn beheben.

---

## 7. Überlappung von Score und Item

Ein Score trifft die Granule-Menge S (bei Multi-Select mehrere), ein Item trägt M(i). Für einen Treffer müssen die
beiden Mengen nicht gleich sein, sie müssen sich überlappen. Die Güte der Überlappung misst der Jaccard-Index:

```
J(S, M(i)) = |S ∩ M(i)| / |S ∪ M(i)|        1 = identisch, 0 = disjunkt
```

*Beispiel:* Ein User wählt CG1–CG7, FUNCAP 32 hat {CG2, CG4, CG7, SN2}. Dann ist J = 3/8.

**Abdeckung einer Skala:** cov(S_Skala) = |erreichte Items ∩ S_Skala| / |S_Skala|. Einen Gesamtwert kann man nur bei cov = 1 berechnen.

---

## 8. Polarität

Die Richtung des Scores wird vor dem Mapping festgelegt. Gespeichert wird das Vorzeichen sgn(s):
+1, wenn ein hoher Wert gesünder ist, sonst −1. Es gibt vier Blatt-Typen:
- **bipolar:** Das Label passt sich der Richtung an, es gibt keine Frage.
- **good / bad:** Bei einem Widerspruch zur Richtung kommt einmal die Bestätigungsfrage.
- **neutral:** Es wird nie gefragt.

---

## 9. Offene Hypothesen und Tests

| Was | Ebene | Test |
|---|---|---|
| Granules = sinnvolle latente Variablen | Linse | Faktorenanalyse auf Antwortdaten |
| Mapping M korrekt | Hypothese | Test 3: blinder Zweit-Annotator, Abweichungen reviewen |
| Baum führt zum richtigen Blatt | Hypothese | T1: blinder Agent läuft mit dem Itemtext als Score-Name durch den Baum |
| Gewichte λ bei Composite-Items | offen | Antwortdaten |
| Facetten-Typ pro Einzelwert | Heuristik | Review der Kontext-Schubladen im Explorer |

---

## Symbolglossar

| Symbol | Bedeutung |
|---|---|
| θ_g | latente Variable zu Granule g |
| c, c_i | Facetten (Bedingung), c_i = volle Facetten von Item i |
| A | Menge der im Baum gefragten Facetten-Schlüssel |
| π_A | Projektion auf die Schlüssel in A |
| M(i) | Granule-Menge von Item i (Mapping) |
| G_ℓ, c_ℓ | Granules und gefragte Facetten von Blatt ℓ |
| L(i) | Menge der Blätter, die Item i treffen |
| ~ | „liegt in derselben Schublade“ |
| x_i | Antwort auf Item i |
| s | User-Score |
| λ_i | Ladung oder Gewicht (wie stark θ in x_i eingeht) |
| b_i, a | Schwierigkeit und Trennschärfe (IRT) |
| σ(z) | logistische S-Kurve 1/(1+e^(−z)) |
| ε | Rauschen |
| Δθ | Änderung gegenüber einem Anker |
| J | Jaccard-Index |
