# T1 – Baum-Validierung mit einem blinden Agenten

**Frage:** Führt der Baum zu dem Blatt, das unser Mapping erwartet, wenn jemand nur den Itemtext als Score-Namen kennt?

Der Agent sieht den Baum ohne Granule-IDs („blind“). Bewertet wird pro Item:

| Urteil | Bedeutung |
|---|---|
| exact | Ein erreichtes Blatt enthält genau dieses Item |
| granule | Richtige Granule, aber das Item wird über eine Facette herausgefiltert |
| construct | Richtiges Konstrukt, andere Granule |
| miss | Falsches Konstrukt |

## Ablauf

```bash
J=../../data/mecfs-criteria_merge.json
python3 make_blind.py $J RAND-36 blind_rand36.json          # 1. blinder Baum + Items  (DSQ | RAND-36 | FUNCAP)
python3 run_haiku.py blind_rand36.json run_rand36.json       # 2. Agent-Lauf (oder: Subagent mit PROMPT.md)
python3 score.py blind_rand36.json run_rand36.json $J t1_rand36.html "RAND-36 · Haiku"   # 3. Report + CSVs
```

- **Schritt 2 mit API:** `run_haiku.py` braucht `pip install anthropic` und `ANTHROPIC_API_KEY`. Das Skript ist noch nicht gelaufen.
- **Schritt 2 ohne API:** Einen Claude-Code-Subagenten (Modell Haiku) mit `PROMPT.md` starten. `{TREE}` wird durch das
  Feld `blind`, `{ITEMS}` durch die Itemliste ersetzt. Die Antwort als `run_*.json` speichern.
- Mehrere Läufe (z. B. 3) machen Zufallsschwankungen sichtbar.

## Pilot

`pilot_rand36/`: RAND-36 mit Haiku, 32/35 exakt, 3 auf Konstrukt-Ebene (R36-5, R36-7, R36-16). R36-2 ist ein
Änderungsitem und nicht im Baum.

## Nächste Tests

- T1 für DSQ und FUNCAP, mit schärferer Multi-Pick-Anweisung (steht in `PROMPT.md`), 3 Läufe.
- Test 3 (Mapping M): Ein blinder Zweit-Annotator bekommt Granule-Definitionen und Items und ordnet Granules zu. Reviewt
  werden nur die Abweichungen.
