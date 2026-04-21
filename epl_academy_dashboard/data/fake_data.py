"""
EPL Academy Dashboard - Fake Data Generator
5 academy players with full realistic data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

PLAYERS = [
    {"id":"P001","name":"Mason Whitfield","dob":"2007-03-14","age":17,"age_group":"U18",
     "position":"CAM","position_secondary":"LW","foot":"Right","nationality":"English",
     "height_cm":176,"weight_kg":68,"contract_status":"Scholarship","contract_expiry":"2026-06-30",
     "graduation_eta":"2026","first_team_apps":0,"overall_score":84,"health_status":"Fit","photo":"MW"},
    {"id":"P002","name":"Kai Oduya","dob":"2006-08-22","age":18,"age_group":"U18",
     "position":"CM","position_secondary":"CDM","foot":"Both","nationality":"Nigerian-British",
     "height_cm":182,"weight_kg":75,"contract_status":"Professional","contract_expiry":"2027-06-30",
     "graduation_eta":"2025","first_team_apps":3,"overall_score":88,"health_status":"Fit","photo":"KO"},
    {"id":"P003","name":"Luca Hernandez","dob":"2008-01-05","age":16,"age_group":"U16",
     "position":"ST","position_secondary":"CF","foot":"Left","nationality":"Spanish",
     "height_cm":171,"weight_kg":63,"contract_status":"Scholarship","contract_expiry":"2026-06-30",
     "graduation_eta":"2027","first_team_apps":0,"overall_score":79,"health_status":"Injured","photo":"LH"},
    {"id":"P004","name":"Ethan Kowalski","dob":"2005-11-30","age":19,"age_group":"U21",
     "position":"CB","position_secondary":"RB","foot":"Right","nationality":"Polish-British",
     "height_cm":188,"weight_kg":82,"contract_status":"Professional","contract_expiry":"2025-06-30",
     "graduation_eta":"2025","first_team_apps":8,"overall_score":82,"health_status":"Precaution","photo":"EK"},
    {"id":"P005","name":"Jaylen Brooks","dob":"2007-06-18","age":17,"age_group":"U18",
     "position":"RB","position_secondary":"RM","foot":"Right","nationality":"English",
     "height_cm":178,"weight_kg":71,"contract_status":"Scholarship","contract_expiry":"2026-06-30",
     "graduation_eta":"2026","first_team_apps":1,"overall_score":81,"health_status":"Fit","photo":"JB"},
]
PLAYER_IDS = [p["id"] for p in PLAYERS]

BODY_PARTS = {
    "head":"Head","neck":"Neck / Cervical Region",
    "left_shoulder":"Left Shoulder","right_shoulder":"Right Shoulder",
    "left_upper_arm":"Left Upper Arm","right_upper_arm":"Right Upper Arm",
    "left_elbow":"Left Elbow","right_elbow":"Right Elbow",
    "left_forearm":"Left Forearm","right_forearm":"Right Forearm",
    "left_wrist":"Left Wrist/Hand","right_wrist":"Right Wrist/Hand",
    "chest":"Chest","abdomen":"Abdomen",
    "left_groin":"Left Groin / Adductors","right_groin":"Right Groin / Adductors",
    "left_quad":"Left Anterior Thigh","right_quad":"Right Anterior Thigh",
    "left_knee_front":"Left Knee (Patella)","right_knee_front":"Right Knee (Patella)",
    "left_shin":"Left Shin / Tibia","right_shin":"Right Shin / Tibia",
    "left_ankle_front":"Left Ankle","right_ankle_front":"Right Ankle",
    "upper_back":"Upper Back / Trapezius","lower_back":"Lumbar Region",
    "left_glute":"Left Gluteal","right_glute":"Right Gluteal",
    "left_hamstring":"Left Hamstring","right_hamstring":"Right Hamstring",
    "left_calf":"Left Calf","right_calf":"Right Calf",
    "left_achilles":"Left Achilles Tendon","right_achilles":"Right Achilles Tendon",
}

INJURY_PRONE = {
    "P001":["right_quad","left_ankle_front","right_groin"],
    "P002":["right_hamstring","lower_back","left_knee_front"],
    "P003":["left_hamstring","right_ankle_front","left_quad"],
    "P004":["right_knee_front","lower_back","left_hamstring"],
    "P005":["right_achilles","right_hamstring","left_groin"],
}
INJURY_TYPES=["Muscle Strain","Ligament Sprain","Tendinopathy","Contusion",
              "Stress Fracture","Muscle Fatigue","Ligament Tear","Bone Bruise"]
SEVERITY=["Minor","Grade I","Grade II","Grade III"]
SEVERITY_DAYS={"Minor":(3,10),"Grade I":(7,21),"Grade II":(14,45),"Grade III":(30,90)}


def generate_physical_data():
    records=[]
    bh={"P001":168,"P002":175,"P003":163,"P004":181,"P005":170}
    bw={"P001":60,"P002":67,"P003":56,"P004":74,"P005":63}
    for pid in PLAYER_IDS:
        h,w=bh[pid],bw[pid]
        for i,q in enumerate(pd.date_range("2022-09-01","2025-03-01",freq="QS")):
            h+=random.uniform(0.5,2.0) if i<6 else random.uniform(0,0.3)
            w+=random.uniform(0.3,1.5)
            records.append({"player_id":pid,"date":q,"height_cm":round(h,1),"weight_kg":round(w,1),
                "bmi":round(w/((h/100)**2),1),"body_fat_pct":round(random.uniform(9,14),1),
                "lean_mass_kg":round(w*random.uniform(0.86,0.91),1),
                "sprint_10m":round(random.uniform(1.65,1.85)-i*0.003,2),
                "sprint_30m":round(random.uniform(4.05,4.35)-i*0.005,2),
                "illinois_agility":round(random.uniform(15.2,16.8)-i*0.04,2),
                "vertical_jump_cm":round(random.uniform(45,65)+i*0.3,1),
                "standing_long_jump_cm":round(random.uniform(210,255)+i*0.5,1),
                "yoyo_ir2_level":round(random.uniform(16,21)+i*0.1,1),
                "vo2max":round(random.uniform(52,62)+i*0.2,1)})
    return pd.DataFrame(records)


def generate_performance_data():
    records=[]
    bs={"P001":{"g":8,"a":10,"min":1400,"kp":38,"dr":42},
        "P002":{"g":4,"a":8,"min":1650,"kp":45,"dr":28},
        "P003":{"g":12,"a":5,"min":1100,"kp":22,"dr":35},
        "P004":{"g":2,"a":3,"min":1750,"kp":12,"dr":8},
        "P005":{"g":3,"a":9,"min":1500,"kp":32,"dr":48}}
    for pid in PLAYER_IDS:
        b=bs[pid]
        for i,season in enumerate(["2022/23","2023/24","2024/25"]):
            m=1+i*0.12; apps=random.randint(18,28)
            records.append({"player_id":pid,"season":season,"appearances":apps,
                "starts":apps-random.randint(2,6),
                "minutes":int(b["min"]*m+random.randint(-100,100)),
                "goals":int(b["g"]*m+random.randint(-1,2)),
                "assists":int(b["a"]*m+random.randint(-1,2)),
                "key_passes":int(b["kp"]*m),"dribbles_completed":int(b["dr"]*m),
                "pass_accuracy_pct":round(random.uniform(72,88),1),
                "duels_won_pct":round(random.uniform(48,62),1),
                "xg":round(random.uniform(3,14),2),"xa":round(random.uniform(2,10),2),
                "tackles":random.randint(20,80),"interceptions":random.randint(10,50),
                "yellow_cards":random.randint(1,5),"red_cards":random.randint(0,1)})
    return pd.DataFrame(records)


def generate_technical_ratings():
    records=[]
    br={"P001":{"pa":78,"dr":85,"sh":72,"hd":55,"df":50,"sp":68,"ta":76,"po":80,"de":74,"aw":82},
        "P002":{"pa":85,"dr":72,"sh":65,"hd":70,"df":78,"sp":62,"ta":84,"po":83,"de":80,"aw":79},
        "P003":{"pa":68,"dr":80,"sh":86,"hd":72,"df":45,"sp":70,"ta":65,"po":78,"de":68,"aw":72},
        "P004":{"pa":72,"dr":55,"sh":40,"hd":85,"df":88,"sp":60,"ta":80,"po":86,"de":82,"aw":84},
        "P005":{"pa":76,"dr":82,"sh":68,"hd":60,"df":72,"sp":65,"ta":70,"po":75,"de":72,"aw":74}}
    for pid in PLAYER_IDS:
        b=br[pid]
        for period in pd.date_range("2022-09-01","2025-03-01",freq="3MS"):
            n=lambda x:min(99,max(30,x+random.randint(-3,5)))
            records.append({"player_id":pid,"date":period,
                "passing":n(b["pa"]),"dribbling":n(b["dr"]),"shooting":n(b["sh"]),
                "heading":n(b["hd"]),"defending":n(b["df"]),"set_pieces":n(b["sp"]),
                "tactical_understanding":n(b["ta"]),"positioning":n(b["po"]),
                "decision_making":n(b["de"]),"spatial_awareness":n(b["aw"])})
    return pd.DataFrame(records)


def generate_injury_data():
    records=[]
    start=datetime(2022,8,1); end=datetime(2025,4,1)
    for pid in PLAYER_IDS:
        prone=list(INJURY_PRONE[pid])
        for _ in range(random.randint(5,9)):
            part_key=random.choice(prone) if random.random()<0.7 else random.choice(list(BODY_PARTS.keys()))
            inj_date=start+timedelta(days=random.randint(0,(end-start).days))
            sev=random.choices(SEVERITY,weights=[30,35,25,10])[0]
            days=random.randint(*SEVERITY_DAYS[sev])
            records.append({"player_id":pid,"body_part_key":part_key,
                "body_part_name":BODY_PARTS[part_key],
                "injury_date":inj_date.strftime("%Y-%m-%d"),
                "return_date":(inj_date+timedelta(days=days)).strftime("%Y-%m-%d"),
                "season":f"{inj_date.year}/{str(inj_date.year+1)[-2:]}",
                "injury_type":random.choice(INJURY_TYPES),"severity":sev,"days_out":days,
                "injury_burden_months":round(days/30,1),"is_active":False,
                "notes":random.choice(["Contact injury during training","Non-contact - sudden onset",
                    "Gradual overuse","Match incident","Pre-season overload"])})
    records.append({"player_id":"P003","body_part_key":"left_hamstring",
        "body_part_name":"Left Hamstring","injury_date":"2025-03-10",
        "return_date":"2025-04-20","season":"2024/25","injury_type":"Muscle Strain",
        "severity":"Grade II","days_out":41,"injury_burden_months":1.4,"is_active":True,
        "notes":"Non-contact hamstring strain during sprint training"})
    return pd.DataFrame(records)


def generate_load_data():
    records=[]
    for pid in PLAYER_IDS:
        chronic=random.uniform(350,450)
        for date in pd.date_range("2024-09-01","2025-04-10",freq="D"):
            if date.dayofweek==6: daily=random.uniform(0,80)
            elif date.dayofweek in [2,5]: daily=random.uniform(400,600)
            else: daily=random.uniform(250,420)
            chronic=chronic*0.9+daily*0.1
            acute=daily*random.uniform(0.8,1.2)
            acwr=round(acute/chronic if chronic>0 else 1.0,2)
            records.append({"player_id":pid,"date":date,"daily_load":round(daily,1),
                "acute_load":round(acute,1),"chronic_load":round(chronic,1),"acwr":acwr,
                "total_distance_km":round(daily/60,2),
                "hsr_distance_m":round(daily*random.uniform(0.08,0.18),0),
                "sprint_count":random.randint(0,25),"max_speed_kmh":round(random.uniform(26,32),1),
                "risk_level":"High" if acwr>1.5 else ("Optimal" if acwr>=0.8 else "Low")})
    return pd.DataFrame(records)


def generate_wellness_data():
    records=[]
    for pid in PLAYER_IDS:
        for date in pd.date_range("2025-01-01","2025-04-10",freq="D"):
            if date.dayofweek==6: continue
            records.append({"player_id":pid,"date":date,
                "sleep_quality":random.randint(5,10),"fatigue":random.randint(1,8),
                "muscle_soreness":random.randint(1,8),"mood":random.randint(5,10),
                "stress":random.randint(1,7)})
    return pd.DataFrame(records)


def generate_psych_data():
    base={"P001":{"re":82,"le":70,"tw":85,"la":88,"co":78,"fo":80},
          "P002":{"re":88,"le":85,"tw":82,"la":86,"co":84,"fo":87},
          "P003":{"re":72,"le":65,"tw":78,"la":80,"co":75,"fo":70},
          "P004":{"re":84,"le":80,"tw":88,"la":76,"co":80,"fo":82},
          "P005":{"re":78,"le":72,"tw":84,"la":82,"co":76,"fo":79}}
    notes=["Excellent attitude in training, shows great maturity for his age.",
           "Natural leader on and off the pitch. First team knocking.",
           "Technically gifted but needs to build mental resilience post-injury.",
           "Commanding presence. Reading of the game is exceptional.",
           "Tireless work rate. Needs to improve decisions in the final third."]
    records=[]
    for i,pid in enumerate(PLAYER_IDS):
        b=base[pid]
        records.append({"player_id":pid,"assessment_date":"2025-03-01",
            "resilience_self":b["re"]+random.randint(-5,5),"resilience_coach":b["re"],
            "leadership_self":b["le"]+random.randint(-5,5),"leadership_coach":b["le"],
            "teamwork_self":b["tw"]+random.randint(-3,3),"teamwork_coach":b["tw"],
            "learning_attitude_self":b["la"]+random.randint(-4,4),"learning_attitude_coach":b["la"],
            "confidence_self":b["co"]+random.randint(-6,6),"confidence_coach":b["co"],
            "focus_self":b["fo"]+random.randint(-5,5),"focus_coach":b["fo"],
            "coach_notes":notes[i]})
    return pd.DataFrame(records)


def generate_milestones():
    data=[
        {"player_id":"P001","date":"2022-09-05","event":"Joined U16 Academy","icon":"🏫"},
        {"player_id":"P001","date":"2023-11-12","event":"First U18 Appearance","icon":"⚽"},
        {"player_id":"P001","date":"2024-03-20","event":"Signed Scholarship Contract","icon":"📝"},
        {"player_id":"P001","date":"2024-08-15","event":"First Team Training Session","icon":"🌟"},
        {"player_id":"P002","date":"2021-07-01","event":"Joined U16 Academy","icon":"🏫"},
        {"player_id":"P002","date":"2023-01-18","event":"Signed Professional Contract","icon":"📝"},
        {"player_id":"P002","date":"2023-09-26","event":"First Team Debut (EFL Trophy)","icon":"🌟"},
        {"player_id":"P002","date":"2024-02-10","event":"First Premier League Bench","icon":"🏆"},
        {"player_id":"P002","date":"2024-12-03","event":"England U20 Call-Up","icon":"🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
        {"player_id":"P003","date":"2022-08-20","event":"Joined U15 Academy","icon":"🏫"},
        {"player_id":"P003","date":"2023-04-05","event":"U16 Top Scorer Award","icon":"🥇"},
        {"player_id":"P003","date":"2024-01-15","event":"First U18 Appearance","icon":"⚽"},
        {"player_id":"P003","date":"2025-03-10","event":"Hamstring Injury (Current)","icon":"🏥"},
        {"player_id":"P004","date":"2020-09-01","event":"Joined U16 Academy","icon":"🏫"},
        {"player_id":"P004","date":"2022-06-10","event":"Signed Professional Contract","icon":"📝"},
        {"player_id":"P004","date":"2023-08-22","event":"First Team Pre-Season","icon":"⚽"},
        {"player_id":"P004","date":"2024-01-09","event":"FA Youth Cup Final Appearance","icon":"🏆"},
        {"player_id":"P004","date":"2024-10-15","event":"Poland U21 International","icon":"🇵🇱"},
        {"player_id":"P005","date":"2022-07-15","event":"Joined U16 Academy","icon":"🏫"},
        {"player_id":"P005","date":"2023-10-08","event":"First U18 Appearance","icon":"⚽"},
        {"player_id":"P005","date":"2024-04-01","event":"Signed Scholarship Contract","icon":"📝"},
        {"player_id":"P005","date":"2024-11-20","event":"First Team Training Invitation","icon":"🌟"},
    ]
    return pd.DataFrame(data)


def load_all_data():
    return {
        "players": pd.DataFrame(PLAYERS),
        "physical": generate_physical_data(),
        "performance": generate_performance_data(),
        "technical": generate_technical_ratings(),
        "injuries": generate_injury_data(),
        "load": generate_load_data(),
        "wellness": generate_wellness_data(),
        "psych": generate_psych_data(),
        "milestones": generate_milestones(),
    }
