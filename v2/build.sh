#!/usr/bin/env bash
# Ganze Pipeline aus EINER Quelle: die Sec-Tabs in data/mecfs-criteria.xlsx.
# Danach sind Baum-SVG, Theorie-Plakat und Explorer auf demselben Stand.
set -euo pipefail
cd "$(dirname "$0")"
X=data/mecfs-criteria.xlsx
J=data/mecfs-criteria_merge.json
python3 pipeline/sections.py "$X"          # Sec-Tabs (idempotent)
python3 pipeline/merge.py "$X"             # All granules / All items / Full tree + merge.json
python3 pipeline/svg_tree.py "$J" out/mecfs-tree.svg
python3 pipeline/build_explorer.py "$J" out/mapping-explorer.html
python3 pipeline/build_poster.py "$J" out/theory-poster.svg
