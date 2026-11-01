"""Parse the 'Sec *' tabs of mecfs-criteria.xlsx into plain data (single source of truth = the xlsx)."""
import re
import openpyxl

PREFIX_SECTION = {}  # filled by parse(): prefix -> tab


def _blocks(ws):
    """Split a Sec tab into its numbered blocks: {'1': [rows], '2': ..., '4': ..., '5': ...}."""
    out, cur = {}, None
    for row in ws.iter_rows(values_only=True):
        a = row[0]
        if isinstance(a, str) and re.match(r"^[1-5]\. ", a) and all(v is None for v in row[1:]):
            cur = a[0]; out[cur] = []; continue
        if cur and any(v is not None for v in row):
            out[cur].append(row)
    return out


def parse(path):
    wb = openpyxl.load_workbook(path)
    secs = []
    for name in wb.sheetnames:
        if not name.startswith("Sec "):
            continue
        ws = wb[name]
        b = _blocks(ws)
        title = ws["A1"].value
        g = [r for r in b["1"][1:] if r[0]]
        granules = [dict(id=r[0], name=r[1], definition=r[2], wording=r[3]) for r in g]
        prefix = re.match(r"[A-Z]+", granules[0]["id"]).group()
        items = [dict(item=r[0], inst=r[1], ver=r[2], other=r[3], text=r[4], tf=r[5], rf=r[6],
                      granules=r[7], facets=r[8] or "", comp=r[9] or "", note=r[10] or "")
                 for r in b["2"][1:] if r[0]]
        boundary = [dict(item=r[0], inst=r[1], ver=r[2], other=r[3], text=r[4], goes=r[5], why=r[6])
                    for r in b.get("3", [])[1:] if r[0]]
        tree = [dict(node=r[0], parent=r[1], level=r[2], q=r[3], a=r[4], to=r[5], g=r[6] or "")
                for r in b["4"][1:] if r[0] and str(r[0]).startswith(("N0", prefix + "-N"))]
        findings = [r[0] for r in b["5"]]
        secs.append(dict(tab=name, title=title, prefix=prefix, granules=granules, items=items,
                         boundary=boundary, tree=tree, findings=findings))
        PREFIX_SECTION[prefix] = name
    return secs


GRAN_RE = re.compile(r"\b([A-Z]{2}\d+)\b")


def granule_ids(s):
    return GRAN_RE.findall(s or "")


if __name__ == "__main__":
    import sys
    for s in parse(sys.argv[1]):
        print(s["tab"], s["prefix"], len(s["granules"]), len(s["items"]), len(s["boundary"]), len(s["tree"]))
