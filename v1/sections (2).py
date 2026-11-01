"""Generic section builder: one tab per section, identical layout, prefixed node IDs for later merge."""
import sys, copy
import openpyxl
from openpyxl.styles import Alignment, PatternFill

WB = sys.argv[1]
wb = openpyxl.load_workbook(WB)
ITEMS = {(r[1], r[2]): r for r in wb["Instrument items"].iter_rows(min_row=2, values_only=True) if r[1]}
sys.path.insert(0, __import__("os").path.dirname(__file__))
from dsqmap import d1to2
INST = {"DSQ-1": ("DSQ", "DSQ1"), "DSQ-2": ("DSQ", "DSQ2"), "FUNCAP55": ("FUNCAP", "F55"), "RAND-36 v1": ("RAND-36", "R36"),
        "Bell CFIDS Disability Scale": ("Bell", "BELL"),
        "PGIC (full 7-point, own wording)": ("PGIC", "PGIC")}

# styles captured from the original pilot tab (kept as style source)
src = wb["Pilot Sleep"] if "Pilot Sleep" in wb.sheetnames else wb["Sec Sleep"]
ST = {k: (copy.copy(src[c].font), copy.copy(src[c].fill)) for k, c in
      dict(title="A1", note="A2", sec="A3", hdr="A4", body="B6").items()}

def item_row(ver, iid):
    r = ITEMS[(ver, str(iid))]
    return r[4], r[8], r[7]  # text, timeframe, response format

def short_rf(rf):
    return rf if len(rf) <= 60 else rf[:57] + "…"

# =====================================================================
SECTIONS = []

# ---------------------------------------------------------------- SLEEP
SECTIONS.append(dict(
 tab="Sec Sleep", title="Section: Sleep", prefix="SL",
 intro="Only the DSQ has sleep items. RAND-36, Bell and FUNCAP have none (FUNCAP's authors state it does not assess symptoms such as unrefreshing sleep). Rebuilt verbatim from the sleep pilot.",
 granules=[
  ("SL1","Sleep onset difficulty","Taking long to fall asleep.","Trouble falling asleep"),
  ("SL2","Sleep maintenance difficulty","Waking up during the night and staying awake.","Waking up during the night"),
  ("SL3","Early waking","Waking much earlier than intended and not falling asleep again.","Waking up too early"),
  ("SL4","Unrefreshing sleep","Not feeling rested after sleep, regardless of duration.","Waking up unrested"),
  ("SL5","Daytime sleepiness / sleep need","Feeling drowsy or needing to sleep or nap during the day.","Being sleepy or needing to nap during the day"),
  ("SL6","Reversed sleep rhythm","Sleeping mainly by day and being awake at night.","Day and night mixed up"),
 ],
 items=[("DSQ-1",19,None,"SL4","","",""),("DSQ-1",20,None,"SL5","","",""),("DSQ-1",21,None,"SL1","","",""),
        ("DSQ-1",22,None,"SL2","","",""),("DSQ-1",23,None,"SL3","timing: e.g. 3am","",""),("DSQ-1",24,None,"SL6","","",""),
        ("DSQ-2",84,None,"SL5","quality: drowsiness","","New in DSQ-2")],
 boundary=[("DSQ-2",89,None,"→ Autonomic","Waking at night to urinate: a cause of night waking (SL2 trigger), primary in Autonomic (AU8)")],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Sleep","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","Something that happens at night","N2",""),
  ("N1","N0",1,None,"How rested or sleepy I am during the day","N3",""),
  ("N2","N1",2,"Which one does '<score name>' measure?","How hard it was to fall asleep","leaf","SL1"),
  ("N2","N1",2,None,"How often or long I was awake in the night","leaf","SL2"),
  ("N2","N1",2,None,"How much too early I woke up","leaf","SL3"),
  ("N2","N1",2,None,"How much my sleep shifted into the day","leaf","SL6"),
  ("N2","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N3","N1",2,"Which one does '<score name>' measure?","How unrested I feel after waking","leaf","SL4"),
  ("N3","N1",2,None,"How sleepy I am or how much I need to nap in the day","leaf","SL5"),
  ("N3","N1",2,None,"Both together","multi-select","composite"),
 ],
 findings=[
  "• Granules are 1:1 with DSQ items: no composites, no facets needed. DSQ-2 adds daytime drowsiness (84) → SL5 widened from nap need to sleepiness/sleep need; no split.",
  "• Sleep items are retrospective ('last night'); in the app they belong in a morning question, not in random check-ins.",
 ]))

# ------------------------------------------------------------ COGNITION
SECTIONS.append(dict(
 tab="Sec Cognition", title="Section: Cognition", prefix="CG",
 intro="Cross-instrument stress test: DSQ-1 (symptoms, past 6 months) vs FUNCAP55/27 (activity cost, last month). FUNCAP27 items are a subset of FUNCAP55 (column 'FUNCAP27 #').",
 granules=[
  ("CG1","Sustained attention","Keeping attention on one thing over a period of time.","Staying focused on one thing"),
  ("CG2","Divided attention","Attending to more than one thing at once (e.g. several speakers, task + interruption).","Following several things at once"),
  ("CG3","Processing speed","How fast thinking runs; slowed thought.","How fast my thinking is"),
  ("CG4","Comprehension","Taking in and understanding information, read or heard.","Understanding what I read or hear"),
  ("CG5","Memory","Retaining and recalling information; everyday forgetting.","Remembering things"),
  ("CG6","Word finding","Retrieving the right word when speaking or writing.","Finding the right words"),
  ("CG7","Expression","Putting thoughts into spoken or written language.","Putting thoughts into words"),
  ("CG8","Mental manipulation","Holding information in mind and working with it (e.g. mental arithmetic).","Working things out in my head"),
  ("CG9","Confusion / disorientation","Losing orientation or the thread: not knowing where/when, feeling muddled.","Feeling confused or disoriented"),
 ],
 items=[
  ("DSQ-1",36,None,"CG5","","",""),
  ("DSQ-1",37,None,"CG1","load: long","",""),
  ("DSQ-1",38,None,"CG6, CG7","modality: speaking","yes","Item bundles word finding + expressing thoughts"),
  ("DSQ-1",39,None,"CG4","","",""),
  ("DSQ-1",40,None,"CG2","","","Phrased as limit: only one thing at a time"),
  ("DSQ-2",42,"DSQ-1: 41 (part)","CG1","","","Split from DSQ-1 41 (vision and/or attention), now clean"),
  ("DSQ-1",43,None,"CG3","","",""),
  ("DSQ-1",44,None,"CG5","","","Absent-mindedness read as everyday forgetting; verify boundary vs CG1"),
  ("DSQ-2",78,None,"CG9","","","New in DSQ-2; first item for CG9"),
  ("DSQ-2",79,None,"CG3","modality: speaking; quality: slowed","","New in DSQ-2. Decided CG3 only: item measures output RATE, CG7 is formulation (what is said). Pauses from word finding would be CG6, which was never mapped either → CG7 was inconsistent. Motor slowing (dysarthria) checked in Neuromuscular: no speech-motor item in any instrument, DSQ places it in the neurocognitive block → stays CG3"),
  ("DSQ-2",80,None,"CG4, EN4","modality: reading; trigger: mild physical or mental activity","yes","New in DSQ-2; reading difficulty as PEM consequence"),
  ("FUNCAP55",26,None,"CG7","modality: speaking; load: minimal","","At this load mainly energy/motor cost"),
  ("FUNCAP55",27,12,"CG4, CG7","modality: conversation; load: 5 min","yes",""),
  ("FUNCAP55",28,None,"CG4, CG7, CG1","modality: conversation; load: 30 min","yes",""),
  ("FUNCAP55",29,None,"CG7","modality: handwriting; load: short","","Also fine-motor demand"),
  ("FUNCAP55",30,13,"CG4, CG7, CG2","modality: conversation (3 people); load: 30 min","yes",""),
  ("FUNCAP55",31,None,"CG4, CG7, CG1","modality: conversation; load: 1 h","yes","Also social/physical context"),
  ("FUNCAP55",32,14,"CG4, CG7, CG2","modality: conversation (group)","yes","Also noise, being upright → multi-section composite"),
  ("FUNCAP55",46,22,"CG4","modality: reading (screen); load: minimal","",""),
  ("FUNCAP55",47,None,"CG4, CG1","modality: reading; load: open","yes",""),
  ("FUNCAP55",48,23,"CG4","modality: reading; load: 1 A4 page, complex","",""),
  ("FUNCAP55",49,None,"CG8","load: simple","",""),
  ("FUNCAP55",50,None,"CG7","modality: writing (screen); load: short","",""),
  ("FUNCAP55",51,24,"CG4, CG7","modality: reading + writing (screen)","yes",""),
  ("FUNCAP55",52,None,"CG4, CG1","modality: audiovisual (screen)","yes","Also light/sound → Sensory section"),
  ("FUNCAP55",53,25,"CG1","load: 10 min","",""),
  ("FUNCAP55",54,26,"CG1","load: 2 h","",""),
  ("FUNCAP55",55,27,"CG1","load: full working day","yes","Global cognitive endurance + sitting; CG1 as nearest granule"),
 ],
 boundary=[
  ("DSQ-2",41,"DSQ-1: 41 (part)","→ Sensory/vision","Visual focus; split from DSQ-1 41"),
  ("DSQ-2",85,None,"→ Sensory","Vibration sensitivity (new in DSQ-2)"),
  ("DSQ-1",16,None,"→ Energy","Mental fatigability (tiring from mental effort), not a cognitive ability"),
  ("DSQ-1","75a",None,"→ Energy","PEM after mental effort"),
  ("DSQ-1",34,None,"→ Sensory","Noise sensitivity"),
  ("DSQ-1",35,None,"→ Sensory","Light sensitivity"),
  ("DSQ-1",42,None,"→ Sensory/vision","Depth perception"),
  ("FUNCAP55","40–45","19–21","→ Sensory","Domain G (light and sound) – tolerance, not cognition"),
  ("DSQ-1",71,None,"excluded","Pre-onset history checklist ('Impaired memory and concentration'), not an outcome"),
  ("RAND-36 v1",19,None,"excluded","'as carefully as usual' attributed to emotional problems; too unspecific"),
  ("Bell CFIDS Disability Scale","90/20/10",None,"→ Global","Single global item; cognition only as anchor wording in levels"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Thinking / cognition","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","My concentration","N2",""),
  ("N1","N0",1,None,"How fast and clearly I think and understand","N3",""),
  ("N1","N0",1,None,"My memory","N4",""),
  ("N1","N0",1,None,"Language: words and expressing myself","N5",""),
  ("N1","N0",1,None,"How mentally exhausted I get","→ EN","(redirect)"),
  ("N1","N0",1,None,"General brain fog / a mix of several","multi-select","composite"),
  ("N2","N1",2,"Which one does '<score name>' measure?","Staying focused on one thing","leaf","CG1"),
  ("N2","N1",2,None,"Following several things at once","leaf","CG2"),
  ("N2","N1",2,None,"Both together","multi-select","composite"),
  ("N3","N1",2,"Which one does '<score name>' measure?","How fast my thinking is","leaf","CG3"),
  ("N3","N1",2,None,"Understanding what I read or hear","leaf","CG4"),
  ("N3","N1",2,None,"Feeling confused or disoriented","leaf","CG9"),
  ("N3","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N4","N1",2,"Which one does '<score name>' measure?","Remembering things","leaf","CG5"),
  ("N4","N1",2,None,"Working things out in my head","leaf","CG8"),
  ("N4","N1",2,None,"Both together","multi-select","composite"),
  ("N5","N1",2,"Which one does '<score name>' measure?","Finding the right words","leaf","CG6"),
  ("N5","N1",2,None,"Putting thoughts into words","leaf","CG7"),
  ("N5","N1",2,None,"Both together","multi-select","composite"),
 ],
 findings=[
  "• DSQ (symptoms) and FUNCAP (activities) map onto the same granules. CG1, CG2, CG4, CG7 covered by both; CG3, CG5, CG6 DSQ only; CG8 FUNCAP only; CG9 DSQ-2 only (78, new).",
  "• Granule = underlying ability. DSQ asks how impaired it is, FUNCAP what using it costs → compatible by concept, not by value.",
  "• FUNCAP items are mostly composites (activities bundle abilities). Clean 1:1: 46, 48, 49, 50, 53, 54 (+ 26, 29). Facets 'load' and 'modality' keep their differences.",
  "• Mental fatigability and PEM after mental effort → Energy (tree redirects); light/noise and vision → Sensory.",
 ]))

# --------------------------------------------------------------- ENERGY
SECTIONS.append(dict(
 tab="Sec Energy", title="Section: Energy, fatigue and PEM", prefix="EN",
 intro="Instruments: DSQ-1 (symptom grid, PEM block, 1–100 energy ratings), RAND-36 Energy/fatigue scale. FUNCAP's response scale itself encodes PEM cost, but its items are activities → mapped in the Function section.",
 granules=[
  ("EN1","Fatigue / energy level","How tired vs. energetic one feels overall; fatigue and available energy are the two poles of one axis.","How tired or energetic I feel"),
  ("EN2","Physical fatigability","Tiring unusually fast DURING physical effort.","Running out of steam while doing something physical"),
  ("EN3","Mental fatigability","Tiring unusually fast DURING mental effort.","Running out of steam while thinking or concentrating"),
  ("EN4","Post-exertional malaise (crash)","Worsening of symptoms AFTER exertion, often delayed, slow recovery.","How bad my crash is after doing too much"),
  ("EN5","Energy used / activity amount","How much energy was spent or how much was done.","How much I did"),
 ],
 items=[
  ("DSQ-1",13,None,"EN1","pole: fatigue","",""),
  ("DSQ-1",14,None,"EN2","quality: heavy; timing: immediate","","DSQ groups it as PEM, but 'after starting' = during effort → fatigability"),
  ("DSQ-1",15,None,"EN4","trigger: everyday activity; timing: next day","yes","Also muscle soreness → Pain section"),
  ("DSQ-1",16,None,"EN3","trigger: slightest mental effort","",""),
  ("DSQ-1",17,None,"EN2","trigger: minimal exercise","",""),
  ("DSQ-1",18,None,"EN4","trigger: mild activity","yes","'sick' also flu-like malaise → Immune section"),
  ("DSQ-1",73,None,"EN4","measure: recovery time (reverse)","","Binary; case-definition item"),
  ("DSQ-1",75,None,"EN4","trigger: minimal physical effort","","Binary; case-definition item"),
  ("DSQ-1","75a",None,"EN4","trigger: mental effort","","Binary; case-definition item"),
  ("DSQ-1","75b",None,"EN4","measure: duration","","Duration categories"),
  ("DSQ-1",91,None,"EN1","pole: energy","",""),
  ("DSQ-1",93,None,"EN1","pole: fatigue","",""),
  ("DSQ-1",94,None,"EN1","pole: energy","",""),
  ("DSQ-1",96,None,"EN1","pole: fatigue","",""),
  ("DSQ-2",75,None,"EN2","region: muscles; trigger: mild physical activity","","New in DSQ-2. Decided EN2: muscle fatigue = loss of force through use (fatigability, low threshold), not systemic symptom worsening; PEM = 76/77. Consistent with DSQ-1 17 'Minimum exercise makes you physically tired' (also 'after', also EN2)"),
  ("DSQ-2",76,None,"EN4","trigger: mild physical activity","","New in DSQ-2 (graded version of binary 102)"),
  ("DSQ-2",77,None,"EN4","trigger: mild mental activity","","New in DSQ-2 (graded version of binary 103)"),
  ("DSQ-2","103b",None,"EN4","measure: duration (hours)","","New in DSQ-2"),
  ("DSQ-2",105,None,"EN4","trigger: exercise/vigorous activity","","New in DSQ-2; binary, hypothetical"),
  ("DSQ-1",92,None,"EN5","","",""),
  ("DSQ-1",95,None,"EN5","","",""),
  ("RAND-36 v1",23,None,"EN1","pole: energy","",""),
  ("RAND-36 v1",27,None,"EN1","pole: energy","",""),
  ("RAND-36 v1",29,None,"EN1","pole: fatigue","",""),
  ("RAND-36 v1",31,None,"EN1","pole: fatigue","",""),
 ],
 boundary=[
  ("DSQ-1",72,None,"excluded","Characteristic of fatigue (relieved by rest?), used by case definitions; not a trackable level"),
  ("DSQ-1","72a",None,"excluded","Same: rest duration needed"),
  ("DSQ-1",74,None,"→ Function","Pacing behaviour (reducing activity), not a symptom"),
  ("DSQ-1",97,None,"→ Function","50 % activity reduction since onset"),
  ("DSQ-1",33,None,"→ Neuromuscular","Muscle weakness = strength, not fatigue"),
  ("DSQ-2",109,None,"→ Immune","Stopped getting colds/flu (new in DSQ-2)"),
  ("Bell CFIDS Disability Scale","100–0",None,"→ Global","Single global level; mentions symptoms with exertion in all anchors"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Energy / exhaustion","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How tired or energetic I feel overall","leaf","EN1"),
  ("N1","N0",1,None,"How fast I run out of steam while doing something","N2",""),
  ("N1","N0",1,None,"How bad my crash is after doing too much","leaf","EN4"),
  ("N1","N0",1,None,"How much I did / how much energy I used","leaf","EN5"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"While doing what?","Something physical","leaf","EN2"),
  ("N2","N1",2,None,"Thinking or concentrating","leaf","EN3"),
  ("N2","N1",2,None,"Both","multi-select","composite"),
 ],
 findings=[
  "• Key boundary is TIMING: tiring during effort (EN2/EN3, fatigability) vs. worsening after effort (EN4, PEM). The DSQ's 'PEM' block mixes both; mapped by mechanism, not by DSQ heading.",
  "• Fatigue and energy = one granule (EN1) with two poles. RAND-36 already scores them as one scale. The direction rule handles the polarity.",
  "• Depth: mostly category + 1 question; EN2/EN3 need a second. 'Crash' is the community term and clearer than 'PEM'.",
  "• PEM facets: trigger (physical/mental), timing (delay), duration. Not asked; set only if the score name specifies them.",
  "• DSQ-2 adds graded PEM items (76, 77: frequency/severity instead of yes/no) and muscle fatigue (75). All fit EN2/EN4; no split.",
 ]))

# ----------------------------------------------------------------- PAIN
SECTIONS.append(dict(
 tab="Sec Pain", title="Section: Pain", prefix="PN",
 intro="Instruments: DSQ-1 (pain items by body region, headache change), RAND-36 Pain scale (intensity + interference). FUNCAP and Bell have no pain items. Per Method, location is a facet, not a granule.",
 granules=[
  ("PN1","Pain","Physical pain of any kind; where it is located is recorded as the facet 'region'.","How strong the pain is"),
  ("PN2","Pain interference","How much pain gets in the way of daily activities (impact, not intensity).","How much the pain gets in the way"),
  ("PN3","Stiffness","Feeling of restricted, stiff movement (e.g. joints), distinct from pain.","How stiff I feel"),
  ("PN4","Pain sensitivity","Pain from stimuli that normally hurt little or not at all, incl. pain spreading from pressure elsewhere.","How sensitive I am to pain"),
 ],
 items=[
  ("DSQ-1",25,None,"PN1","region: muscles","",""),
  ("DSQ-1",26,None,"PN1, PN3","region: joints (> 1, no swelling/redness); quality: tenderness","yes","Bundles pain, stiffness, tenderness"),
  ("DSQ-1",27,None,"PN1","region: eyes","",""),
  ("DSQ-1",28,None,"PN1","region: chest","",""),
  ("DSQ-1",30,None,"PN1","region: abdomen","",""),
  ("DSQ-1",31,None,"PN1","region: head","",""),
  ("DSQ-2",81,None,"PN1","region: eyes; quality: aching","","New in DSQ-2; overlaps DSQ 27 (eye pain)"),
  ("DSQ-2",82,None,"PN4","","","New in DSQ-2"),
  ("DSQ-2",83,None,"PN4","quality: referred (pressure → pain elsewhere)","","New in DSQ-2"),
  ("DSQ-1",68,None,"PN1","region: head; measure: change since onset","","Binary; case-definition item (new/changed headache)"),
  ("DSQ-1",15,None,"EN4, PN1","region: muscles (soreness); timing: next day","yes","Primary in Energy (PEM); listed here for pain coverage"),
  ("RAND-36 v1",21,None,"PN1","region: whole body (unspecified)","","Matches any region (missing facet ≠ mismatch)"),
  ("RAND-36 v1",22,None,"PN2","","",""),
 ],
 boundary=[
  ("DSQ-1",29,None,"→ Autonomic","Bloating is not pain; AU7"),
  ("DSQ-1",71,None,"excluded","Pre-onset history checklist (muscle pain, headaches, joint pain), not an outcome"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Pain","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How strong the pain is","N2",""),
  ("N1","N0",1,None,"How much the pain gets in the way of my day","leaf","PN2"),
  ("N1","N0",1,None,"How stiff I feel","leaf","PN3"),
  ("N1","N0",1,None,"How sensitive I am to pain","leaf","PN4"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"Where is the pain?","Muscles","leaf","PN1 [region: muscles]"),
  ("N2","N1",2,None,"Joints","leaf","PN1 [region: joints]"),
  ("N2","N1",2,None,"Head","leaf","PN1 [region: head]"),
  ("N2","N1",2,None,"Eyes","leaf","PN1 [region: eyes]"),
  ("N2","N1",2,None,"Chest","leaf","PN1 [region: chest]"),
  ("N2","N1",2,None,"Belly","leaf","PN1 [region: abdomen]"),
  ("N2","N1",2,None,"All over / it moves around","leaf","PN1 [region: unspecified]"),
  ("N2","N1",2,None,"Several places (pick)","multi-select","PN1 [region: several]"),
 ],
 findings=[
  "• First section where items differ ONLY by a facet (region). Without asking, a 'headache' score would map to all pain items. Hence the tree asks 'Where?' here → rule 'Asked facets' (Method tab).",
  "• Intensity vs. interference are separate granules: RAND-36 scores both in one Pain scale, but they measure different things (sensation vs. impact).",
  "• Unspecified region (RAND-36 21, 'all over') matches every region-specific item; a region-specific score matches RAND-36 21 too.",
  "• DSQ 26 bundles pain + stiffness + tenderness → composite. Tenderness = pain on pressure, kept as quality facet.",
  "• DSQ-2 adds pain sensitivity (82) and pressure-induced pain elsewhere (83) → new granule PN4. No split of existing granules.",
 ]))

# ------------------------------------------------------- SENSORY & VISION
SECTIONS.append(dict(
 tab="Sec Sensory", title="Section: Sensory and vision", prefix="SN",
 intro="Instruments: DSQ-2 (sensitivity and vision symptoms), FUNCAP55/27 domain G (cost of light and sound exposure). RAND-36 and Bell have no sensory items. Each sense is its own granule (different sensation); stimulus strength/duration is the facet 'load'.",
 granules=[
  ("SN1","Light sensitivity","Light that others find normal is unpleasant, straining or makes symptoms worse.","Being bothered by light"),
  ("SN2","Noise sensitivity","Sounds that others find normal are unpleasant, straining or make symptoms worse.","Being bothered by noise"),
  ("SN3","Vibration sensitivity","Vibration (e.g. car, train, machines) is unpleasant or makes symptoms worse.","Being bothered by vibration"),
  ("SN4","Visual focus / blurred vision","Eyes cannot focus; the image is blurred or narrowed.","How sharp and clear I see"),
  ("SN5","Depth perception","Judging distances and depth.","Judging distances"),
 ],
 items=[
  ("DSQ-1",35,None,"SN1","","",""),
  ("DSQ-1",34,None,"SN2","","",""),
  ("DSQ-2",85,None,"SN3","","","New in DSQ-2; only item for SN3"),
  ("DSQ-2",41,"DSQ-1: 41 (part)","SN4","","","Split from DSQ-1 41 (vision and/or attention); attention part = DSQ2-42 → CG1"),
  ("DSQ-2",70,None,"SN4","trigger: standing; quality: blurred or tunnel","","New in DSQ-2. Sensation = SN4, standing = trigger facet. Mechanism orthostatic → listed in Autonomic for coverage"),
  ("DSQ-1",42,None,"SN5","","",""),
  ("FUNCAP55",40,None,"SN1","load: dim light, 30 min","",""),
  ("FUNCAP55",41,19,"SN1","load: normal indoor light, 1 h","",""),
  ("FUNCAP55",42,20,"SN1","load: daylight, 2 h","",""),
  ("FUNCAP55",43,None,"SN2","load: quiet conversation","","Also listening (CG4) at low load; noise is the stated domain"),
  ("FUNCAP55",44,21,"SN2","load: noisy environment, 1 h","",""),
  ("FUNCAP55",45,None,"SN2","load: high noise (cinema, concert)","yes","Also outing, sitting upright → multi-section composite"),
  ("FUNCAP55",32,14,"CG4, CG7, CG2, SN2","modality: conversation (group)","yes","Primary in Cognition; SN2 added for noise"),
  ("FUNCAP55",52,None,"CG4, CG1, SN1, SN2","modality: audiovisual (screen)","yes","Primary in Cognition; screen light + sound"),
 ],
 boundary=[
  ("DSQ-1",27,None,"→ Pain","Eye pain: stays PN1 [region: eyes]; tree redirects"),
  ("DSQ-2",81,None,"→ Pain","Aching of/behind the eyes: stays PN1 [region: eyes]"),
  ("DSQ-2",82,None,"→ Pain","Pain sensitivity: stays PN4 (pain, not a sense)"),
  ("DSQ-1",66,None,"→ Immune","Smells/foods/chemicals make you feel sick: intolerance reaction, not perception; tree redirects"),
  ("DSQ-2",72,None,"→ Immune","Sensitivity to mold: same reasoning"),
  ("DSQ-2",71,None,"→ Autonomic","Graying/blacking out after standing: presyncope, not a visual symptom"),
  ("DSQ-1",50,None,"→ Autonomic","Dizziness or fainting"),
  ("DSQ-2",73,None,"→ Temperature","Intolerance to temperature extremes: thermoregulation (section 8)"),
  ("DSQ-2",86,None,"→ Neuromuscular","Poor coordination: motor, not sensory"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Senses and vision","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How much light, noise or vibration bothers me","N2",""),
  ("N1","N0",1,None,"How well I see","N3",""),
  ("N1","N0",1,None,"Pain in or behind my eyes","leaf","PN1 [region: eyes] (redirect)"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"What bothers you?","Light","leaf","SN1"),
  ("N2","N1",2,None,"Noise","leaf","SN2"),
  ("N2","N1",2,None,"Vibration or shaking (e.g. in a car)","leaf","SN3"),
  ("N2","N1",2,None,"Smells or chemicals","leaf","IM6 (redirect)"),
  ("N2","N1",2,None,"Several of these","multi-select","composite"),
  ("N3","N1",2,"Which one does '<score name>' measure?","How sharp and clear I see","leaf","SN4"),
  ("N3","N1",2,None,"Judging distances","leaf","SN5"),
  ("N3","N1",2,None,"Both together","multi-select","composite"),
 ],
 findings=[
  "• Granule = sense, not stimulus strength. FUNCAP G grades load (dim → daylight, quiet → concert); this is the facet 'load', like in Cognition. DSQ asks severity, FUNCAP cost → same granule, values not comparable (measure type rule).",
  "• SN1, SN2 covered by DSQ + FUNCAP; SN3, SN4, SN5 DSQ only. No RAND-36/Bell coverage.",
  "• Smell/chemical items are NOT a sense granule: 'make you feel sick' = intolerance reaction → Immune. Tree still offers 'Smells or chemicals' and redirects, because users will look for it here.",
  "• DSQ2-70 (blurred/tunnel vision after standing): sensation is SN4, standing is a trigger facet. A plain 'blurred vision' score matches 41 and 70 (missing facet ≠ mismatch). Listed again in Autonomic for coverage (same mapping).",
  "• Eye pain stays in Pain; tree reaches it via a cross-section leaf. Depth: category + 2 questions everywhere.",
 ]))

# ------------------------------------------------------ PHYSICAL FUNCTION
_SC, _HW, _OUT = "activity: self-care", "activity: housework", "activity: outing"
SECTIONS.append(dict(
 tab="Sec Function", title="Section: Physical function", prefix="PF",
 intro="Instruments: FUNCAP55/27 domains A–D, F (cost of activities), RAND-36 Physical functioning (limitation) and Role-physical, DSQ-2 function/behaviour items. FUNCAP E/G/H are mapped in Cognition and Sensory. Granules = type of physical load (upright, walking, exertion) plus participation level and pacing; the concrete activity is the facet 'activity'.",
 granules=[
  ("PF1","Upright tolerance","Being able to sit or stand upright for a while without symptoms forcing you to lie down.","How long I can sit or stand"),
  ("PF2","Walking / moving around","Moving on foot; distance, stairs and terrain are the facet 'load'.","How far I can walk"),
  ("PF3","Physical exertion","Activities that need force or raise the heart rate (lifting, carrying, housework, sport).","How much physical effort I can manage"),
  ("PF4","Activity limitation","How much health reduces work and daily activities compared with normal / before illness.","How much my health limits my daily life"),
  ("PF5","Pacing","Deliberately keeping activity below one's limit to avoid crashes (behaviour, not ability).","How well I stay within my limits"),
 ],
 items=[
  ("FUNCAP55",1,None,"PF2, PF1",_SC+"; load: toilet","yes",""),
  ("FUNCAP55",2,None,"PF1, PF3",_SC+"; load: minimal","yes",""),
  ("FUNCAP55",3,None,"PF1, PF3",_SC+"; load: showering seated, assisted","yes",""),
  ("FUNCAP55",4,None,"PF1, PF3",_SC+"; load: showering seated","yes",""),
  ("FUNCAP55",5,None,"PF1, PF3",_SC+"; load: showering standing","yes",""),
  ("FUNCAP55",6,None,"PF1","load: out of bed, 1 h","",""),
  ("FUNCAP55",7,None,"PF1, PF3",_SC+"; load: dressing","yes",""),
  ("FUNCAP55",8,None,"PF2","load: room to room","",""),
  ("FUNCAP55",9,None,"PF2","load: 100 m","",""),
  ("FUNCAP55",10,None,"PF2","load: 100 m – 1 km","",""),
  ("FUNCAP55",11,None,"PF2","load: 1 km level","",""),
  ("FUNCAP55",12,None,"PF2, PF3","load: 1 km hilly","yes","Hilly terrain adds exertion"),
  ("FUNCAP55",13,None,"PF3","activity: exercise; load: raised heart rate, 15 min","",""),
  ("FUNCAP55",14,None,"PF3","activity: exercise; load: raised heart rate, 30 min","",""),
  ("FUNCAP55",15,None,"PF1","load: sitting in bed, 30 min","",""),
  ("FUNCAP55",16,None,"PF1","load: chair, 10 min","",""),
  ("FUNCAP55",17,None,"PF1","load: chair, 2 h","",""),
  ("FUNCAP55",18,None,"PF1","load: standing, 5 min","",""),
  ("FUNCAP55",19,None,"PF1","load: standing, 30 min","",""),
  ("FUNCAP55",20,None,"PF1, PF3",_HW+"; load: light, 30 min","yes",""),
  ("FUNCAP55",21,None,"PF3, PF1",_HW+"; load: heavy, 30 min","yes",""),
  ("FUNCAP55",22,None,"PF1, PF3",_HW+"; load: laundry","yes",""),
  ("FUNCAP55",23,None,"PF1, PF3",_HW+"; load: cold meal","yes",""),
  ("FUNCAP55",24,None,"PF1, PF3",_HW+"; load: simple hot meal","yes",""),
  ("FUNCAP55",25,None,"PF1, PF3",_HW+"; load: complex meal, 1 h","yes","Also planning/multitasking (cognitive), not mapped"),
  ("FUNCAP55",33,None,"PF2",_OUT+"; load: stepping outside","","Threshold item for leaving home"),
  ("FUNCAP55",34,None,"PF2, PF1",_OUT+"; load: necessary errand","yes",""),
  ("FUNCAP55",35,None,"PF2, PF1, PF3",_OUT+"; load: grocery shopping","yes","Carrying; also noise (SN2)"),
  ("FUNCAP55",36,None,"PF2, PF1",_OUT+"; load: leisure (café, shopping)","yes","Also noise, social → multi-section composite"),
  ("FUNCAP55",37,None,"PF1, SN3",_OUT+"; load: car passenger, 15 min","yes","Sitting upright + vibration"),
  ("FUNCAP55",38,None,"PF1, PF2, SN3",_OUT+"; load: public transport","yes",""),
  ("FUNCAP55",39,None,"PF3, PF2",_OUT+"; activity: exercise; load: organised classes/sports","yes",""),
  ("RAND-36 v1",3,None,"PF3","activity: exercise; load: vigorous","",""),
  ("RAND-36 v1",4,None,"PF3",_HW+"; load: moderate","","Examples mix housework and sport"),
  ("RAND-36 v1",5,None,"PF3","load: lifting/carrying groceries","",""),
  ("RAND-36 v1",6,None,"PF2, PF3","load: stairs, several flights","yes",""),
  ("RAND-36 v1",7,None,"PF2","load: stairs, one flight","",""),
  ("RAND-36 v1",8,None,"PF3","load: bending, kneeling, stooping","","Nearest granule; posture change also loads PF1"),
  ("RAND-36 v1",9,None,"PF2","load: > 1 mile","",""),
  ("RAND-36 v1",10,None,"PF2","load: several blocks","",""),
  ("RAND-36 v1",11,None,"PF2","load: one block","",""),
  ("RAND-36 v1",12,None,"PF1, PF3",_SC,"yes",""),
  ("RAND-36 v1",13,None,"PF4","measure: time cut down","",""),
  ("RAND-36 v1",14,None,"PF4","measure: accomplished less","",""),
  ("RAND-36 v1",15,None,"PF4","measure: kind of activity limited","",""),
  ("RAND-36 v1",16,None,"PF4","measure: extra effort needed","",""),
  ("DSQ-1",90,None,"PF4","measure: hours reduced vs pre-illness (binary)","",""),
  ("DSQ-1",97,None,"PF4","measure: ≥ 50 % reduction since onset (binary)","","Case-definition item"),
  ("DSQ-1",74,None,"PF5","measure: binary","","Case-definition item"),
  ("DSQ-2","119a",None,"EN5","activity: household; measure: hours/week","","Primary in Energy (EN5 = how much I did)"),
  ("DSQ-2","119b",None,"EN5","activity: social/recreational; measure: hours/week","",""),
  ("DSQ-2","119c",None,"EN5","activity: family; measure: hours/week","",""),
  ("DSQ-2","119d",None,"EN5","activity: work; measure: hours/week","",""),
  ("DSQ-1",76,None,"EN5","activity: exercise; measure: binary","","Whether one exercises at all = activity amount"),
 ],
 boundary=[
  ("DSQ-2","120a–d",None,"excluded","Pre-illness hours: baseline reference for 120, not trackable"),
  ("DSQ-1","76a",None,"excluded","Reasons for not exercising: attribution, not a level"),
  ("DSQ-1",79,None,"→ Global","Global illness level (bedridden … no problems), like Bell"),
  ("RAND-36 v1","17–19",None,"→ Mood","Role limitations due to emotional problems"),
  ("RAND-36 v1","20, 32",None,"→ Global","Social functioning"),
  ("DSQ-2",90,None,"→ Autonomic","Inability to tolerate upright position = symptom behind PF1; composite there"),
  ("DSQ-1",33,None,"→ Neuromuscular","Muscle weakness"),
  ("DSQ-2",86,None,"→ Neuromuscular","Poor coordination"),
  ("FUNCAP55","26–32, 40–55",None,"done","Domains E, G, H mapped in Cognition / Sensory"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Physical activity and daily function","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","What my body can manage physically","N2",""),
  ("N1","N0",1,None,"A specific everyday activity","N3",""),
  ("N1","N0",1,None,"How much my health limits my work or daily life","leaf","PF4"),
  ("N1","N0",1,None,"How well I stay within my limits (pacing)","leaf","PF5"),
  ("N1","N0",1,None,"How much I did","leaf","EN5 (redirect)"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"Which one does '<score name>' measure?","How long I can sit or stand","leaf","PF1"),
  ("N2","N1",2,None,"How far I can walk","leaf","PF2"),
  ("N2","N1",2,None,"How much physical effort I can manage","leaf","PF3"),
  ("N2","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N3","N1",2,"Which activity?","Washing, dressing, toilet","leaf","PF1, PF3 [activity: self-care]"),
  ("N3","N1",2,None,"Housework or cooking","leaf","PF1, PF3 [activity: housework]"),
  ("N3","N1",2,None,"Getting out of the house (errands, shopping, transport)","leaf","PF1, PF2 [activity: outing]"),
  ("N3","N1",2,None,"Exercise or sport","leaf","PF3 [activity: exercise]"),
  ("N3","N1",2,None,"Several of these","multi-select","composite"),
 ],
 findings=[
  "• Activities are not granules: showering, cooking, shopping bundle the same few physical loads. Granules = load type (PF1 upright, PF2 walking, PF3 exertion); the activity becomes the facet 'activity'. Most FUNCAP A/D/F items are therefore composites.",
  "• 'activity' is an ASKED facet (N3): within PF1/PF3 the FUNCAP items differ mainly by activity, same logic as pain region. A score 'could shower' maps to self-care items only, not to all PF1/PF3 items.",
  "• Three measure types meet: FUNCAP = cost, RAND-36 PF = limitation (3 levels), DSQ = binary/hours. Same granule, values not comparable.",
  "• PF4 (participation) ≠ PF1–3 (capacity): RAND-36 Role-physical and DSQ reduction items say how much less one does, not what the body can do.",
  "• Pacing (PF5) is behaviour; kept because users track it. Hours per activity (DSQ2-119) and exercising yes/no → EN5 'how much I did'.",
  "• Upright tolerance (PF1) is the capacity side of orthostatic intolerance; the symptom side (DSQ2-90, 69–71) follows in Autonomic.",
 ]))

# ------------------------------------------------------------ AUTONOMIC
SECTIONS.append(dict(
 tab="Sec Autonomic", title="Section: Autonomic – circulation, breathing, digestion, bladder", prefix="AU",
 intro="Only the DSQ has autonomic symptom items (COMPASS-31 excluded for license). Includes gastrointestinal and urinary items (DSQ groups them as autonomic). Standing/upright is the facet 'trigger', not part of a granule. Upright CAPACITY is PF1 (Function); this section holds the symptom side.",
 granules=[
  ("AU1","Orthostatic intolerance","Not being able to stay upright; symptoms build up when sitting/standing and ease when lying down.","How badly I tolerate being upright"),
  ("AU2","Light-headedness / fainting","Feeling dizzy or faint, vision greying, nearly or actually passing out.","Feeling dizzy or faint"),
  ("AU3","Palpitations / fast heart","Heart racing, pounding or beating irregularly.","Fast or irregular heartbeat"),
  ("AU4","Shortness of breath","Trouble getting enough air or catching one's breath.","Shortness of breath"),
  ("AU5","Nausea","Feeling sick in the stomach.","Feeling sick (nausea)"),
  ("AU6","Bowel problems","Diarrhoea, constipation or cramping of the bowel.","Bowel problems"),
  ("AU7","Bloating","Feeling of a swollen, full belly.","Bloating"),
  ("AU8","Bladder problems","Problems passing urine: urgency, frequency, waking at night to urinate.","Bladder problems"),
 ],
 items=[
  ("DSQ-2",90,None,"AU1","","","New in DSQ-2; symptom side of PF1"),
  ("DSQ-1",50,None,"AU2","quality: dizziness or fainting","","'Dizziness' read as presyncope (DSQ autonomic block), not vertigo"),
  ("DSQ-2",71,None,"AU2","trigger: standing; quality: greying/blacking out","","New in DSQ-2"),
  ("DSQ-1",51,None,"AU3","quality: irregular","",""),
  ("DSQ-2",69,None,"AU3","trigger: standing; quality: fast","","New in DSQ-2; POTS-type item"),
  ("DSQ-2",70,None,"SN4","trigger: standing; quality: blurred or tunnel","","Primary in Sensory; listed for orthostatic coverage"),
  ("DSQ-1",49,None,"AU4","","",""),
  ("DSQ-1",47,None,"AU5","","",""),
  ("DSQ-1",46,None,"AU6","","","'Irritable bowel problems': bowel function in general"),
  ("DSQ-1",29,None,"AU7","","","DSQ groups it under Pain; mapped by mechanism"),
  ("DSQ-1",45,None,"AU8","quality: unspecified","",""),
  ("DSQ-2",88,None,"AU8","quality: urgency","","New in DSQ-2"),
  ("DSQ-2",89,None,"AU8","timing: night","","New in DSQ-2; also a cause of night waking (SL2)"),
 ],
 boundary=[
  ("DSQ-1",48,None,"→ Neuromuscular","Unsteady on feet, like you might fall: balance; DSQ lists it as autonomic, mechanism unclear (orthostatic or motor)"),
  ("DSQ-1",54,None,"→ Temperature","Sweating hands: sudomotor, but grouped with the sweating/temperature cluster (section 8)"),
  ("DSQ-2",58,None,"→ Temperature","Cold limbs: peripheral vasomotor, grouped with temperature"),
  ("DSQ-1",53,None,"→ Temperature","No appetite: neuroendocrine block (with weight items)"),
  ("DSQ-1",30,None,"→ Pain","Abdominal pain stays PN1 [region: abdomen]; tree redirects"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Heart, breathing, stomach and bladder","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","Heart, circulation or being upright","N2",""),
  ("N1","N0",1,None,"Breathing","leaf","AU4"),
  ("N1","N0",1,None,"Stomach and bowel","N3",""),
  ("N1","N0",1,None,"Bladder","N4",""),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"Which one does '<score name>' measure?","How badly I tolerate being upright","leaf","AU1"),
  ("N2","N1",2,None,"Feeling dizzy or faint","leaf","AU2"),
  ("N2","N1",2,None,"Fast or irregular heartbeat","leaf","AU3"),
  ("N2","N1",2,None,"My heart rate measured by a watch or sensor","leaf","AU3 [measure: device] (measured, not rated)"),
  ("N2","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N3","N1",2,"Which one does '<score name>' measure?","Feeling sick (nausea)","leaf","AU5"),
  ("N3","N1",2,None,"Diarrhoea, constipation, cramps","leaf","AU6"),
  ("N3","N1",2,None,"Bloating","leaf","AU7"),
  ("N3","N1",2,None,"Belly pain","leaf","PN1 [region: abdomen] (redirect)"),
  ("N3","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N4","N1",2,"What about your bladder?","Sudden strong urge to go","leaf","AU8 [quality: urgency]"),
  ("N4","N1",2,None,"Waking up at night to go","leaf","AU8 [timing: night]"),
  ("N4","N1",2,None,"Bladder problems in general","leaf","AU8"),
 ],
 findings=[
  "• GI and urinary items are part of this section (DSQ groups them as autonomic; one category with sub-branches keeps N0 short). Neuromuscular items get their own section.",
  "• 'After standing' items (69, 70, 71) are mapped to their sensation (AU3, SN4, AU2) with trigger: standing. A plain 'heart racing' score matches 52 and 69 (missing facet ≠ mismatch). AU1 is the only granule for upright intolerance itself (DSQ2-90).",
  "• AU8 is an asked facet (N4): bladder items differ only by quality/timing, same logic as pain region.",
  "• Objective wearable data (heart rate, HRV) is not a symptom and has no DSQ item; the tree offers it as its own leaf (N2) on AU3 as nearest granule, flagged 'measured, not rated' (never pooled with DSQ values).",
  "• Section is DSQ-only: no capacity/limitation items (FUNCAP C upright items are PF1).",
 ]))

# --------------------------------------------------------- NEUROMUSCULAR
SECTIONS.append(dict(
 tab="Sec Neuromuscular", title="Section: Neuromuscular – muscles and movement", prefix="NM",
 intro="Only the DSQ has neuromuscular items. RAND-36/FUNCAP measure physical function, not motor symptoms (→ Function). Boundary to Energy: weakness = reduced strength, fatigability = tiring during use (EN2).",
 granules=[
  ("NM1","Muscle weakness","Muscles produce less force than normal, even before tiring.","How weak my muscles are"),
  ("NM2","Muscle twitches","Small involuntary muscle contractions or jerks.","Muscle twitches"),
  ("NM3","Coordination","Precision of movements: clumsy, dropping things, missing targets.","How clumsy I am"),
  ("NM4","Balance / unsteadiness","Keeping stable on one's feet; feeling one might fall.","Feeling unsteady on my feet"),
 ],
 items=[
  ("DSQ-1",33,None,"NM1","","",""),
  ("DSQ-1",32,None,"NM2","","",""),
  ("DSQ-2",86,None,"NM3","","","New in DSQ-2"),
  ("DSQ-1",48,None,"NM4","","","DSQ lists it as autonomic. Unsteadiness can be orthostatic (→ AU2) or motor; sensation is instability → NM4. No composite: a light-headed score maps via AU2"),
 ],
 boundary=[
  ("DSQ-2",75,None,"→ Energy","Muscle fatigue after mild activity = fatigability (EN2), not weakness"),
  ("DSQ-1",25,None,"→ Pain","Muscle pain stays PN1 [region: muscles]; tree redirects"),
  ("DSQ-2",79,None,"→ Cognition","Slowed speech: checked, stays CG3 (no speech-motor item)"),
  ("FUNCAP55",29,None,"→ Cognition","Handwriting: fine-motor demand noted there, mapped CG7"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Muscles and movement","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How weak my muscles are","leaf","NM1"),
  ("N1","N0",1,None,"Muscle twitches","leaf","NM2"),
  ("N1","N0",1,None,"How clumsy I am","leaf","NM3"),
  ("N1","N0",1,None,"Feeling unsteady on my feet","leaf","NM4"),
  ("N1","N0",1,None,"How fast my muscles tire","leaf","EN2 (redirect)"),
  ("N1","N0",1,None,"Muscle pain","leaf","PN1 [region: muscles] (redirect)"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
 ],
 findings=[
  "• Granules are 1:1 with DSQ items; depth = category + 1 question.",
  "• Weakness (NM1) vs fatigability (EN2): reduced maximal force vs. tiring during use. Users mix these → tree offers both and redirects.",
  "• DSQ2-49 (unsteady) sits in the DSQ autonomic block; mapped by sensation to NM4. Orthostatic light-headedness is AU2.",
  "• DSQ2-79 slowed speech: no motor counterpart in any instrument → stays CG3 (decision closed).",
 ]))

# ---------------------------------------------- NEUROENDOCRINE & TEMPERATURE
SECTIONS.append(dict(
 tab="Sec Temperature", title="Section: Neuroendocrine – temperature, sweating, appetite, weight", prefix="NE",
 intro="Only the DSQ has items here. Fever, sore throat, flu-like symptoms → Immune (signs of immune activation). Sweating and cold limbs are autonomic by mechanism but kept with the temperature cluster for the user.",
 granules=[
  ("NE1","Feeling cold / chills","Feeling cold, shivering or having cold hands/feet without a cold environment.","Feeling cold or shivery"),
  ("NE2","Feeling hot / feverish","Feeling as if one has a raised temperature (not a measured fever).","Feeling hot or feverish"),
  ("NE3","Temperature swings","Switching between hot and cold for no reason, over the day.","Swinging between hot and cold"),
  ("NE4","Temperature intolerance","Coping badly with heat or cold in the environment.","Coping badly with heat or cold"),
  ("NE5","Sweating","Sweating more than the situation explains.","Sweating"),
  ("NE6","Appetite loss","Little or no appetite.","Little appetite"),
  ("NE7","Unintended weight change","Weight going down or up without trying; direction = facet 'pole'.","Weight change"),
  ("NE8","Alcohol intolerance","Feeling unusually unwell from small amounts of alcohol.","Reacting badly to alcohol"),
 ],
 items=[
  ("DSQ-1",57,None,"NE1","quality: chills/shivers","",""),
  ("DSQ-1",60,None,"NE1","quality: feeling low temperature","",""),
  ("DSQ-2",58,None,"NE1","region: limbs","","New in DSQ-2"),
  ("DSQ-1",59,None,"NE2","","",""),
  ("DSQ-1",58,None,"NE3","","",""),
  ("DSQ-2",91,None,"NE3","timing: over the day","","New in DSQ-2"),
  ("DSQ-2",73,None,"NE4","","","New in DSQ-2 (graded version of binary 129)"),
  ("DSQ-1",99,None,"NE4","measure: binary","","Case-definition item"),
  ("DSQ-1",54,None,"NE5","region: hands","",""),
  ("DSQ-1",55,None,"NE5","timing: night","",""),
  ("DSQ-1",53,None,"NE6","","",""),
  ("DSQ-2",53,"DSQ-1: 52 (part)","NE7","pole: loss","","Split from DSQ-1 52 (weight change)"),
  ("DSQ-2",54,"DSQ-1: 52 (part)","NE7","pole: gain","","Split from DSQ-1 52 (weight change)"),
  ("DSQ-1",61,None,"NE8","","","Mechanism unclear; DSQ groups it as neuroendocrine"),
 ],
 boundary=[
  ("DSQ-1",64,None,"→ Immune","Fever: measurable sign of immune activation (NE2 = feeling feverish)"),
  ("DSQ-1",65,None,"→ Immune","Flu-like symptoms"),
  ("DSQ-1",98,None,"→ Immune","Frequent viral infections"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Temperature, sweating, appetite and weight","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","Feeling cold or hot","N2",""),
  ("N1","N0",1,None,"Sweating","N3",""),
  ("N1","N0",1,None,"Appetite or weight","N4",""),
  ("N1","N0",1,None,"Reacting badly to alcohol","leaf","NE8"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"Which one does '<score name>' measure?","Feeling cold or shivery","leaf","NE1"),
  ("N2","N1",2,None,"Feeling hot or feverish","leaf","NE2"),
  ("N2","N1",2,None,"Swinging between hot and cold","leaf","NE3"),
  ("N2","N1",2,None,"Coping badly with heat or cold","leaf","NE4"),
  ("N2","N1",2,None,"A measured fever","leaf","IM4 (redirect)"),
  ("N2","N1",2,None,"A mix of several of these","multi-select","composite"),
  ("N3","N1",2,"Where or when?","Sweaty hands","leaf","NE5 [region: hands]"),
  ("N3","N1",2,None,"Sweating at night","leaf","NE5 [timing: night]"),
  ("N3","N1",2,None,"Sweating in general","leaf","NE5"),
  ("N4","N1",2,"Which one does '<score name>' measure?","Little appetite","leaf","NE6"),
  ("N4","N1",2,None,"Losing weight","leaf","NE7 [pole: loss]"),
  ("N4","N1",2,None,"Gaining weight","leaf","NE7 [pole: gain]"),
  ("N4","N1",2,None,"My weight itself (e.g. from a scale)","leaf","NE7 [measure: device] (measured, not rated)"),
 ],
 findings=[
  "• Two asked facets: sweating (region/timing, N3) and weight (pole, N4). Items differ only there, same rule as pain region.",
  "• Weight = one granule with two poles (like EN1). 'My weight itself' (e.g. kg from a scale) matches both items; it is measured, not rated → flag at merge, like wearable heart rate.",
  "• Feeling feverish (NE2) ≠ fever (Immune): sensation vs. measured sign.",
  "• NE3 vs NE1/NE2: swings are their own granule, because DSQ asks them separately (58, 91) and users track 'temperature regulation' as one thing.",
 ]))

# ---------------------------------------------------------------- IMMUNE
SECTIONS.append(dict(
 tab="Sec Immune", title="Section: Immune – feeling ill, infections, sensitivities", prefix="IM",
 intro="Instruments: DSQ-2 (immune symptom items, infection history), RAND-36 one General-health item on getting sick easily. Sensitivity to smells/chemicals/mold is grouped here as in the DSQ; mechanism (immune vs. other) is unresolved.",
 granules=[
  ("IM1","Sore throat","Pain or scratchiness in the throat.","Sore throat"),
  ("IM2","Tender lymph nodes","Swollen or tender glands, e.g. neck, armpits.","Swollen or tender glands"),
  ("IM3","Flu-like feeling","Feeling ill as with flu: aching, feverish, run-down.","Feeling flu-like"),
  ("IM4","Fever","Raised body temperature (ideally measured; NE2 = only feeling feverish).","Fever"),
  ("IM5","Infections","How often one gets infections and how long recovery takes.","How often I get infections"),
  ("IM6","Chemical / smell sensitivity","Feeling sick from smells, chemicals, foods, medication or mold.","Reacting to smells, chemicals or foods"),
 ],
 items=[
  ("DSQ-1",62,None,"IM1","","",""),
  ("DSQ-1",63,None,"IM2","","",""),
  ("DSQ-1",65,None,"IM3","","",""),
  ("DSQ-1",18,None,"EN4, IM3","trigger: mild activity","yes","Primary in Energy; 'sick' = flu-like malaise after exertion"),
  ("DSQ-1",64,None,"IM4","","","Self-reported; not necessarily measured"),
  ("DSQ-2",74,None,"IM5","type: viral; measure: frequency + recovery","","New in DSQ-2 (graded version of binary 128)"),
  ("DSQ-2",87,None,"IM5","type: sinus","","New in DSQ-2"),
  ("DSQ-1",98,None,"IM5","type: viral; measure: binary","","Case-definition item"),
  ("DSQ-2",109,None,"IM5","pole: fewer; measure: change since onset","","New in DSQ-2; reverse direction (stopped getting colds) – same axis, opposite pole"),
  ("RAND-36 v1",33,None,"IM5","measure: susceptibility vs others","","Also scored in RAND-36 General health → Global"),
  ("DSQ-1",66,None,"IM6","trigger: smells, foods, medication, chemicals","",""),
  ("DSQ-2",72,None,"IM6","trigger: mold","","New in DSQ-2"),
 ],
 boundary=[
  ("RAND-36 v1",34,None,"→ Global","'As healthy as anybody I know': global health, not immune"),
  ("DSQ-1",71,None,"excluded","Pre-onset checklist (sore throat, lymph nodes), not an outcome"),
  ("DSQ-1",59,None,"→ Temperature","Feeling like a high temperature = NE2 (sensation)"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Immune system: feeling ill, infections, sensitivities","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","Feeling ill (flu-like, throat, glands, fever)","N2",""),
  ("N1","N0",1,None,"How often I get infections","leaf","IM5"),
  ("N1","N0",1,None,"Reacting to smells, chemicals, foods or mold","leaf","IM6"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
  ("N2","N1",2,"Which one does '<score name>' measure?","Feeling flu-like","leaf","IM3"),
  ("N2","N1",2,None,"Sore throat","leaf","IM1"),
  ("N2","N1",2,None,"Swollen or tender glands","leaf","IM2"),
  ("N2","N1",2,None,"Fever","leaf","IM4"),
  ("N2","N1",2,None,"A mix of several of these","multi-select","composite"),
 ],
 findings=[
  "• Infection items share one axis (IM5) despite different wording: frequency, recovery, susceptibility, and DSQ2-109 'stopped getting colds' as opposite pole. Facets 'type', 'measure', 'pole' keep them apart; not asked.",
  "• IM6 grouped here as in the DSQ; mechanism unresolved. Sensory and Temperature trees redirect smells/chemicals and measured fever to this section.",
  "• DSQ-1 18 (drained or sick after mild activity) = EN4 + IM3 composite; primary in Energy.",
  "• Infection items are slow-changing (months); unsuitable for daily check-ins, better for periodic questionnaires.",
 ]))

# ------------------------------------------------------------------ MOOD
SECTIONS.append(dict(
 tab="Sec Mood", title="Section: Mood and emotions", prefix="MO",
 intro="Instruments: RAND-36 Emotional well-being (24, 25, 26, 28, 30; = MHI-5) and Role-emotional (17–19). DSQ, FUNCAP and Bell have no mood items. Positively worded items (calm, happy) are the opposite pole of the same granule, as in EN1.",
 granules=[
  ("MO1","Anxiety / tension","Feeling nervous, tense or worried; opposite pole: calm and peaceful.","How anxious or calm I feel"),
  ("MO2","Mood (low vs good)","Feeling down, low or blue; opposite pole: happy.","How good or low my mood is"),
  ("MO3","Emotional role limitation","How much emotional problems reduce work and daily activities.","How much my emotions limit my daily life"),
  ("MO4","Stress / feeling overwhelmed","Feeling under pressure or unable to cope with demands.","How stressed I feel"),
 ],
 items=[
  ("RAND-36 v1",24,None,"MO1","pole: anxious","",""),
  ("RAND-36 v1",26,None,"MO1","pole: calm","",""),
  ("RAND-36 v1",25,None,"MO2","pole: low; quality: nothing could cheer up","",""),
  ("RAND-36 v1",28,None,"MO2","pole: low","",""),
  ("RAND-36 v1",30,None,"MO2","pole: good","","Positive affect read as opposite pole of low mood (usability); psychometrically partly separate"),
  ("RAND-36 v1",17,None,"MO3","measure: time cut down","",""),
  ("RAND-36 v1",18,None,"MO3","measure: accomplished less","",""),
  ("RAND-36 v1",19,None,"MO3","measure: less carefully","","Excluded from Cognition as unspecific; fits here"),
 ],
 boundary=[
  ("DSQ-1",86,None,"excluded","Lifetime diagnoses (incl. psychiatric): exclusion criterion, not an outcome"),
  ("RAND-36 v1","20, 32",None,"→ Global","Social functioning (physical OR emotional cause)"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Mood and emotions","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How good or low my mood is","leaf","MO2"),
  ("N1","N0",1,None,"How anxious or calm I feel","leaf","MO1"),
  ("N1","N0",1,None,"How stressed I feel","leaf","MO4"),
  ("N1","N0",1,None,"How much my emotions limit my daily life","leaf","MO3"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
 ],
 findings=[
  "• Two-pole granules again: MO1 (anxious ↔ calm), MO2 (low ↔ happy). Direction rule handles it; RAND-36 scores EWB as one scale.",
  "• MO4 stress has no instrument item (granule without items, like CG9). Kept so a 'stress' score does not land in MO1 by default.",
  "• MO3 (role-emotional) mirrors PF4 (role-physical): participation, not the emotion itself.",
  "• Depth: category + 1 question.",
 ]))

# ---------------------------------------------------------------- GLOBAL
SECTIONS.append(dict(
 tab="Sec Global", title="Section: Global – overall health, illness level, change, social life", prefix="GL",
 intro="Instruments: RAND-36 General health (1, 33–36), Health change (2), Social functioning (20, 32); Bell CFIDS Disability Scale (one item, 11 levels); PGIC (own wording); DSQ-2 illness level (108). These items rate the whole condition, not one symptom.",
 granules=[
  ("GL1","Overall health","Rating of one's health as a whole.","How good my health is overall"),
  ("GL2","Overall illness level","How much the illness restricts life as a whole, from bedbound to normal.","How much the illness restricts me overall"),
  ("GL3","Global change","Better or worse than at a reference point (protocol start, a year ago).","How much better or worse I am than before"),
  ("GL4","Social limitation","How much health (physical or emotional) limits social activities.","How much my health limits my social life"),
 ],
 items=[
  ("RAND-36 v1",1,None,"GL1","","",""),
  ("RAND-36 v1",34,None,"GL1","measure: vs others","",""),
  ("RAND-36 v1",36,None,"GL1","","",""),
  ("RAND-36 v1",35,None,"GL1","measure: expectation (future)","","Prognosis, not current state; kept so the GH scale stays computable"),
  ("RAND-36 v1",33,None,"GL1, IM5","measure: susceptibility vs others","yes","Primary in Immune; listed for GH scale coverage"),
  ("Bell CFIDS Disability Scale","100–0",None,"GL2","measure: level 0–100, steps of 10","","Single item; each level = anchor text with function + symptoms"),
  ("DSQ-1",79,None,"GL2","measure: 7 levels, last 6 months","",""),
  ("PGIC (full 7-point, own wording)",1,None,"GL3","anchor: protocol start","","Own wording; stem decided 31 Oct 2026"),
  ("RAND-36 v1",2,None,"GL3","anchor: 1 year ago","","Not part of a RAND-36 scale"),
  ("RAND-36 v1",20,None,"GL4","measure: extent","",""),
  ("RAND-36 v1",32,None,"GL4","measure: time","",""),
 ],
 boundary=[
  ("DSQ-1",77,None,"excluded","Onset speed: history"),
  ("DSQ-1",78,None,"excluded","Course of illness: history, not a trackable level"),
 ],
 tree=[
  ("N0","—",0,"Which category fits '<score name>'?","Overall: how I am in general","N1",""),
  ("N1","N0",1,"When you give '<score name>' a high value, what are you rating?","How good my health is overall","leaf","GL1"),
  ("N1","N0",1,None,"How much the illness restricts me overall","leaf","GL2"),
  ("N1","N0",1,None,"How much better or worse I am than before","leaf","GL3"),
  ("N1","N0",1,None,"How much my health limits my social life","leaf","GL4"),
  ("N1","N0",1,None,"A mix of several of these","multi-select","composite"),
 ],
 findings=[
  "• The most common custom score ('how am I today overall') lands in GL1. Instrument items for GL1 are slow (RAND-36: 4 weeks / general) → compatible by concept, not by value.",
  "• Bell = one item with 11 anchor levels (steps of 10); too coarse for daily tracking, good for periodic snapshots.",
  "• GL3 change items need an anchor (facet 'anchor'): PGIC = protocol start, RAND-36 2 = one year ago. Change scores belong at block end, not into EMA.",
  "• RAND-36 General health is computable only with 1, 33, 34, 35, 36 all mapped → 33 listed as composite (primary IM5), 35 kept although it rates expectation.",
  "• GL4 (social) sits beside PF4 (role-physical) and MO3 (role-emotional): same participation level, different cause/domain.",
 ]))

# =====================================================================
def conv(ver, iid, alt):
    """DSQ-1 references are converted to DSQ-2 (primary); DSQ-1 id kept as 'other version'."""
    if ver == "DSQ-1":
        new = d1to2(iid); assert " " not in new, (iid, new)
        return "DSQ-2", new, f"DSQ-1: {iid}"
    if ver == "FUNCAP55":
        if not alt:  # auto: FUNCAP27 equivalent from 'Instrument items' notes
            r = ITEMS.get((ver, str(iid)))
            m_ = __import__("re").search(r"Same as FUNCAP27 item (\d+)", (r[11] or "") if r else "")
            alt = m_.group(1) if m_ else None
        return ver, iid, (f"F27: {alt}" if alt else None)
    return ver, iid, alt

def build(spec):
    for old in (spec["tab"], spec["tab"].replace("Sec ", "Pilot ")):
        if old in wb.sheetnames and old != "Pilot Sleep": del wb[old]
    anchor = [n for n in wb.sheetnames if n.startswith("Sec ")]
    idx = (wb.sheetnames.index(anchor[-1]) + 1) if anchor else wb.sheetnames.index("Method") + 1
    ws = wb.create_sheet(spec["tab"], index=idx)
    def put(row, vals, kind="body"):
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row, j, v); c.font, c.fill = copy.copy(ST[kind][0]), copy.copy(ST[kind][1])
            c.alignment = Alignment(vertical="top", wrap_text=True)
    p = spec["prefix"]; r = 1
    put(r, [spec["title"]], "title"); r += 1
    put(r, [spec["intro"] + " Items quoted verbatim from tab 'Instrument items'."], "note"); r += 2
    put(r, ["1. Granules"], "sec"); r += 1
    put(r, ["Granule ID","Granule","Plain-language definition","User-facing wording","Items mapped","DSQ","FUNCAP","RAND-36","Bell","PGIC","Instruments covering"], "hdr"); r += 1
    grows = []
    for g in spec["granules"]: grows.append(r); put(r, list(g)); r += 1
    r += 1
    put(r, ["2. Instrument items"], "sec"); r += 1
    put(r, ["Item ID","Instrument","Version","Other version","Item (verbatim)","Timeframe","Response format","Granule(s)","Facets","Composite?","Note"], "hdr"); r += 1
    i0 = r
    for ver, iid, f27, gr, fac, comp, note in spec["items"]:
        ver, iid, f27 = conv(ver, iid, f27)
        inst, pre = INST[ver]
        try: t, tf, rf = item_row(ver, iid)
        except KeyError:  # range of response levels of one single item (Bell)
            lv = __import__("re").findall(r"\d+", str(iid))
            _, tf, rf = item_row(ver, lv[0]); t = f"Single item, levels {iid} (see 'Instrument items')"
        put(r, [f"{pre}-{iid}", inst, ver, f27, t, tf, short_rf(rf), gr, fac, comp, note])
        if comp == "yes": ws.cell(r, 10).fill = PatternFill("solid", fgColor="FFFCE8B2")
        r += 1
    i1 = r - 1; r += 1
    if spec["boundary"]:
        put(r, ["3. Boundary and excluded items"], "sec"); r += 1
        put(r, ["Item ID","Instrument","Version","Other version","Item (verbatim)","Goes to","Reason"], "hdr"); r += 1
        for ver, iid, f27, goes, why in spec["boundary"]:
            try: ver, iid, f27 = conv(ver, iid, f27)
            except (KeyError, ValueError, AssertionError): pass
            inst, pre = INST[ver]
            try: t = item_row(ver, iid)[0]
            except KeyError: t = f"Items/levels {iid} (see 'Instrument items')"
            put(r, [f"{pre}-{iid}", inst, ver, f27, t, goes, why]); r += 1
        r += 1
    put(r, ["4. Decision tree"], "sec"); r += 1
    put(r, ["Node ID","Parent","Level","Question shown to the user","Answer option","Leads to","Granule"], "hdr"); r += 1
    def pid(x): return f"{p}-{x}" if x and x[0] == "N" and x != "N0" else x
    for nid, par, lvl, q, a, to, g in spec["tree"]:
        put(r, [pid(nid) if nid != "N0" else "N0", pid(par), lvl, q, a, pid(to), g]); r += 1
    put(r, ["After any leaf: the app asks once 'Is a high value good or bad for you?' (direction rule, Method tab). Facets are never asked; set only if the score name specifies them."], "note"); r += 2
    put(r, ["5. Findings"], "sec"); r += 1
    for f in spec["findings"]: put(r, [f], "note"); r += 1
    G, I = f"$H${i0}:$H${i1}", f"$B${i0}:$B${i1}"
    for gr in grows:
        ws.cell(gr, 5, f'=COUNTIF({G},"*"&A{gr}&"*")')
        for col, name in ((6, "DSQ"), (7, "FUNCAP"), (8, "RAND-36"), (9, "Bell"), (10, "PGIC")):
            ws.cell(gr, col, f'=COUNTIFS({I},"{name}",{G},"*"&A{gr}&"*")')
        ws.cell(gr, 11, f"=(F{gr}>0)+(G{gr}>0)+(H{gr}>0)+(I{gr}>0)+(J{gr}>0)")
    for col, w in zip("ABCDEFGHIJK", [13, 26, 34, 32, 60, 18, 26, 16, 30, 11, 40]):
        ws.column_dimensions[col].width = w

for s in SECTIONS: build(s)
if "Pilot Sleep" in wb.sheetnames: del wb["Pilot Sleep"]

# ---------------- Method tab: rules added after the pilots ----------------
m = wb["Method"]
if not any(c.value == "Rules added after pilots" for c in m["A"]):
    hdr_font, hdr_fill = copy.copy(m["A15"].font), copy.copy(m["A15"].fill)
    rr = m.max_row + 2
    m.cell(rr, 1, "Rules added after pilots").font = copy.copy(m["A1"].font); rr += 1
    for k, v in [
     ("Scale", "Users may choose any scale for a custom score. It is poolable if it is ordinal (more = more) and its direction is known. Nominal scales stay personal (flag 'not pooled')."),
     ("Direction", "After a leaf is reached the app asks once: 'Is a high value good or bad for you?'. Stored per score; needed e.g. for EN1 (fatigue vs. energy pole)."),
     ("Measure type", "Recorded per item: symptom (frequency/severity, DSQ), capacity/cost (FUNCAP), level (1–100 energy, RAND). Same granule, values not comparable."),
     ("Cross-user analysis", "Primary: within-person standardized effects (e.g. protocol on vs. off), pooled across users. Absolute levels between users only via periodic official questionnaires."),
     ("Facets (extended)", "Added 'load' (duration/complexity) and 'modality' (reading, conversation, writing, screen) after cognition; 'pole' and 'measure' after energy. All optional, never a mismatch."),
     ("Granules without items", "Allowed (e.g. CG9 confusion): reachable in the tree, linked to case definitions only, no instrument leaf."),
     ("Asked facets", "A facet is asked in the tree only when the section's items differ by nothing but that facet (Pain: region). Elsewhere facets are not asked."),
     ("Mapping by mechanism", "Items are assigned by what they measure, not by the instrument's own heading (e.g. DSQ 14 sits in the DSQ 'PEM' block but measures fatigability)."),
    ]:
        m.cell(rr, 1, k).font = copy.copy(m["A4"].font); m.cell(rr, 2, v)
        m.cell(rr, 2).alignment = Alignment(wrap_text=True, vertical="top"); rr += 1

if not any(c.value == "Facet 'activity'" for c in m["A"]):
    rr = m.max_row + 1
    m.cell(rr, 1, "Facet 'activity'").font = copy.copy(m["A4"].font)
    m.cell(rr, 2, "Added after Function: concrete everyday activity (self-care, housework, outing, exercise). Activities are not granules; they bundle load types (PF1–3). Asked in the Function tree (N3).")
    m.cell(rr, 2).alignment = Alignment(wrap_text=True, vertical="top")

wb.save(WB)
print(wb.sheetnames)

# ---------------- legacy tabs (kept, marked; not renamed → cross-tab formulas stay intact) ----------------
wb = openpyxl.load_workbook(WB)
for name in ("Groups", "Grouped rows", "Criteria", "DSQ outcome items"):
    ws = wb[name]
    ws.sheet_properties.tabColor = "FF9E9E9E"
    col = ws.max_column + 2
    if not any(str(c.value).startswith("LEGACY") for c in ws[1] if c.value):
        c = ws.cell(1, col, "LEGACY – paraphrased, predates the granule method (Sec tabs + 'Instrument items'). Kept as bridge to case definitions; may be deleted.")
        c.font = copy.copy(ST["note"][0]); c.fill = PatternFill("solid", fgColor="FFFCE8B2")
        c.alignment = Alignment(wrap_text=True, vertical="top"); ws.column_dimensions[c.column_letter].width = 50
ov = wb["Overview"]
if not any(str(c.value or "").startswith("Legacy tabs") for c in ov["A"]):
    ov.cell(ov.max_row + 2, 1, "Legacy tabs (grey): Groups, Grouped rows, Criteria, DSQ outcome items – paraphrased, predate the granule method. Current work: Method, Sec * tabs, Instrument items.")
wb.save(WB)
