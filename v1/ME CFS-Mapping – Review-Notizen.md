# ME/CFS-Mapping – Review-Notizen

Oct 31, 2026 · @Alexander Hallmann

## So liest du das

Sammelstelle für alles, was du in `mecfs-criteria.xlsx` gegenlesen solltest. Wird nach jeder Section ergänzt. Jeder Punkt hat einen Typ:

- **Prüfen** – Zuordnung, bei der ich unsicher bin oder die du fachlich bestätigen solltest
- **Kompromiss** – bewusst vereinfacht zugunsten der Bedienbarkeit; psychometrisch/mechanistisch nicht ganz sauber
- **Hinweis** – Konsequenz für App-Design oder Auswertung, keine Mapping-Frage

Tab- und Item-IDs beziehen sich auf die xlsx (z. B. `Sec Immune`, `DSQ2-109`).

## Übergreifend

| Typ | Punkt | Konsequenz |
| --- | --- | --- |
| Hinweis | **Gemessen vs. eingeschätzt:** Wearable-Puls/HRV (→ AU3) und Körpergewicht (→ NE7) haben kein Symptom-Item, hängen nur am nächstliegenden Granule. | Umgesetzt im Merge: eigene Leaves (Puls per Uhr/Sensor, Gewicht per Waage) mit Flag „measured, not rated“; 0 Instrument-Items, nie mit DSQ-Werten poolen. |
| Hinweis | **Check-in vs. periodischer Fragebogen:** Infekt-Items (IM5), Gewicht (NE7), Binär-Items der Falldefinition (z. B. DSQ2-101, -127, -129) ändern sich über Monate. | Nicht in tägliche EMA, sondern in periodische Fragebögen (z. B. monatlich). Schlaf-Items gehören in die Morgenabfrage. |
| Kompromiss | **Zwei-Pol-Granules:** EN1 (müde↔energiegeladen), MO1 (ängstlich↔ruhig), MO2 (niedergeschlagen↔glücklich), NE7 (ab↔zunehmen), IM5 (DSQ2-109 als Gegenpol). | Funktioniert nur, wenn die Richtungsfrage nach dem Leaf zuverlässig beantwortet wird. |
| Prüfen | **Abgefragte Facets** (Ausnahme von „Facets nie fragen“): Pain region, Function activity, Autonomic Blase, Temperature Schwitzen + Gewicht. | Jede Ausnahme verlängert den Baum um eine Frage. Gegenlesen, ob alle nötig sind. |
| Hinweis | **Measure type** unterscheidet sich je Instrument: DSQ = Häufigkeit/Schwere, FUNCAP = Kosten, RAND-36 = Einschränkung. | Gleiches Granule ≠ vergleichbare Werte. Pooling nur within-person standardisiert. |
| Hinweis | **Granules ohne Item:** MO4 Stress (CG9 hat seit DSQ-2 ein Item, 78). | Erreichbar im Baum, aber nur persönlich auswertbar. |

## Pro Section

| Section | Typ | Punkt |
| --- | --- | --- |
| Sensory | Prüfen | DSQ2-70 (verschwommen/Tunnelblick nach Aufstehen) = SN4 mit Trigger „standing“. Ein Score „verschwommen sehen“ matcht dadurch auch das orthostatische Item. |
| Sensory | Kompromiss | Gerüche/Chemikalien stehen im Baum unter „Sinne“, leiten aber auf IM6 um (Unverträglichkeit, keine Wahrnehmung). |
| Function | Prüfen | Strukturentscheidung: Aktivitäten (Duschen, Kochen, Einkaufen) sind keine Granules, sondern Facet „activity“ auf PF1–PF3. Dadurch fast alle FUNCAP A/D/F-Items Composite. |
| Function | Kompromiss | RAND-36 8 (Bücken/Knien) auf PF3 als nächstliegendes Granule; eigentlich Beweglichkeit + Haltungswechsel. |
| Function | Hinweis | PF5 Pacing ist Verhalten, keine Fähigkeit. Nur behalten, weil Nutzer es tracken. |
| Autonomic | Prüfen | GI und Blase in Autonomic statt eigener Sections (DSQ-Gruppierung, kurzer Baum). Mechanistisch ist z. B. Reizdarm nicht rein autonom. |
| Autonomic | Kompromiss | DSQ2-51 „Dizziness“ als Präsynkope gelesen, nicht als Drehschwindel. |
| Autonomic | Hinweis | POTS-Score wäre Composite AU1 + AU3; kein eigenes Granule. |
| Neuromuscular | Prüfen | DSQ2-49 (unsicher auf den Beinen) → NM4, obwohl DSQ es unter Autonomic führt. Ursache kann orthostatisch oder motorisch sein. |
| Temperature | Kompromiss | Schwitzen (NE5) und kalte Gliedmaßen (NE1) sind mechanistisch autonom, für Nutzer aber beim Temperatur-Cluster. |
| Temperature | Prüfen | NE8 Alkoholunverträglichkeit: Mechanismus unklar, nur DSQ-Gruppierung gefolgt. |
| Immune | Kompromiss | IM6 (Gerüche, Chemikalien, Schimmel) in Immune, weil DSQ es so gruppiert; immunologischer Mechanismus nicht belegt. |
| Immune | Prüfen | IM5 bündelt Häufigkeit, Erholung, Anfälligkeit und DSQ2-109 „keine Erkältungen mehr“ als Gegenpol. |
| Mood | Kompromiss | „Glücklich“ als Gegenpol zu „niedergeschlagen“ (MO2). Positive Affektivität und Depressivität sind teils getrennte Konstrukte; RAND-36 wertet MHI-5 aber als eine Skala. |
| Mood | Hinweis | MO4 Stress ohne Item, nur damit Stress-Scores nicht bei Angst (MO1) landen. |

### Global

| Typ | Punkt |
| --- | --- |
| Hinweis | Der häufigste eigene Score („wie geht es mir heute insgesamt“) landet in GL1. Die passenden Items (RAND-36 1, 34, 36) fragen allgemein bzw. 4 Wochen ab → nur konzeptuell vergleichbar. |
| Hinweis | Bell = ein Item mit 11 Stufen (10er-Schritte): zu grob für tägliches Tracking, gut als periodischer Snapshot. |
| Hinweis | Änderungs-Items (PGIC, RAND-36 2) brauchen einen Anker (Protokollstart bzw. 1 Jahr). Gehören ans Blockende, nicht in EMA. |
| Kompromiss | RAND-36 35 „I expect my health to get worse“ misst Erwartung, nicht Zustand. Trotzdem GL1, damit die General-health-Skala berechenbar bleibt; ebenso 33 als Composite mit IM5. |
| Prüfen | Die oberste Baumebene hat jetzt 12 Kategorien. Umgesetzt im Merge: 8 Bereiche + „mehrere“, siehe Abschnitt Merge. |

### Merge (Schritt 12)

| Typ | Punkt |
| --- | --- |
| Prüfen | **N0-Gruppierung:** 12 Kategorien → 8 Bereiche + „Several of these areas“. Overall, Energy, Thinking, Sleep, Pain, Function, Mood bleiben oben; Senses, Muscles, Autonomic, Temperature, Immune liegen unter „Other body symptoms“ (BD-N1, +1 Frage). Max. 4 Fragen bis zum Leaf (+ Richtungsfrage). Reihenfolge = erwartete Häufigkeit eigener Scores. |
| Prüfen | **„Several of these areas“** an N0: Multi-Select, danach wird jeder gewählte Zweig durchlaufen. Bei 3+ Bereichen wird das lang – evtl. auf 2 Bereiche begrenzen. |
| Prüfen | **Redirect „How mentally exhausted I get“** (Cognition) → jetzt direkt EN3 (mentale Ermüdbarkeit) statt Sprung in die Energy-Section. Falls eher der Crash nach geistiger Anstrengung gemeint ist, wäre EN4 richtig. |
| Prüfen | **DSQ2-2 (Körpergewicht)** ist als demografisch geführt, wäre aber das passende Item für den Leaf „My weight itself (from a scale)“ (NE7). Mappen oder demografisch lassen? |
| Kompromiss | **Facet-Matching bei abgefragten Facets:** Ein Item matcht, wenn es denselben Wert hat, „unspecified“ ist oder gar kein Facet dieses Knotens trägt. Folge: RAND-36 21 (Schmerz allgemein) matcht jede Region, DSQ2-46 (Blase allgemein) matcht „Drang“ und „nachts“. Ausnahme „activity“ (strikt): nur Items mit genau dieser Aktivität. |
| Hinweis | **Dedupe:** 6 Items standen in zwei Tabs (DSQ2-15, -18, -70; F55-32, -52; R36-33). Keine Widersprüche, nur unvollständige Listen; jetzt Union, z. B. DSQ2-15 = EN4 + PN1, F55-32 = CG2/4/7 + SN2. |
| Hinweis | **Coverage:** 247 Outcome-Items (DSQ-2, FUNCAP55, RAND-36, Bell, PGIC): 197 gemappt (35 Composite), 11 ausgeschlossen, 39 keine Outcomes (Demografie, Anamnese, Ausschluss, Attribution, 119-Stem), 0 unbehandelt. Einziges Granule ohne Item: MO4. Bell/PGIC zählen jetzt in allen Coverage-Spalten. |
| Hinweis | Neue Tabs `All granules`, `All items`, `Full tree` werden von `merge.py` erzeugt – Änderungen immer in `sections.py`, dann beide Skripte laufen lassen. |

## Entscheidungen zum Gegenlesen

| Thema | Entscheidung | Begründung |
| --- | --- | --- |
| DSQ2-75 Muskelermüdung nach leichter Aktivität | EN2 (Ermüdbarkeit) | Kraftverlust durch Nutzung, keine systemische Verschlechterung; PEM = 76/77; konsistent mit DSQ-1 17 |
| DSQ2-79 verlangsamtes Sprechen | nur CG3 | Misst Tempo, nicht Formulierung (CG7); kein Sprechmotorik-Item in irgendeinem Instrument |
| PGIC-Stem | „Since you started '\<protocol name>', how has your overall condition changed? (Think of your symptoms, your energy and what you can manage day to day.)“ | Anker Protokollstart (PGI-I-Logik); Domänen nach Hurst & Bolton verdichtet; ohne Diagnosename |
| GI + Blase | Teil von Autonomic (AU5–AU8) | DSQ-Gruppierung; oberste Baumebene bleibt kurz |
| Neuromuskulär | eigene Section (NM1–NM4) | anderer Mechanismus als autonom |

## Noch offen

- [ ] „Rules added after pilots“ im Tab `Method` gegenlesen (inkl. neuer Regel „Facet activity“)
- [ ] FUNCAP: Höflichkeits-Mail an die Autoren
- [ ] Bell: Nutzungsbedingungen verifizieren
- [ ] Merge-Entscheidungen (Abschnitt Merge, Typ „Prüfen“) gegenlesen
