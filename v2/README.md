# symptom-tree · V2

Ein Check-in-Score einer N-of-1-App wird über einen kurzen Fragebaum auf Items offizieller Instrumente gemappt
(DSQ, RAND-36, FUNCAP, Bell, PGIC). V2 bündelt vier Dinge:

| | Was | Datei |
|---|---|---|
| **Theorie** | Messmodell: Variable θ, Facetten c, Item-Typen, Projektion, Schubladen, Kriterium | `THEORY.md` |
| **Kommunikation** | Lernplakat zur Theorie · Baum mit Granule-Register | `out/theory-poster.svg` · `out/mecfs-tree.svg` |
| **Exploration** | Mapping-Explorer: Granule → Blätter → Items, Schubladen pro Instrument | `out/mapping-explorer.html` |
| **Tests** | T1: blinder Agent läuft mit dem Itemtext als Score-Name durch den Baum | `tests/t1/` |

## Eine Quelle für alles

```
data/mecfs-criteria.xlsx  (Sec-Tabs = Ground Truth)
  └─ pipeline/sections.py ─ pipeline/merge.py ─▶ data/mecfs-criteria_merge.json
                                                   ├─ svg_tree.py       ▶ out/mecfs-tree.svg
                                                   ├─ build_explorer.py ▶ out/mapping-explorer.html
                                                   ├─ build_poster.py   ▶ out/theory-poster.svg
                                                   └─ tests/t1/make_blind.py ▶ blinder Baum für T1
```

Nach jeder Änderung in den Sec-Tabs:

```bash
./build.sh
```

Geteilte Logik (Facetten-Typen, Schubladen, Auflösungskette) liegt in `pipeline/model.py`. Explorer und Plakat rechnen
damit dieselben Zahlen.

- **Regeln** stehen im xlsx, Tab `Method`. Die Merged-Tabs (`All granules`, `All items`, `Full tree`) werden generiert und
  nie von Hand bearbeitet.
- Neue Sektion: ein Dict in `SECTIONS` in `pipeline/sections.py` ergänzen.
- `out/` ist generiert, wird aber eingecheckt, damit man Plakat und Explorer ohne Build öffnen kann.

## Explorer benutzen

`out/mapping-explorer.html` im Browser öffnen, es ist eine Datei ohne Server. Direktlinks: `#k-DSQ`, `#k-R36`, `#k-F55`
(Schubladen), `#g-PF2` (Granule), `#i-DSQ2-71` (Item).

## Voraussetzungen

Python 3 mit `openpyxl`. Für T1 optional zusätzlich `anthropic`.
