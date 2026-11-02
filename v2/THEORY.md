# Theorie: Vom Check-in-Score zum Instrument-Item

Ein Messmodell für den ME/CFS-Symptombaum. Es erklärt, was Fragen, Variablen, Facetten, Blätter und Schubladen sind
und wann der Baum Information verliert. Das Plakat `out/theory-poster.svg` fasst diesen Text zusammen, `out/theory.html` ist
diese Datei als Lese-Seite. Die Zahlen stammen aus dem Stand **V1 (2. Nov 2026)**. Aktuelle Zahlen stehen im Plakat und im
Explorer, beide werden aus dem xlsx generiert.

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
| c | **Bedingung** (Facetten) | Schlüssel → Wert: wo, wann, unter welcher Last, bei welcher Aktivität. Index einer Variablenfamilie θ_g(c) |
| i | **Item** | eine Frage eines Instruments. Sie trägt Granules M(i) und volle Facetten c_i |
| S | **Skala** | Mittelwert über k Items. Das berichten Studien |
| s | **User-Score** | die Zahl, die der User einträgt (Slider). Der Baum speichert nur die *gefragten* Facetten |

Antwortmodelle:

```
Item:   x_i = f_i(θ, c_i) + ε_i          Antwort = Funktion der Variable unter Bedingung c_i, plus Rauschen
Skala:  S   = (1/k) · Σ_{i∈S} x_i         Mittelwert über k Items
Score:  s   = h(θ_g(c_s)) + ε              Selbsteinschätzung der Variable unter der Bedingung c_s, die der User meint
Mapping:      (G_ℓ, π_A(c_s))             gespeichert: alle Granules, aber nur die gefragten Facetten
```

Dabei ist θ der wahre, nicht beobachtbare Zustand und x_i die Antwort auf Item i. f_i beschreibt, wie Item i θ in eine
Antwort übersetzt, h, wie der User θ in seine Skala übersetzt (persönlich: Skala, Richtung, Anker). λ ist die Ladung (wie stark θ in die Antwort eingeht)
und ε Rauschen. **c_s** ist die Bedingung, die der User mit seinem Score meint (z. B. „Schwindel nach dem Aufstehen“).
**A** ist die Menge der im Baum gefragten Facetten-Schlüssel (heute Region bei Schmerz, Lastart beim Kosten-Knoten EN6,
Blase, Schwitzen), **π_A(c) = c|A** behält nur diese. π_A wirkt nur auf die Facetten, nie auf θ: Die Granule wird immer
vollständig gespeichert. Beispiel: π_A({trigger: standing, quality: greying}) = {}.

**Kernsatz:** Eine Frage ist eine *Messung* einer Variable unter einer Bedingung. Frage und Variable stehen in einer
**n:m-Beziehung**. Mehrere Fragen pro Variable sind normal, auch innerhalb eines Instruments.

---

## 2. Sechs Item-Typen

Die Typen unterscheiden sich in der Form von f. Der triviale Fall „ein Item für eine Variable“ ist Typ 1 mit k = 1.
Ein siebter Typ „Kosten“ ist nicht nötig: Kosten ist ein **Messtyp** (was die Antwortzahl ausdrückt, §3), kein eigener
Item-Typ. FUNCAP ist Typ 2 auf einer eigenen Variable (§2.2, §2.7).

### 2.1 Parallel: Rauschen mitteln
Gleiche Variable, gleiche Bedingung, andere Formulierung.
```
x_i = λ_i · θ + ε_i          Var(Mittelwert über k Items) = Var(ε)/k   (für λ_i = 1)
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

*Beispiel Kosten (FUNCAP):* Alle 55 FUNCAP-Items fragen dasselbe: „What are the consequences for you if you perform …?
To what extent does this affect how much else you can do?“, Skala 0–6 (0 = kann ich nicht · 1 = Kapazität ≥ 3 Tage stark
reduziert · … · 6 = beeinträchtigt nichts). Gemessen wird die **Belastbarkeit** θ_budget (Granule EN6), die Aktivität
setzt die Schwierigkeit d:
```
x_i = f(θ_budget − d(Aktivität_i, Fähigkeiten)) + ε_i
```
Fähigkeiten (Verstehen, Lärmtoleranz, Gehen …) erhöhen nur d. Sie zeigen sich in x erst, wenn das Budget knapp ist: Wer
schlecht versteht, aber kein Energieproblem hat, antwortet bei der Dinnerparty 6. Deshalb sind sie hier **Facette**
(load type), nicht Granule. Ausnahme in der Skala: Stufe 0 „I cannot do this“ ist Fähigkeit, nicht Kosten (akzeptiert).

### 2.3 Composite: ein Item, mehrere Variablen
```
x = f(θ_1, …, θ_m) + ε
kompensatorisch:  f = Σ λ_g · θ_g      eine Stärke gleicht eine Schwäche aus
Engpass:          f = min_g θ_g         die schwächste Fähigkeit entscheidet
```
*Beispiel:* DSQ2-38 „Difficulty finding the right word to say or expressing thoughts“ → CG6, CG7. (Bis V1 stand hier
FUNCAP 32 „Dinner party“ → CG2, CG4, CG7, SN2. Das war falsch: FUNCAP misst Kosten, siehe §2.2.)
**Nicht identifizierbar:** Dieselbe Antwort kann verschiedene Ursachen haben, man kann x nicht auf ein einzelnes θ
zurückrechnen. Die Gewichte λ sind nur aus Antwortdaten schätzbar. Bis dahin gilt die Regel: ungewichtet, allen Granules zugeordnet.

### 2.4 Global
θ_GL ≈ agg(θ_1, …, θ_n) ist eine übergeordnete Variable, wahrgenommen als Gesamturteil über viele θ. *Beispiel:* RAND-36 1, GL1.

### 2.5 Änderung
Gemessen wird Δθ = θ_jetzt − θ_Anker, nicht θ. *Beispiel:* RAND-36 2, PGIC. Diese Items stehen nicht im Check-in-Baum,
sie gehören in periodische Fragebögen.

### 2.6 Gemessen statt bewertet
x = θ_phys + ε_Gerät. Es gibt keine Selbsteinschätzung, die Einheit ist eine andere. *Beispiel:* Puls (AU3), Gewicht (NE7).
Diese Werte werden nie mit bewerteten Items gepoolt.

### 2.7 Die Instrumente nach Item-Typen

Gleiche Granule heißt nicht gleiche Zahl. Jedes Instrument hat eine eigene Frage, einen eigenen Messtyp und eine typische
Mischung von Item-Typen. Typ je Item nach einer Regel (`model.item_types`): Änderung (GL3) > global (GL1/GL2) > composite
(> 1 Granule) > Vergleich mit den anderen Items derselben Schublade und Granule: keines → *einzeln*, Unterschied in einer
Kontext-Facette → *Kontext-Variante* (gleiche Variable, andere Bedingung; geht verloren, wenn ungefragt), in einer
Wert-Facette → *gestuft*, sonst → *parallel*. Stand V1:

| | DSQ-2 | RAND-36 | FUNCAP55 | Bell | PGIC |
|---|---|---|---|---|---|
| **Frage** | „How often / how severe … in the past 6 months?“ | „Does your health limit you …?“, „How much of the time …?“ u. a. | „What are the consequences for you if you perform …?“ | Stufe 0–100 wählen | „Since you started …, how has your overall condition changed?“ |
| **Messtyp** | Symptomlast: Häufigkeit 0–4 × Stärke 0–4 | Niveau, Einschränkung, Häufigkeit (9 Formate) | Kosten einer Aktivität 0–6 (ein Format) | Gesamtniveau | Änderung (7 Stufen) |
| **Items / Granules** | 104 / 56 | 36 / 14 | 55 / 1 (EN6) | 1 / 1 (GL2) | 1 / 1 (GL3) |
| **Items pro Granule** | 1,9 | 2,6 | 55 | 1 | 1 |
| **Schubladen** | 66 | 15 | 8 (= Domänen A–H) | 1 | 1 |
| **Item-Typen** | 43 Kontext-Variante · 40 einzeln · 13 parallel · 5 composite · 2 gestuft · 1 global | 15 parallel · 7 Kontext-Variante · 5 global · 4 gestuft · 3 einzeln · 1 composite · 1 Änderung | 55 gestuft | global | Änderung |
| **Verlust im Baum** | 14 Kontext-Schubladen (z. B. Auslöser bei EN4) | 2 Kontext-Schubladen, sonst Wert/Format | keiner: Lastart wird gefragt, Last ist Wert | – | nicht im Baum |

**Kurzprofile.**
- **DSQ-2: viele Variablen.** Je ein bis zwei Items pro Variable. Zwei Items derselben Variable unterscheiden sich meist
  durch eine Bedingung (Auslöser, Körperregion), kaum durch Stufen. Kaum Mitteln.
- **RAND-36: mitteln und abtasten.** Wenige Variablen, mehrere Items pro Skala: parallel bei Energie, Stimmung und
  Gesundheit, gestuft bei Gehstrecke und Treppen. Studien berichten die 8 Skalen.
- **FUNCAP: eine Variable, viele Aktivitäten.** Jedes Item fragt die Kosten derselben Belastbarkeit θ_budget (EN6). Die
  Aktivität setzt die Schwierigkeit, die Domäne A–H ist die Lastart.
- **Bell, PGIC:** je ein Item. Bell ist ein Gesamtniveau, PGIC eine Änderung (nicht im Check-in-Baum).

Die Zahlen sind ein Snapshot; das Plakat (Panel 08) rechnet sie live aus dem xlsx.

---

## 3. Facetten: drei Typen

Eine Facette ist ein Paar Schlüssel → Wert. Ihr **Typ** entscheidet, ob man sie im Baum fragen muss.

**Was eine Facette ist.** Streng genommen ist jede Kombination eine eigene Variable θ_g(c). Die Facette ist der Index
dieser Variablenfamilie, wie ein Adjektiv zum Verb. Anders als Konstrukt → Granule (verschachtelt: jede Granule gehört
zu genau einem Konstrukt) ist Granule × Facette **gekreuzt**: Derselbe Facetten-Wert verbindet sich mit vielen Granules
(trigger: standing mit AU2, AU3, SN4). Die Zerlegung ist eine Hypothese, siehe §9.

| Typ | Was sie beschreibt | Schlüssel (Heuristik) | Beispiel | Geht verloren, wenn ungefragt? |
|---|---|---|---|---|
| **Wert** | Position auf der θ-Achse (= b_i) | load | ein Block / eine Meile | **nein**, s enthält die Position |
| **Format** | wie gefragt wird | measure, pole, anchor, Zeitraum | energy vs fatigue; gestern vs letzte Woche | **nein** für die Bedeutung |
| **Kontext** | Bedingung, unter der θ auftritt | region, trigger, timing, load type, modality, activity, quality, type | Schwindel *nach dem Aufstehen* | **ja** |

**Lemma (Wert-Facetten).** Wenn sich Items nur in einer Wert-Facette unterscheiden, sind sie Stufen b_i desselben θ.
Ein Score s = h(θ) trägt die Position auf der Achse direkt, deshalb geht nichts verloren.

**Messtyp-Regel (Format auf Instrumentebene).** DSQ fragt nach der Symptomlast (Häufigkeit und Stärke), RAND-36 nach
Niveau, Einschränkung und Häufigkeit. Die Bedeutung ist gleich, die Zahlen sind aber nicht 1:1 vergleichbar. Ausgewertet
wird deshalb innerhalb einer Person (standardisiert); Studien werden auf Skalenebene verglichen.

**Grenze der Regel (V1).** Ein Messtyp ist nur dann Format, wenn er die gemessene **Variable nicht ändert**. FUNCAP
„Kosten“ ändert sie: Gefragt wird nicht die Fähigkeit, die die Aktivität verlangt, sondern das Budget, das sie verbraucht.
Bis V1 lief FUNCAP hier als „nur Format“ und war auf PF-, CG- und SN-Granules gemappt. Jetzt: alle 55 Items → EN6, die
Domäne A–H ist die gefragte Kontext-Facette **load type**, die Größe der Aktivität die Wert-Facette load.

Die Typzuordnung nach Schlüssel ist eine Heuristik. Einzelwerte können abweichen, z. B. ist „load: bending“ eher Kontext.

---

## 4. Der Baum

- **Struktur.** Der Baum ist ein gerichteter Graph. Jeder innere Knoten stellt eine Frage, jede Antwort führt zu einem
  Knoten oder zu einem Blatt.
- **Sektion vs. Konstrukt.** Das sind zwei Einteilungen derselben Granules:
  - **Sektion** (Präfix SN, CG, EN …): die Herkunft. Items wurden gesammelt, in Sektionen aufgeteilt und innerhalb der
    Sektion granuliert. Knoten-IDs zählen pro Sektion (CG-N3 = 3. Knoten der Sektion Kognition, nicht Tiefe 3).
  - **Konstrukt** (10, z. B. FAT, PEM, FUN): die Darstellung, also das, was Studien berichten. N0 bietet die Konstrukte,
    darunter folgen die Sektionsbäume.
  - Die beiden Einteilungen sind nicht ineinander geschachtelt: Sektion EN verteilt sich auf FAT (EN1–3), PEM (EN4) und
    FUN (EN5, EN6). FUN sammelt Granules aus PF, EN, MO und GL.
- **Knoten.** Jeder Knoten n trägt einen Zustand (G_n, c_n). G_n sind die Granules, die unter n noch erreichbar sind,
  c_n die bisher beantworteten Facetten (Schlüssel aus A).
- **Blatt.** ℓ ist ein Endknoten, (G_ℓ, c_ℓ) das gespeicherte Mapping.
- **Trefferregel** (für jeden Knoten):
  ```
  trifft(n, i)  ⇔  G_n ∩ M(i) ≠ ∅   ∧   π_A(c_i) ≃ c_n
  ≃ (verträglich) = gleicher Wert  ∨  'unspecified'  ∨  Item trägt den Schlüssel gar nicht
  D(n) = { i | trifft(n, i) }        Items, die Knoten n trifft; für ein Blatt ist D(ℓ) seine Schublade
  L(i) = { ℓ | trifft(ℓ, i) }        Etikett eines Items (nur Blätter)
  ```
- **Das Blatt ist der Treffpunkt.** Der User erreicht es über Fragen (Score → Fragen → Blatt). Items treffen es über
  ihre Granules und die gefragten Facetten (Item → π_A → Blatt). Ungefragte Facetten wirft π_A weg.
- **Doppelpfade.** Mehrere Pfade können zum selben Mapping führen (Heimat-Blatt + „Same leaf as“). Es gilt
  |Pfade| ≥ |Mappings|. Das dient der Bedienbarkeit und ändert die Information nicht.

**Regeln für Knoten**

| | Status | Regel |
|---|---|---|
| R1 | Regel | **Monotonie:** Für ein Kind m von n gilt G_m ⊆ G_n und c_m ⊇ c_n, ohne Widerspruch. |
| R2 | Lemma (aus R1) | D(m) ⊆ D(n). Jeder Knoten ist ein gültiger Endpunkt der Konfiguration, tiefer heißt feiner. |
| R3 | Regel | Eine Facette wird nur gefragt, wenn sie Kontext ist und Items in D(n) trennt. Jeder Schlüssel höchstens einmal pro Pfad. |
| R4 | zulässig | Facette an einem inneren Knoten, wenn sie Items mehrerer Granules teilt, z. B. trigger: standing → AU2, AU3, SN4 (DSQ2-71, -69, -70). Heute nicht genutzt. |

*R1 und R2 am Pfad Schmerz:* PN-N1 (G = {PN1–PN4}, c = {}, 13 Items) → PN-N2 (G = {PN1}, c = {}, 10 Items) →
Blatt Headache (G = {PN1}, c = {region: head}, 3 Items). Items aller Instrumente.

**Konstrukt-Blätter** („… in general“) speichern heute nur das Konstrukt. Nach R2 hätten sie D(n) = alle Items der
Konstrukt-Granules.

Als Interface:
```ts
interface Item { granules: Set<G>; facets: Map<Key, Value> }   // vollständig, aus dem Itemtext
interface Node { granules: Set<G>; asked:  Map<Key, Value> }   // Zustand (G_n, c_n), nur Schlüssel aus A
```

---

## 5. Schubladen (Äquivalenzklassen)

**Definition.** i ~ j ⇔ L(i) = L(j), also wenn genau dieselben Blätter beide Items treffen.

Die Relation ~ ist reflexiv, symmetrisch und transitiv, also eine **Äquivalenzrelation**. Ihre Klassen heißen
**Schubladen**. Jedes Item liegt in genau einer Schublade.

**Intuition.** Jedes Item bekommt als Etikett „welche Blätter treffen mich?“. Items mit gleichem Etikett liegen in derselben Schublade.

**Lemma (Restriktion).** Schränkt man ~ auf ein Instrument ein, bleibt sie eine Äquivalenzrelation. Die Schubladen pro
Instrument sind also die Schnitte der globalen Schubladen mit dem Instrument.

**Drei Einteilungen.** Dieselben Items lassen sich auf drei Stufen zusammenfassen. Zwei Items liegen zusammen, wenn …

| Stufe | … sie haben | DSQ | RAND-36 | FUNCAP |
|---|---|---|---|---|
| E₀ Items | dasselbe Item | 104 | 36 | 55 |
| E₁ Annotation | gleiche Granules M(i) und gleiche Facetten c_i | 99 | 33 | 55 |
| E₂ Schubladen | gleiche Blätter L(i) | 66 | 15 | 8 |

**Lemma (geschachtelt).** E₀ ⊑ E₁ ⊑ E₂: Jede Einteilung ist eine Vergröberung der vorigen. Gleiche Granules und gleiche
Facetten ergeben zwangsläufig gleiche Blätter, also liegt jede E₁-Gruppe komplett in einer Schublade.

Damit lässt sich der Verlust auf zwei Ursachen aufteilen:
- **E₀ → E₁: Verlust durch die Annotation.** Die Items sind im xlsx identisch beschrieben, kein Baum kann sie trennen.
  Meist unterscheiden sie sich nur im Zeitraum, der eine eigene Spalte ist und keine Facette (DSQ2-121 gestern vs DSQ2-124
  letzte Woche), oder sie sind echt parallel (DSQ2-36 vs DSQ2-45). DSQ −5, RAND-36 −3, FUNCAP 0.
- **E₁ → E₂: Verlust durch den Baum.** Die Projektion π_A wirft ungefragte Facetten **aller drei Typen** weg.
  DSQ −33, RAND-36 −18, FUNCAP −47. Bei FUNCAP ist das gewollt: Innerhalb einer Domäne unterscheiden sich die Items nur
  in der Last (Wert-Typ), also verlustfrei.

Die Typzählung der Schubladen (z. B. DSQ 14 Kontext / 5 Wert-Format / 1 parallel) zählt **Schubladen**, nicht Items. Jede
Schublade ist nach dem schwersten Typ benannt, der ihre Items unterscheidet. Der Zeitraum zählt dabei als Format.

**Satz (Auflösung des Baums).** Der Baum kann Schubladen unterscheiden, aber keine Items innerhalb einer Schublade.

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

Ein Score trifft die Granule-Menge G_s (bei Multi-Select mehrere), ein Item trägt M(i). Für einen Treffer müssen die
beiden Mengen nicht gleich sein, sie müssen sich überlappen. Die Güte der Überlappung misst der Jaccard-Index:

```
J(G_s, M(i)) = |G_s ∩ M(i)| / |G_s ∪ M(i)|        1 = identisch, 0 = disjunkt
```

*Beispiel:* Ein User wählt CG1–CG7, DSQ2-80 („difficulty reading after mild activity“) hat {CG4, EN4}. Dann ist J = 1/8.

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
| Zerlegung θ_g(c) = θ_g + δ_g(c) + Rest | Hypothese | Varianten hoch korreliert, gleicher Mechanismus → Facette; sonst getrennte Granules |

**Nach App V1 (nicht jetzt umsetzen)**
- **Neuer Workflow für die Granularisierung.** Der Entwickler ist näher an der Granularisierung beteiligt, es wird
  systematisch vorgegangen:
  1. Die Paper der Instrumente lesen, ein allgemeines Verständnis entwickeln (Konstrukt, Frage, Skala, Auswertung).
  2. Grob überlegen, wie die Verbindung vom Baum zu diesem Instrumenttyp modelliert werden kann und worauf zu achten ist
     (Lehre aus V1: FUNCAP fragt Kosten, nicht Fähigkeit).
  3. Eine Anwendung, in der die KI die Granularisierung vorschlägt, für eine Sektion instrumentübergreifend, eventuell
     direkt pro Konstrukt gruppiert. Der Reviewer sieht alle Items der Sektion samt Originalfrage und Skala des Instruments.
  4. Der Reviewer muss freigeben, erst dann geht es mit der nächsten Sektion bzw. dem nächsten Konstrukt weiter.
  5. Zum Schluss die Tests: blinder Agent (T1) und ein zweiter Test (z. B. blinder Zweit-Annotator für M).
- Die eigene Theorie in die Konventionen von Psychometrie und Statistik übersetzen (Notation und Begriffe).
- Den Baum nach wissenschaftlichen Standards konstruieren, z. B. Guttmans Facet Theory und Cronbachs
  Generalisierbarkeitstheorie. Vorher prüfen, ob neuere Ansätze besser passen (z. B. Messinvarianz-Tests,
  Multilevel- und IRT-Modelle für EMA-Daten).
- Die Zerlegung Variable + Facette pro Granule mit Daten prüfen (Zeile oben).
- Todo: Schmerzregionen (Kopf, Bauch …) sind nach Einschätzung des Users keine Facetten von PN1, sondern eigene
  Granules. Umbauen, wenn der Baum das nächste Mal angefasst wird.

---

## 10. Ausblick: Facetten pro Check-in (nach App V1)

Der User konfiguriert bis zu einem Knoten n, meist einem Blatt (R2: jeder Knoten ist ein gültiger Endpunkt).
Optional nennt er in der Sprachnotiz eines Check-ins Facetten, die D(n) pro Messung verfeinern.

```
Konfiguration:  s endet an Knoten n:  (G_n, c_n),  D = D(n)
Check-in:       (s_t, log_t)                         t Zeitpunkt, s_t Slider-Wert, log_t Sprachnotiz (optional)
Extraktion:     ĉ_t = LLM(log_t),  ĉ_t = ∅ ohne Log   Facetten dieses Check-ins
Verfeinerung:   D_t = { i ∈ D | c_i ≃ ĉ_t } ⊆ D       Items, die zu diesem Check-in passen
Messmodell:     s_t = h(θ_t, c_n ∪ ĉ_t) + ε_t         θ_t: Zustand am Tag t
Auswertung:     x̂_γ = w·x̄_γ + (1 − w)·x̄_D,  w = n_γ / (n_γ + κ)
                γ Facetten-Gruppe, x̄ Mittelwert, n_γ Check-ins in γ, κ Glättung
Falle:          P(Facette erwähnt | θ_t) hängt von θ_t ab
```

*Beispiel:* Score „Crash-Schwere“ endet an Blatt EN4, (G_n, c_n) = ({EN4}, {}), D = 8 DSQ-Items. Check-in s_t = 7 mit
Notiz „Crash, weil ich gestern bei der Verabredung zu lange geredet habe“ → ĉ_t = {trigger: mental} → D_t = {DSQ2-77, DSQ2-103}.

Nach Facetten-Typ:
- **Kontext** (Trigger, Region, Aktivität) verfeinert D. Er kann auch auf andere Granules hinweisen.
- **Wert** („kann nicht staubsaugen, liege im Bett“) verfeinert nicht D, sondern ist ein Anker b_i für den Zahlenwert s_t.

**Auswertungsregel:** Ausgewertet wird auf der feinsten Ebene mit genug Daten, sonst auf D (R2: Obermenge). Partial
pooling statt hartem Umschalten: Bei kleinem n_γ liegt x̂_γ nahe am Schubladen-Mittel.

**Falle:** Facetten fehlen nicht zufällig. Trigger werden vor allem an schlechten Tagen erwähnt. Check-ins mit einer
Facette sind dadurch systematisch schlechter, auch ohne kausalen Effekt (informatives Fehlen).

---

## Symbolindex

Jedes Symbol ist genau einmal definiert, hier steht nur, wo.

| Symbol | Abschnitt | Symbol | Abschnitt |
|---|---|---|---|
| θ_g, c, c_i, i, M(i), S, k, s | 1 | n, G_n, c_n, ℓ, G_ℓ, c_ℓ | 4 |
| x_i, f_i, h, λ, ε, c_s, A, π_A | 1 | trifft, ≃, D(n), L(i), R1–R4 | 4 |
| b_i, a, σ(z), θ_budget, d | 2.2 | ~, E₀–E₂ | 5 |
| agg, Δθ | 2.4, 2.5 | G_s, J | 7 |
| | | sgn(s) | 8 |
| | | t, s_t, log_t, ĉ_t, D_t, θ_t, γ, n_γ, κ, w | 10 |
