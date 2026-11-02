# T1 – Prompt für den blinden Agenten

Der Agent sieht **nur** den blinden Baum (`blind` aus `make_blind.py`, ohne Granule-IDs) und die Itemtexte.
`{TREE}` und `{ITEMS}` werden ersetzt (das macht `run_haiku.py`; bei Claude-Code-Subagenten per Hand einfügen).

---

You are testing a question tree for a symptom-tracking app. A user has created a check-in score and gives it a name.
The tree asks what the score measures. Your job: for each score name below, walk the tree like a thoughtful patient would.

Rules
- Start at Q01. At each question pick the option(s) that fit the score name best.
- Pick SEVERAL options only if the score name clearly covers several of them (e.g. "pain in muscles and joints").
  Then you must follow EVERY picked branch to its END.
- Follow "→ Qxx" to the next question; "→ END" finishes that branch.
- Do not guess what is behind an option; decide from the option text.
- For each step give a short reason (max 12 words).

Tree
{TREE}

Score names (id: text)
{ITEMS}

Answer with JSON only, no prose:
[{"id": "<item id>", "steps": [{"q": "Q01", "picked": [<option numbers>], "why": "<reason>"}, ...]}, ...]
