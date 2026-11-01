"""DSQ-1 -> DSQ-2 item equivalence (verified against both PDFs)."""
import re

SUB = {"8a": "8a", "8b": "8b", "11a": "11a", "12a": "12a", "70a": "95a", "70b": "96", "70c": "95b", "70d": "97 + 97a",
       "72a": "99a", "75a": "103", "75b": "103a", "76a": "104a", "83a": "113a", "83b": "113b", "84a": "114a",
       "85a": "115a", "88a": "118a", "90a": "120a–d"}
NONGRID = {67: 92, 68: 93, 69: 94, 70: 95, 71: 98, 72: 99, 73: 100, 74: 101, 75: 102, 76: 104, 77: 106, 78: 107,
           79: 108, 80: 110, 89: "119a–d", 90: 120}

def d1to2(x):
    x = str(x)
    if x in SUB: return SUB[x]
    n = int(x)
    if n <= 40: return str(n)
    if n == 41: return "41 + 42 (split)"
    if 42 <= n <= 51: return str(n + 1)
    if n == 52: return "53 + 54 (split)"
    if 53 <= n <= 66: return str(n + 2)
    if n in NONGRID: return str(NONGRID[n])
    if 81 <= n <= 88 or 91 <= n <= 99: return str(n + 30)
    raise KeyError(x)

def d2to1():
    """reverse map: DSQ-2 id -> DSQ-1 id (single ids only)."""
    rev = {}
    ids = [str(i) for i in range(1, 100)] + list(SUB)
    for i in ids:
        v = d1to2(i)
        for part in re.findall(r"\d+[a-z]?", v.replace("–d", "")):
            if "split" in v:
                rev[part] = f"{i} (part)"
            elif "–" in v:
                for L in "abcd": rev[part[:-1] + L] = i
            else:
                rev.setdefault(part, i)
    return rev
