import re, subprocess, copy, sys
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

SRC = sys.argv[1]; PDF = sys.argv[2]; OUT = sys.argv[3]

DSQ_SRC = "DSQ-1.pdf (DePaul)"
RAND_SRC = "DSQ-1.pdf appendix 'MOS Survey (SF-36)'; RAND-36 uses same item wording (verify vs rand.org form)"
F27_SRC = "batemanhornecenter.org/wp-content/uploads/2023/12/FUNCAP27-questionnaire.pdf"
BELL_SRC = "Bell-Skala.pdf (German translation; orig. Bell 1995, The Doctor's Guide to CFS, pp. 122 f.)"

rows = []  # Instrument, Version, ID, Section, Item text, Text status, Item type, Response format, Timeframe, Scored in, Source, Notes
def add(*r): rows.append(list(r))

# ---------------- DSQ-1 ----------------
FREQ_SEV = "Frequency 0–4 (none … all of the time) + Severity 0–4 (not present … very severe)"
txt = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True).stdout
lines = txt.splitlines()

# symptom items 13-66: join wrapped lines, strip the 0 1 2 3 4 grid
sym = {}
cur = None
for ln in lines:
    m = re.match(r"^(\d{2})\)\s+(.*)$", ln)
    body = None
    if m and 13 <= int(m.group(1)) <= 66:
        cur = int(m.group(1)); body = m.group(2); sym[cur] = ""
    elif cur and ln.strip() and not re.match(r"^\s*\d{2}\)", ln) and cur < 67:
        if re.search(r"Frequency|Severity|Throughout|For each|Symptoms|= ", ln) or re.match(r"^\s{20,}\d+\s*$", ln):
            if "Frequency" in ln: cur = None
            continue
        body = ln
    if body is not None and cur:
        body = re.sub(r"(\s+[0-4]){10}\s*$", "", body).strip()
        body = re.sub(r"\s{2,}.*$", "", body) if re.search(r"\s{3,}[0-4]", body) else body
        sym[cur] = (sym[cur] + " " + body).strip()
    if cur == 66 and "chemicals" in ln: cur = None
assert len(sym) == 54, len(sym)

symdom = {}
for i in [13]: symdom[i] = "Fatigue"
for i in range(14, 19): symdom[i] = "Post-exertional malaise"
for i in range(19, 25): symdom[i] = "Sleep"
for i in range(25, 32): symdom[i] = "Pain"
for i in range(32, 45): symdom[i] = "Neurocognitive / neuromuscular / sensory"
for i in range(45, 52): symdom[i] = "Autonomic"
for i in range(52, 62): symdom[i] = "Neuroendocrine"
for i in range(62, 67): symdom[i] = "Immune"

dsq_other = [
 ("1","Demographics","What is your height?","demographic","open"),
 ("2","Demographics","What is your weight?","demographic","open"),
 ("3","Demographics","What is your date of birth?","demographic","open"),
 ("4","Demographics","What is your gender?","demographic","open"),
 ("5","Demographics","To which of the following race(s) do you belong?","demographic","multiple choice (5)"),
 ("6","Demographics","Are you of Latino or Hispanic origin?","demographic","yes/no"),
 ("7","Demographics","What is your current marital status?","demographic","single choice (5)"),
 ("8","Demographics","Do you have any children?","demographic","yes/no"),
 ("8a","Demographics","How many children do you have?","demographic","open"),
 ("8b","Demographics","How many of your children are under 18 years old?","demographic","open"),
 ("9","Demographics","How many people live in your home?","demographic","open"),
 ("10","Demographics","What grade or degree have you completed in school?","demographic","single choice (6)"),
 ("11","Demographics","What is your current work status? (Check all that apply)","demographic / function","multiple choice (7)"),
 ("11a","Demographics","If you are on disability, for what condition do you receive disability compensation?","demographic","open"),
 ("12","Demographics","What is your current occupation?","demographic","open"),
 ("12a","Demographics","If you are currently not working, what was your most recent occupation?","demographic","open"),
]
for i, sec, t, typ, rf in dsq_other:
    add("DSQ","DSQ-1",i,sec,t,"verbatim",typ,rf,"current","—",DSQ_SRC,"")
for i in range(13, 67):
    add("DSQ","DSQ-1",str(i),"Symptoms – "+symdom[i],sym[i],"verbatim","symptom",FREQ_SEV,"past 6 months",
        "Case-definition scoring (DePaul syntax)",DSQ_SRC,"Domain grouping provisional – verify vs DePaul scoring syntax")

YN_NP = "yes / no / not having a problem with fatigue/energy"
dsq_hist = [
 ("67","Illness history","Have you always had persistent or recurring fatigue/energy problems, even back to your earliest memories as a child? (By persistent or recurring, we mean that the fatigue/energy problems are usually ongoing and constant, but sometimes there are good periods and bad periods.)","history",YN_NP,"lifetime"),
 ("68","Illness history","Since your fatigue/energy related illness began, do your headaches either happen more often, feel worse or more severe, or are they in a different place or spot?","symptom (change)",YN_NP,"since onset"),
 ("69","Illness history","How long ago did your problem with fatigue/energy begin?","history","single choice (6)","—"),
 ("70","Illness history","Have you been diagnosed with Chronic Fatigue Syndrome or Myalgic Encephalomyelitis?","history","yes/no","lifetime"),
 ("70a","Illness history","If yes, what year were you diagnosed?","history","open","—"),
 ("70b","Illness history","Do you currently have a diagnosis of Chronic Fatigue Syndrome or Myalgic Encephalomyelitis?","history","yes/no","current"),
 ("70c","Illness history","Who diagnosed you with Chronic Fatigue Syndrome or Myalgic Encephalomyelitis?","history","Medical Doctor / Alternative Practitioner / Self-Diagnosed","—"),
 ("70d","Illness history","Have any of your family members been diagnosed with Chronic Fatigue Syndrome or Myalgic Encephalomyelitis? If yes, please list their relation to you and current age","history","yes/no + open","—"),
 ("71","Illness history","Did you experience any of the following symptoms regularly and repeatedly in the months and years before your fatigue/energy problems began? [Sore throat; Tender/sore lymph nodes; Unrefreshing sleep; Impaired memory and concentration; Prolonged fatigue following physical or mental exertion; Muscle pain; Headaches; Joint Pain; Not having a problem with fatigue/energy]","history (pre-onset symptoms)","multiple choice (9)","before onset"),
 ("72","Fatigue characteristics","If you rest, does your problem with fatigue/energy go away? (Check one)","symptom characteristic","Entirely / Partially / not improved by rest / no problem","current"),
 ("72a","Fatigue characteristics","How long do you have to rest for your problem with fatigue/energy to entirely or partially go away?","symptom characteristic","<30 min / 30–59 min / 1–2 h / >2 h","current"),
 ("73","PEM","If you were to become exhausted after actively participating in extracurricular activities, sports, or outings with friends, would you recover within an hour or two after the activity ended?","symptom (PEM)","yes/no","current"),
 ("74","PEM","Do you reduce your activity level to avoid experiencing problems with fatigue/energy?","behaviour (pacing)",YN_NP,"current"),
 ("75","PEM","Do you experience a worsening of your fatigue/energy related illness after engaging in minimal physical effort?","symptom (PEM)",YN_NP,"current"),
 ("75a","PEM","Do you experience a worsening of your fatigue/energy related illness after engaging in mental effort?","symptom (PEM)","yes/no","current"),
 ("75b","PEM","If you feel worse after activities, how long does this last? (Check one)","symptom (PEM duration)","≤1 h / 2–3 h / 4–10 h / 11–13 h / 14–23 h / >24 h (specify)","current"),
 ("76","Activity","Are you currently engaging in any form of exercise?","behaviour","yes/no","current"),
 ("76a","Activity","If you do not exercise, why aren’t you exercising? (Check all boxes that you agree with)","behaviour","multiple choice (4)","current"),
 ("77","Illness history","Over what period of time did your fatigue/energy related illness, develop? (Check one)","history (onset)","single choice (8)","—"),
 ("78","Illness history","How would you describe the course of your fatigue/energy related illness? (Check one)","history (course)","single choice (6)","—"),
 ("79","Function","Which statement best describes your fatigue/energy related illness during the last 6 months? (Check one)","function (global level)","single choice (7 levels, bedridden … no problems)","past 6 months"),
 ("80","Illness history","Did your fatigue/energy related illness start after you experienced any of the following? (Check one or more and please specify)","history (trigger)","multiple choice (8)","—"),
 ("81","Medical history","Have you ever consulted a medical doctor or health professional about your fatigue/energy problem?","history","yes/no","lifetime"),
 ("82","Medical history","Do you currently have a medical doctor overseeing your fatigue/energy problem?","history","yes/no","current"),
 ("83","Medical history","Do you have any medical illness (es) that might be causing your symptoms?","exclusion","yes/no","current"),
 ("83a","Medical history","What medical illnesses do you have? Illness name(s) and year it began:","exclusion","open","—"),
 ("83b","Medical history","For which of these conditions are you currently receiving treatment?","exclusion","open","current"),
 ("84","Medical history","Are you currently taking any medications (over the counter or prescription)?","exclusion","yes/no","current"),
 ("84a","Medical history","What medications are you taking?","exclusion","open","current"),
 ("85","Medical history","Do you think any medication(s) is (are) causing your problem with fatigue/energy?","exclusion","yes / no / no problem","current"),
 ("85a","Medical history","Please specify which medications:","exclusion","open","current"),
 ("86","Medical history","Have you ever been diagnosed and/or treated for any of the following: (Check all that apply and write year (s) experienced, years treated, and medication (if applicable) in the blank)","exclusion","multiple choice (12) + open","lifetime"),
 ("87","Illness attribution","What do you think is the cause of your problem with fatigue/energy? (Check one)","attribution","single choice (6)","—"),
 ("88","Illness attribution","Do you think anything specific in your personal life or environment accounts for your problem with fatigue/energy?","attribution","yes / no / no problem","—"),
 ("88a","Illness attribution","Please specify:","attribution","open","—"),
 ("89","Function","In the past 4 weeks, approximately how many hours per week have you spent doing: Household / Social/Recreational / Family / Work related activities?","function (activity hours)","4 × hours per week","past 4 weeks"),
 ("90","Function","In the past 4 weeks, have you had to reduce the number of hours you previously spent (prior to your illness) on occupational, social or family activities because of your health or problems with fatigue/energy?","function (reduction)",YN_NP,"past 4 weeks"),
 ("90a","Function","Before your fatigue/energy related illness, approximately how many hours did you used to spend on: Household / Social/Recreational / Family / Work related activities?","function (pre-illness hours)","4 × hours per week","pre-illness"),
 ("91","Energy ratings","Please rate the amount of energy you had available yesterday, using a scale from 1 to 100 where 1= no energy and 100 = your pre-illness energy level. (If you don't have a fatigue/energy related illness, a score of 100 = having abundant energy such that you could work full time and complete your family responsibilities)","symptom (energy available)","1–100","yesterday"),
 ("92","Energy ratings","Please rate the amount of energy you expended (used) yesterday, using a scale from 1 to 100 where 1 = no energy and 100 = your pre-illness energy expended","function (energy expended)","1–100","yesterday"),
 ("93","Energy ratings","Please rate the amount of fatigue you had yesterday, using a scale from 1 to 100 where 1 = no fatigue and 100 = severe fatigue","symptom (fatigue)","1–100","yesterday"),
 ("94","Energy ratings","For the past week, please rate the amount of energy you had available using a scale from 1 to 100 where 1 = no energy and 100 = your pre-illness energy level","symptom (energy available)","1–100","past week"),
 ("95","Energy ratings","For the past week, please rate the amount of energy you have expended (used) using a scale from 1 to 100 where 1 = no energy and 100 = your pre-illness energy expended","function (energy expended)","1–100","past week"),
 ("96","Energy ratings","For the past week, please rate the amount of fatigue you have had using a scale from 1 to 100 where 1 = no fatigue and 100 = severe fatigue","symptom (fatigue)","1–100","past week"),
 ("97","Function","Since the onset of your problems with fatigue/energy, have your symptoms caused a 50% or greater reduction in your activity level?","function (substantial reduction)",YN_NP,"since onset"),
 ("98","Immune","Do you experience frequent viral infections with prolonged recovery periods?","symptom (immune)","yes/no","—"),
 ("99","Thermoregulation","Are you intolerant of extremes of temperatures (when it is extremely hot or cold)?","symptom (neuroendocrine)","yes/no","—"),
]
for i, sec, t, typ, rf, tf in dsq_hist:
    add("DSQ","DSQ-1",i,sec,t,"verbatim",typ,rf,tf,"Case-definition scoring where applicable",DSQ_SRC,"")

# ---------------- DSQ-2 ----------------
sys.path.insert(0, __import__("os").path.dirname(__file__))
from dsqmap import d1to2, d2to1
DSQ2_PDF = sys.argv[6]
DSQ2_SRC = "DSQ-2 REDCap version PDF (DePaul)"
t2 = subprocess.run(["pdftotext", "-layout", DSQ2_PDF, "-"], capture_output=True, text=True).stdout
q2 = {}; order = []; cur = None; last = 0; mode = None
for ln in t2.splitlines():
    if re.search(r"projectredcap|^\s+Page \d+$|DSQ-2 \(Continued\)", ln): cur = None; continue
    if not ln.strip(): cur = None; continue
    ind = len(ln) - len(ln.lstrip())
    mh = re.match(r"^\s{0,5}(\d{1,3})\s+(\S.*)$", ln)
    ms = re.match(r"^\s{3,6}([a-d])\.\s+(.*)$", ln)
    if mh and int(mh.group(1)) == last + 1:
        last = int(mh.group(1)); cur = str(last); q2[cur] = mh.group(2).strip(); order.append(cur); continue
    if ms and last:
        cur = f"{last}{ms.group(1)}"; q2[cur] = ms.group(2).strip(); order.append(cur); continue
    if cur and ind <= 6 and not ln.strip().startswith(("(", "_", "Frequency", "Severity")):
        q2[cur] += " " + ln.strip()
    elif ind >= 7 or ln.strip().startswith(("(", "_", "Frequency", "Severity")):
        cur = None
assert last == 129, last
rev = d2to1()
d1rows = {r[2]: r for r in rows if r[1] == "DSQ-1"}
NEW2 = {  # id: (section, item type, response format, timeframe)
 "5a": ("Demographics","demographic","open","current"),
 "103b": ("PEM","symptom (PEM duration)","hours (open)","current"),
 "105": ("PEM","symptom (PEM)","yes/no","hypothetical"),
 "109": ("Immune","symptom (immune, change)","single choice (4)","since onset"),
 "119": ("Function","function (activity hours)","see a–d","past 4 weeks"),
}
NEWSYM = {69:"Autonomic (orthostatic)",70:"Autonomic (orthostatic)",71:"Autonomic (orthostatic)",72:"Immune / sensitivities",
          73:"Neuroendocrine",74:"Immune",75:"Post-exertional malaise",76:"Post-exertional malaise",77:"Post-exertional malaise",
          78:"Neurocognitive",79:"Neurocognitive",80:"Post-exertional malaise / neurocognitive",81:"Pain",82:"Pain",83:"Pain",
          84:"Sleep",85:"Neurocognitive / sensory",86:"Neuromuscular",87:"Immune",88:"Autonomic (urinary)",89:"Autonomic (urinary)",
          90:"Autonomic (orthostatic)",91:"Neuroendocrine"}
def d1_equiv(i2):
    v = rev.get(i2)
    if v is None: return None
    return v.replace(" (part)", "")
for i2 in order:
    text = q2[i2]
    n = int(re.match(r"\d+", i2).group())
    eq1 = rev.get(i2) if i2 != "119" else "89 (stem)"
    if 13 <= n <= 91 and i2.isdigit():
        if n <= 68:
            base = d1rows[d1_equiv(i2)]; sec = base[3]
        else:
            sec = "Symptoms – " + NEWSYM[n]
        add("DSQ","DSQ-2",i2,sec,text,"verbatim (symptom name; frequency/severity stems in PDF)","symptom",FREQ_SEV,"past 6 months",
            "Case-definition scoring (DePaul syntax)",DSQ2_SRC,"" if eq1 else "New in DSQ-2")
    else:
        if eq1 and i2 != "119":
            b = d1rows[d1_equiv(i2)]
            add("DSQ","DSQ-2",i2,b[3],text,"verbatim",b[6],b[7],b[8],b[9],DSQ2_SRC,"")
        else:
            sec, typ, rf, tf = NEW2[i2]
            add("DSQ","DSQ-2",i2,sec,text,"verbatim",typ,rf,tf,"Case-definition scoring where applicable",DSQ2_SRC,"" if eq1 else "New in DSQ-2")
    rows[-1].append(f"DSQ-1: {eq1}" if eq1 else "new in DSQ-2")
for r in rows:
    if r[1] == "DSQ-1": r.append("DSQ-2: " + d1to2(r[2]))

# ---------------- RAND-36 ----------------
LIM = "1 Yes, limited a lot / 2 Yes, limited a little / 3 No, not limited at all"
YN = "1 Yes / 2 No"
TIME6 = "1 All of the time … 6 None of the time"
TF5 = "1 Definitely true / 2 Mostly true / 3 Don't know / 4 Mostly false / 5 Definitely false"
EXT5 = "1 Not at all / 2 Slightly / 3 Moderately / 4 Quite a bit / 5 Extremely"
rand = [
 (1,"General health","In general, would you say your health is:","1 Excellent … 5 Poor","—","General health"),
 (2,"Health change","Compared to one year ago, how would you rate your health in general now?","1 Much better … 5 Much worse","vs 1 year ago","not in a scale (health change)"),
]
pf = ["Vigorous activities: running, lifting heavy objects, participating in strenuous sports",
 "Moderate activities: moving a table, pushing a vacuum cleaner, bowling, playing golf",
 "Lifting or carrying groceries","Climbing several flights of stairs","Climbing one flight of stairs",
 "Bending, kneeling, or stooping","Walking more than a mile","Walking several blocks","Walking one block",
 "Bathing or dressing yourself"]
for k, t in enumerate(pf):
    rand.append((3+k,"Physical functioning","Does your health now limit you in these activities? If so, how much? – "+t,LIM,"now","Physical functioning"))
rp = ["Cut down on the amount of time you spent on work or other activities","Accomplished less than you would like",
 "Were limited in the kind of work or other activities","Had difficulty performing the work or other activities (For example, it took extra effort)"]
for k, t in enumerate(rp):
    rand.append((13+k,"Role limitations – physical","Problems with your work or other regular daily activities as a result of your physical health: "+t,YN,"past 4 weeks","Role limitations due to physical health"))
re_ = ["Cut down the amount of time you spent on work or other activities","Accomplished less than you would like",
 "Didn’t do work or other activities as carefully as usual"]
for k, t in enumerate(re_):
    rand.append((17+k,"Role limitations – emotional","Problems with your work or other regular daily activities as a result of any emotional problems (such as feeling depressed or anxious): "+t,YN,"past 4 weeks","Role limitations due to emotional problems"))
rand += [
 (20,"Social functioning","To what extent has your physical health or emotional problems interfered with your normal social activities with family, neighbors, or groups?",EXT5,"past 4 weeks","Social functioning"),
 (21,"Pain","How much bodily pain have you had during the past 4 weeks?","1 None / 2 Very mild / 3 Mild / 4 Moderate / 5 Severe / 6 Very severe","past 4 weeks","Pain"),
 (22,"Pain","How much did pain interfere with your normal work (including both work outside the home and housework)?",EXT5,"past 4 weeks","Pain"),
]
ewb = [(23,"Did you feel full of pep?","Energy/fatigue"),(24,"Have you been a nervous person?","Emotional well-being"),
 (25,"Have you felt so down in the dumps that nothing could cheer you up?","Emotional well-being"),
 (26,"Have you felt calm and peaceful?","Emotional well-being"),(27,"Did you have a lot of energy?","Energy/fatigue"),
 (28,"Have you felt down-hearted and blue?","Emotional well-being"),(29,"Did you feel worn out?","Energy/fatigue"),
 (30,"Have you been a happy person?","Emotional well-being"),(31,"Did you feel tired?","Energy/fatigue")]
for n, t, sc in ewb:
    rand.append((n,sc,"How much of the time during the past 4 weeks – "+t,TIME6,"past 4 weeks",sc))
rand.append((32,"Social functioning","How much of the time has your physical health or emotional problems interfered with your social activities (like visiting with friends, relatives, etc.)?","1 All of the time … 5 None of the time","past 4 weeks","Social functioning"))
for k, t in enumerate(["I seem to get sick a little easier than other people","I am as healthy as anybody I know",
                       "I expect my health to get worse","My health is excellent"]):
    rand.append((33+k,"General health","How TRUE or FALSE is each of following statements for you? – "+t,TF5,"—","General health"))
rand.sort(key=lambda r: r[0])
for n, sec, t, rf, tf, sc in rand:
    typ = "symptom" if sc in ("Pain","Energy/fatigue","Emotional well-being") and n != 22 else ("global" if sc in ("General health","not in a scale (health change)") else "function")
    note = "Only indirect cognition link (attributed to emotional problems)" if n == 19 else ""
    add("RAND-36","RAND-36 v1",str(n),sec,t,"verbatim (stem condensed)",typ,rf,tf,sc,RAND_SRC,note)

# ---------------- FUNCAP27 (paraphrased placeholder) ----------------
F_SCALE = "0 Cannot do this … 6 Unproblematic, doesn't affect other activities (7 levels; consequence-based)"
F_SCALE = "0 I cannot do this / 1 My capacity will be severely reduced for at least three days / 2 I can do little else on the same day and for one to two days afterwards / 3 I can do little else on the same day / 4 I must limit other activities on the same day / 5 This rarely affects other activities / 6 Unproblematic – does not affect other activities"
F_STEM = "What are the consequences for you if you perform the activities described below? To what extent does this affect how much else you can do? – "
f27 = [
 ("A","Personal hygiene / basic functions",["Using the toilet (not bedpan or bedside commode)","Showering standing up","Getting dressed in regular clothes"]),
 ("B","Walking – moving around",["Walking a short distance indoors, from one room to another","Walking between approx. 100 m and 1 km on level ground (length of 1 to 10 football fields)","Physical activity with increased heart rate, for approx. 15 min"]),
 ("C","Being upright",["Sitting in bed for approx. ½ hour","Sitting in an upright chair (dining chair) with feet on floor for approx. 2 hours","Standing up for approx. 5 minutes, e.g. while queuing or while cooking"]),
 ("D","Activities in the home",["Heavier housework (washing floors, vacuuming etc.) for approx. 1/2 hour continuously","Cooking a complicated meal from scratch, approx. 1 hour of preparation"]),
 ("E","Communication",["Having a conversation for approx. 5 minutes","Participating in a conversation with three people for approx. 1/2 hour","Participating in a dinner party, party or family event"]),
 ("F","Activities outside your home",["Stepping right outside your home","Going to a shop for groceries","Using public transport (bus or train)","Participating in organized leisure activities such as classes, sports etc."]),
 ("G","Reactions to light and sound",["Staying in a room with normal lighting, without sunglasses, for approx. 1 hour","Staying outdoors in daylight without sunglasses for approx. 2 hours","Staying in a noisy environment, (shopping mall, café or open plan office) for approx. 1 hour"]),
 ("H","Concentration",["Reading a short text, such as a mobile phone text message","Reading and understanding a non-fiction text, such as an official document one A4 page long","Using social media to stay in touch with others","Focusing on a task for approx. 10 minutes continuously","Focusing on a task for approx. 2 hours continuously","Managing a full working day (non-physical work such as office work, classes or lectures)"]),
]
n = 1
for d, dn, items in f27:
    for t in items:
        add("FUNCAP","FUNCAP27",str(n),f"{d} {dn}",t,"verbatim (stem in Notes)","function",F_SCALE,
            "average day during the last month","Domain "+d+" sub-score; total = mean of A–H","FUNCAP27 questionnaire PDF (Sommerfelt et al.)",
            "Stem: "+F_STEM.strip(" –"))
        n += 1


# ---------------- FUNCAP55 (parsed from PDF) ----------------
F55PDF = sys.argv[4]; BELLPDF = sys.argv[5]
t55 = subprocess.run(["pdftotext", "-layout", F55PDF, "-"], capture_output=True, text=True).stdout
body = t55[t55.index("Personal hygiene"):]
items55 = {}; dom = None; curn = None; domname = {}
for ln in body.splitlines():
    m_d = re.match(r"^\s*([A-H])\s+([A-Z][a-z].*)$", ln)
    m_i = re.match(r"^\s*(\d{1,2})\s+(\S.*)$", ln)
    if ln.strip().startswith("Personal hygiene"): dom = "A"; domname["A"] = ln.strip(); continue
    if m_d and not m_i: dom = m_d.group(1); domname[dom] = m_d.group(2).strip(); curn = None; continue
    if m_i and int(m_i.group(1)) == (curn or len(items55)) + 1 and dom and not re.match(r"^\s*0\s+1\s+2", ln):
        curn = int(m_i.group(1)); items55[curn] = [dom, m_i.group(2).strip()]; continue
    if curn and ln.strip() and not re.match(r"^[\s0-6]+$", ln):
        items55[curn][1] += " " + ln.strip()
assert sorted(items55) == list(range(1, 56)), sorted(items55)
txt27 = {t.rstrip("."): i for i, t in enumerate([t for _, _, its in f27 for t in its], start=1)}
for k in range(1, 56):
    d, t = items55[k]
    in27 = txt27.get(t.rstrip("."))
    add("FUNCAP","FUNCAP55",str(k),f"{d} {domname[d]}",t,"verbatim (stem in Notes)","function",F_SCALE,
        "average day during the last month","Domain "+d+" sub-score; total = mean of A–H","FUNCAP_English_55.pdf (Supplementary S2)",
        (f"Same as FUNCAP27 item {in27}. " if in27 else "") + "Stem: "+F_STEM.strip(" –"))

# ---------------- Bell (paraphrased placeholder) ----------------
tb = subprocess.run(["pdftotext", "-layout", BELLPDF, "-"], capture_output=True, text=True).stdout
bell = {}; cur = None
for ln in tb.splitlines():
    m = re.match(r"^(\d{1,3}) Punkte\s+(.*)$", ln)
    if m: cur = int(m.group(1)); bell[cur] = m.group(2).strip()
    elif cur is not None and ln.strip(): bell[cur] += " " + ln.strip()
assert sorted(bell) == list(range(0, 101, 10)), sorted(bell)
for lvl in sorted(bell, reverse=True):
    note = "Contains cognition content" if lvl in (20, 10) else ("Mentions mental exertion (geistige Belastung)" if lvl == 90 else "")
    add("Bell","Bell CFIDS Disability Scale",str(lvl),"Single item – response level",bell[lvl],"verbatim (German version)",
        "function (global level, incl. symptoms)","pick one level 0–100 (steps of 10)","current","Bell score",BELL_SRC,note)

# ---------------- PGIC ----------------
add("PGIC","PGIC (full 7-point, own wording)","1","Global change","Since you started '<protocol name>', how has your overall condition changed? (Think of your symptoms, your energy and what you can manage day to day.)","OWN WORDING – full version, provisional",
    "global change",
    "1 Very Much Improved – A great deal better, and a considerable improvement that has made all the difference / "
    "2 Much Improved – Better, and a definite improvement that has made a real and worthwhile difference / "
    "3 Minimally Improved – Somewhat better, but the change has not made any real difference / "
    "4 No Change – Status remains exactly the same / "
    "5 Minimally Worse – A little worse, but no noticeable or impactful difference / "
    "6 Much Worse – Definitively worse, making a noticeable negative difference / "
    "7 Very Much Worse – A great deal worse, representing a severe decline in clinical status",
    "since protocol start","PGIC (single item)","user-supplied list (bipolar 7-point with descriptions)",
    "Decision: full version first, simplify later. Hybrid: labels CGI-I/PGI-I style, descriptions partly Hurst & Bolton PGIC. Stem decided: anchor = protocol start (PGI-I logic), domains from Hurst & Bolton condensed to symptoms / energy / daily function; 'overall condition' instead of a diagnosis name so it works without ME/CFS diagnosis.")

# ---------------- write ----------------
wb = openpyxl.load_workbook(SRC)
if "Instrument items" in wb.sheetnames: del wb["Instrument items"]
ws = wb.create_sheet("Instrument items", index=wb.sheetnames.index("Criteria") + 1)
hdr = ["Instrument","Version","Item ID","Section / domain","Item text","Text status","Item type","Response format","Timeframe","Scored in","Source","Notes","Other version"]
ws.append(hdr)
ref = wb["DSQ outcome items"]["A1"]
for c in ws[1]:
    c.font = copy.copy(ref.font); c.fill = copy.copy(ref.fill); c.alignment = Alignment(vertical="center", wrap_text=True)
warn = PatternFill("solid", fgColor="FFFCE8B2")
for r in rows:
    ws.append(r)
    if not r[5].startswith("verbatim"):
        ws.cell(ws.max_row, 6).fill = warn
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(vertical="top", wrap_text=True)
widths = [11,20,8,30,70,22,22,36,18,30,40,40,22]
for i, w in enumerate(widths): ws.column_dimensions[openpyxl.utils.get_column_letter(i+1)].width = w
ws.freeze_panes = "A2"
last = ws.max_row
ws.auto_filter.ref = f"A1:M{last}"
ws.append([])
ws.append(["Count", f'=COUNTA(C2:C{last})', "verbatim:", f'=COUNTIF(F2:F{last},"verbatim*")', "DSQ-1 symptom items:", f'=COUNTIFS(B2:B{last},"DSQ-1",G2:G{last},"symptom")', "DSQ-2 symptom items:", f'=COUNTIFS(B2:B{last},"DSQ-2",G2:G{last},"symptom")'])
ws.append(["Excluded instruments (COMPASS-31, MFI-20, FSS, PROMIS, Chalder) not listed: license pending, verbatim text not sourceable. SF-36 = RAND-36 wording. CDC SI / CGI excluded for content."])
wb.save(OUT)
from collections import Counter
print(len(rows), Counter(r[0] for r in rows))
for i in (14,26,38,41,48,56,66): print(i, sym[i])
