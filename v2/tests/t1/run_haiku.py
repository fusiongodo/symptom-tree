"""T1 runner: send the blind tree + items to a model, write the run JSON for score.py.
usage: run_haiku.py <blind.json> <run_out.json> [--model claude-haiku-5-5] [--batch 12]
Needs: pip install anthropic, env ANTHROPIC_API_KEY.  (Not yet run in this repo – the RAND-36 pilot used Claude Code subagents.)"""
import argparse, json, os, re
import anthropic

ap = argparse.ArgumentParser()
ap.add_argument("blind"); ap.add_argument("out")
ap.add_argument("--model", default="claude-haiku-5-5"); ap.add_argument("--batch", type=int, default=12)
a = ap.parse_args()
B = json.load(open(a.blind))
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "PROMPT.md"), encoding="utf-8").read().split("---", 1)[1]
client = anthropic.Anthropic()
run = []
for k in range(0, len(B["items"]), a.batch):
    chunk = B["items"][k:k + a.batch]
    prompt = tpl.replace("{TREE}", B["blind"]).replace("{ITEMS}", "\n".join(f'{i["id"]}: {i["text"]}' for i in chunk))
    msg = client.messages.create(model=a.model, max_tokens=8000, messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if b.type == "text")
    run += json.loads(re.search(r"\[.*\]", text, re.S).group(0))
    print(f"{min(k + a.batch, len(B['items']))}/{len(B['items'])}")
json.dump(run, open(a.out, "w"), ensure_ascii=False, indent=0)
print("written", a.out, len(run), "items")
