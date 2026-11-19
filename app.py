import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import requests

st.set_page_config(
    page_title="RASD — منظومة التنبؤ والإنذار المبكر",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background-color: #06101e;
        color: #e6eef8;
    }
    .block-container {
        padding-top: 0.45rem !important;
        padding-bottom: 0.45rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    section[data-testid="stSidebar"], button[kind="header"] {
        display: none;
    }
    .stButton > button, .stButton > button * {
        background-color: #0d2240 !important;
        color: #e2e8f0 !important;
        border: 1px solid #234675 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        padding: 0.2rem 0.4rem !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover, .stButton > button:hover * {
        background-color: #163b6d !important;
        color: #7dd3fc !important;
        border-color: #38bdf8 !important;
    }
    .bar-box {
        background: #091930;
        border: 1px solid #1e3a60;
        border-radius: 8px;
        padding: 6px 10px;
        margin-bottom: 6px;
    }
    .mini-lbl {
        font-size: 10px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 2px;
    }
    .kpi-card {
        background: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 8px;
        padding: 6px 10px;
    }
    .kpi-title {
        font-size: 10px;
        color: #94b2d6;
    }
    .kpi-val {
        font-size: 17px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 10px;
        color: #7dd3fc;
    }
    .side-box {
        background: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 8px;
        padding: 8px 10px;
        margin-bottom: 6px;
        font-size: 11px;
    }
    </style>
""", unsafe_allow_html=True)

makkah_boundary_coords = [
    [38.88, 22.92], [39.32, 23.12], [39.85, 22.85], [40.45, 22.78],
    [41.15, 22.65], [41.85, 22.55], [42.55, 22.35], [42.95, 21.85],
    [42.80, 21.20], [42.20, 20.65], [41.65, 20.15], [41.45, 19.55],
    [41.20, 19.05], [40.82, 19.35], [40.68, 19.95], [40.25, 20.15],
    [39.82, 20.75], [39.38, 21.35], [39.05, 21.95], [38.88, 22.92]
]

stations_data = [
    ("J112", "جدة", "أودية شمال جدة", "مجرى وادي شمال جدة الساحلي", 39.42, 23.28, 42.0, 25.0, 32.0, 0.35, 31.0, 68.0, 1011.0, 24.0, 95.0, 68, 7, 56.0),
    ("J140", "جدة", "أودية خليص وثول", "تقاطع وادي خليص مع الطريق الساحلي", 39.28, 22.68, 48.0, 35.0, 38.0, 0.35, 31.5, 70.0, 1010.5, 26.0, 105.0, 72, 8, 42.0),
    ("J116", "جدة", "وادي غران / شمال جدة", "مصب الوادي شرق الطريق السريع", 39.55, 22.42, 54.0, 85.0, 42.0, 0.40, 32.0, 65.0, 1011.0, 22.0, 88.0, 64, 8, 38.0),
    ("J220", "جدة", "وادي قديد / شمال جدة", "نقطة تجمع السيول شرق المحافظة", 39.72, 22.15, 62.0, 140.0, 46.0, 0.45, 32.5, 62.0, 1011.5, 25.0, 92.0, 66, 8, 34.0),
    ("J239", "جدة", "حوض جدة الشمالي", "تقاطع أودية ذهبان وعسفان", 39.58, 21.88, 58.0, 65.0, 44.0, 0.40, 33.0, 67.0, 1010.8, 28.0, 110.0, 76, 9, 28.0),
    ("J214", "جدة", "وادي عسفان / جدة", "مجرى وادي عسفان ومخرج المياه", 39.88, 21.89, 76.0, 185.0, 52.0, 0.50, 33.5, 58.0, 1011.2, 27.0, 100.0, 71, 9, 26.0),
    ("J134", "جدة", "حوض جدة الأوسط", "مجرى وادي مريخ وتصريف شرق جدة", 39.18, 21.54, 52.0, 18.0, 40.0, 0.35, 32.8, 72.0, 1010.2, 29.0, 115.0, 80, 9, 24.0),
    ("J102", "مكة المكرمة", "وادي فاطمة / مكة", "تقاطع وادي فاطمة مع طريق الحرمين", 39.68, 21.46, 88.0, 240.0, 58.0, 0.55, 35.0, 52.0, 1010.6, 23.0, 120.0, 84, 9, 22.0),
    ("J114", "مكة المكرمة", "وادي نعمان / مكة", "مجرى وادي نعمان ومناطق التجمع", 39.96, 21.42, 104.0, 390.0, 64.0, 0.60, 34.0, 50.0, 1011.4, 21.0, 95.0, 70, 9, 18.0),
    ("J113", "مكة المكرمة", "أودية الكر / مكة - الطائف", "منحدرات الكر وطريق الهدا", 40.12, 21.62, 138.0, 780.0, 72.0, 0.65, 28.5, 64.0, 1013.0, 26.0, 65.0, 52, 8, 19.0),
    ("J204", "مكة المكرمة", "وادي الكر السفلي", "نقطة التقاء الشعاب أسفل الكر", 40.05, 21.52, 124.0, 560.0, 68.0, 0.60, 30.0, 58.0, 1012.5, 24.0, 75.0, 58, 8, 17.0),
    ("J205", "مكة المكرمة", "وادي الكر العلوي", "مناطق التجمع الجبلية بأعالي الكر", 40.22, 21.55, 165.0, 1320.0, 78.0, 0.70, 24.0, 70.0, 1014.5, 28.0, 50.0, 42, 7, 16.0),
    ("TA206", "الطائف", "حوض الطائف / وادي وج", "مجرى وادي وج ومخرج الطائف", 40.41, 21.27, 192.0, 1480.0, 82.0, 0.72, 22.5, 68.0, 1015.2, 25.0, 48.0, 40, 7, 14.0),
    ("TA004", "الطائف", "أودية السيل / الطائف", "مجرى السيل الكبير ومخرج الطائف", 40.58, 21.48, 154.0, 1290.0, 74.0, 0.65, 25.0, 56.0, 1014.0, 27.0, 62.0, 49, 8, 21.0),
    ("TA106", "الطائف", "وادي محرم / الطائف", "تجمع السيول شرق الطائف", 40.52, 21.35, 178.0, 1540.0, 79.0, 0.70, 23.0, 62.0, 1014.8, 24.0, 52.0, 43, 7, 15.0),
    ("TA002", "الطائف", "حوض سيسد / الطائف", "حوض وادي سيسد ومناطق التجمع", 40.64, 21.22, 186.0, 1620.0, 80.0, 0.70, 22.0, 65.0, 1015.0, 22.0, 46.0, 39, 7, 18.0),
    ("TA104", "الطائف", "أودية كلاخ / الطائف", "مجرى الأودية الشرقية بالطائف", 40.76, 21.26, 145.0, 1410.0, 70.0, 0.65, 24.5, 50.0, 1014.2, 26.0, 58.0, 47, 8, 27.0),
    ("TA233", "الطائف", "أودية بقران / الطائف", "مجرى بقران جنوب شرق الطائف", 40.72, 20.98, 172.0, 1710.0, 76.0, 0.68, 21.5, 60.0, 1015.5, 25.0, 45.0, 38, 7, 29.0),
    ("TA109", "الطائف", "مرتفعات الشفا / الطائف", "منحدرات الشفا والأودية الغربية", 40.32, 21.08, 238.0, 1980.0, 88.0, 0.75, 19.5, 76.0, 1016.0, 28.0, 35.0, 33, 6, 15.0),
    ("TA005", "الطائف", "أودية شرق مكة - الطائف", "نطاق الرصد الشرقي المفتوح", 41.48, 21.18, 96.0, 1120.0, 55.0, 0.55, 27.0, 44.0, 1013.5, 31.0, 130.0, 88, 9, 74.0),
    ("J107", "الليث", "وادي الليث العلوي", "نقطة اختناق وادي الليث", 40.27, 20.15, 148.0, 620.0, 74.0, 0.65, 31.0, 66.0, 1011.8, 22.0, 78.0, 60, 8, 33.0),
    ("J108", "الليث", "مصب وادي الليث", "مجرى الوادي قرب الساحل بالليث", 40.18, 20.05, 84.0, 85.0, 56.0, 0.50, 33.5, 72.0, 1010.4, 24.0, 96.0, 70, 9, 25.0),
    ("J221", "الليث", "أودية جنوب الليث", "تقاطع الشعاب جنوب المحافظة", 40.68, 20.12, 132.0, 940.0, 68.0, 0.62, 27.5, 61.0, 1012.6, 23.0, 70.0, 55, 8, 39.0),
    ("J137", "القنفذة", "وادي قنونا الأوسط", "معبر وادي قنونا ومناطق الجريان", 41.08, 19.82, 118.0, 410.0, 65.0, 0.58, 32.0, 69.0, 1011.2, 21.0, 85.0, 64, 9, 36.0),
    ("J139", "القنفذة", "أودية غرب القنفذة", "مجرى الأودية باتجاه الساحل", 40.86, 19.62, 74.0, 65.0, 52.0, 0.45, 34.0, 74.0, 1010.0, 23.0, 98.0, 71, 9, 31.0),
    ("J131", "القنفذة", "أودية جنوب شرق القنفذة", "مرتفعات جنوب منطقة الدراسة", 41.52, 19.42, 156.0, 1240.0, 75.0, 0.68, 25.5, 71.0, 1013.8, 24.0, 62.0, 49, 8, 54.0),
]

CITIES = [
    {"ar": "جدة", "lat": 21.54, "lon": 39.17},
    {"ar": "مكة المكرمة", "lat": 21.42, "lon": 39.83},
    {"ar": "الطائف", "lat": 21.27, "lon": 40.42},
    {"ar": "رابغ", "lat": 22.80, "lon": 39.03},
    {"ar": "الليث", "lat": 20.15, "lon": 40.27},
    {"ar": "القنفذة", "lat": 19.13, "lon": 41.08},
    {"ar": "تربة", "lat": 21.21, "lon": 41.63},
]
ALERT_MM = 20.0

@st.cache_data(ttl=900, show_spinner=False)
def fetch_open_meteo_7d():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=" + ",".join(str(c["lat"]) for c in CITIES)
        + "&longitude=" + ",".join(str(c["lon"]) for c in CITIES)
        + "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m"
        + "&daily=precipitation_sum,precipitation_probability_max"
        + "&forecast_days=7&timezone=Asia%2FRiyadh"
    )
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    payload = resp.json()
    items = payload if isinstance(payload, list) else [payload]
    rows = []
    for idx, city in enumerate(CITIES):
        if idx >= len(items):
            break
        w = items[idx]
        cur = w.get("current", {})
        daily = w.get("daily", {})
        p_sums = daily.get("precipitation_sum") or [0.0]
        p_probs = daily.get("precipitation_probability_max") or [0]
        max_rain_7d = float(np.max([x if x is not None else 0.0 for x in p_sums]))
        max_prob_7d = int(np.max([x if x is not None else 0 for x in p_probs]))
        rows.append({
            "city": city["ar"],
            "temp_c": cur.get("temperature_2m"),
            "humidity": cur.get("relative_humidity_2m"),
            "rain_now": cur.get("precipitation", 0.0),
            "wind_kmh": cur.get("wind_speed_10m"),
            "max_rain_7d": round(max_rain_7d, 1),
            "max_prob_7d": max_prob_7d,
            "alert_7d": max_rain_7d >= ALERT_MM,
            "daily_rain": [round(float(x if x is not None else 0.0), 1) for x in p_sums[:7]],
            "daily_dates": daily.get("time", [])[:7],
        })
    return pd.DataFrame(rows)

df = pd.DataFrame(stations_data, columns=[
    "Station", "Governorate", "Basin", "Hotspot", "lon", "lat",
    "Hist_Mean_Rain", "Elevation_m", "Soil_Saturation_Pct", "Low_Perm_Factor",
    "Temp_C", "Humidity_Pct", "Pressure_hPa", "Wind_kmh", "Dust_ugm3",
    "AQI", "UV_Index", "Dist_Nearest_km"
])
df["Extrapolated_Low_Conf"] = df["Dist_Nearest_km"] > 50.0

defaults = {
    "selected_gov": "الكل",
    "model_mode": "Random Forest",
    "horizon_mode": "Nowcasting",
    "hazard_type": "rain",
    "map_layer": "rain",
    "rain_sim_val": 0,
    "pct_boost": 0,
    "storm_hours": 6,
    "picked_station": "TA109",
    "use_live_meteo": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def set_scenario(r_val, p_val, h_val):
    st.session_state.rain_sim_val = r_val
    st.session_state.pct_boost = p_val
    st.session_state.storm_hours = h_val
    st.session_state["sl_rain"] = r_val
    st.session_state["sl_pct"] = p_val
    st.session_state["sl_hrs"] = h_val

def reset_all():
    st.session_state.selected_gov = "الكل"
    st.session_state.model_mode = "Random Forest"
    st.session_state.horizon_mode = "Nowcasting"
    st.session_state.hazard_type = "rain"
    st.session_state.map_layer = "rain"
    st.session_state.picked_station = "TA109"
    st.session_state.use_live_meteo = True
    set_scenario(0, 0, 6)

live_df = None
live_error = None
if st.session_state.use_live_meteo:
    try:
        live_df = fetch_open_meteo_7d()
    except Exception as exc:
        live_error = str(exc)

# شريط علوي واحد مضغوط
st.markdown('<div class="bar-box">', unsafe_allow_html=True)
r1, r2, r3, r4 = st.columns([2.1, 1.7, 1.7, 2.5])

with r1:
    st.markdown('<div class="mini-lbl">النطاق</div>', unsafe_allow_html=True)
    govs = ["الكل", "مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة"]
    gcols = st.columns(len(govs))
    for i, g in enumerate(govs):
        lbl = f"[{g}]" if st.session_state.selected_gov == g else g
        if gcols[i].button(lbl, key=f"g_{g}"):
            st.session_state.selected_gov = g
            st.rerun()

with r2:
    st.markdown('<div class="mini-lbl">سيناريو سريع</div>', unsafe_allow_html=True)
    scols = st.columns(5)
    if scols[0].button("عادي", key="s0"): set_scenario(0, 0, 6); st.rerun()
    if scols[1].button("متوسط", key="s1"): set_scenario(40, 15, 8); st.rerun()
    if scols[2].button("غزير", key="s2"): set_scenario(95, 35, 12); st.rerun()
    if scols[3].button("حرج", key="s3"): set_scenario(155, 60, 18); st.rerun()
    if scols[4].button("Reset", key="srst"): reset_all(); st.rerun()

with r3:
    st.markdown('<div class="mini-lbl">نموذج / أفق / مؤشر / حي</div>', unsafe_allow_html=True)
    mcols = st.columns(5)
    if mcols[0].button("RF" if st.session_state.model_mode == "Random Forest" else "AHP", key="m_tog"):
        st.session_state.model_mode = "AHP" if st.session_state.model_mode == "Random Forest" else "Random Forest"
        st.rerun()
    if mcols[1].button("+24h" if st.session_state.horizon_mode == "Nowcasting" else ("14d" if st.session_state.horizon_mode == "14d" else "موسمي"), key="h_tog"):
        order = ["Nowcasting", "14d", "Seasonal"]
        st.session_state.horizon_mode = order[(order.index(st.session_state.horizon_mode) + 1) % 3]
        st.rerun()
    if mcols[2].button("سيول" if st.session_state.hazard_type == "rain" else "عواصف", key="z_tog"):
        st.session_state.hazard_type = "wind" if st.session_state.hazard_type == "rain" else "rain"
        st.rerun()
    if mcols[3].button("هطول" if st.session_state.map_layer == "rain" else "AQI", key="l_tog"):
        st.session_state.map_layer = "aqi" if st.session_state.map_layer == "rain" else "rain"
        st.rerun()
    if mcols[4].button("حي" if st.session_state.use_live_meteo else "ثابت", key="live_tog"):
        st.session_state.use_live_meteo = not st.session_state.use_live_meteo
        st.rerun()

with r4:
    sc_sl1, sc_sl2, sc_sl3 = st.columns(3)
    st.session_state.rain_sim_val = sc_sl1.slider("+هطول مم", 0, 180, int(st.session_state.rain_sim_val), 5, key="sl_rain")
    st.session_state.pct_boost = sc_sl2.slider("What-If %", -20, 100, int(st.session_state.pct_boost), 5, key="sl_pct")
    st.session_state.storm_hours = sc_sl3.slider("مدة س", 2, 24, int(st.session_state.storm_hours), 2, key="sl_hrs")

st.markdown("</div>", unsafe_allow_html=True)

# الحسابات + دمج بيانات Open-Meteo الحية إن توفرت
out = df.copy()
if live_df is not None and not live_df.empty:
    meteo_map = live_df.set_index("city").to_dict("index")
    for idx_r, r_item in out.iterrows():
        m_info = meteo_map.get(r_item["Governorate"])
        if m_info:
            if m_info.get("temp_c") is not None:
                out.at[idx_r, "Temp_C"] = float(m_info["temp_c"])
            if m_info.get("humidity") is not None:
                out.at[idx_r, "Humidity_Pct"] = float(m_info["humidity"])
            if m_info.get("wind_kmh") is not None:
                out.at[idx_r, "Wind_kmh"] = float(m_info["wind_kmh"])
            if m_info.get("max_rain_7d") is not None and float(m_info["max_rain_7d"]) > 0:
                out.at[idx_r, "Hist_Mean_Rain"] = round(0.7 * float(r_item["Hist_Mean_Rain"]) + 0.3 * float(m_info["max_rain_7d"]), 1)

h_mult = 1.0 if st.session_state.horizon_mode == "Nowcasting" else (1.15 if st.session_state.horizon_mode == "14d" else 1.25)
dur_factor = 0.75 + (st.session_state.storm_hours / 12.0) * 0.45
pct_factor = 1.0 + (st.session_state.pct_boost / 100.0)

out["Rain_RF"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (st.session_state.rain_sim_val * 1.25)) * h_mult * dur_factor, 1)
out["Rain_AHP"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (st.session_state.rain_sim_val * 0.92)) * h_mult * dur_factor, 1)
out["Forecast_Rain"] = out["Rain_RF"] if st.session_state.model_mode == "Random Forest" else out["Rain_AHP"]
out["Eff_Soil_Sat_Pct"] = np.clip(out["Soil_Saturation_Pct"] + (out["Forecast_Rain"] * 0.12), 15.0, 100.0)
runoff_coeff = np.clip(0.22 + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.35 + out["Low_Perm_Factor"] * 0.32, 0.25, 0.92)
out["Runoff_m3s"] = np.round(out["Forecast_Rain"] * runoff_coeff * (1.2 + out["Elevation_m"] / 1600.0), 1)
out["Arrival_Hours"] = np.round(np.clip(6.5 - (out["Forecast_Rain"] / 70.0) + (out["Elevation_m"] / 1400.0), 1.2, 8.5), 1)
storm_boost = 1.0 if st.session_state.hazard_type == "rain" else 1.35
washout = np.where(out["Forecast_Rain"] > 90.0, 0.75, 1.0)
out["Eff_Wind_kmh"] = np.round(out["Wind_kmh"] * (1.0 + (st.session_state.rain_sim_val / 240.0) + (0.20 if st.session_state.hazard_type == "wind" else 0.0)), 0)
out["Eff_Dust_ugm3"] = np.round(np.maximum(15.0, out["Dust_ugm3"] * (1.0 + (out["Eff_Wind_kmh"] - 25.0) / 80.0) * washout), 0)
out["Eff_AQI"] = np.clip(np.round(out["AQI"] * 0.55 + (out["Eff_Dust_ugm3"] * 0.45) * storm_boost - (out["Forecast_Rain"] * 0.08)), 18, 260).astype(int)
out["Susceptibility_Idx"] = np.clip((out["Forecast_Rain"] / 260.0) * 0.50 + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.25 + out["Low_Perm_Factor"] * 0.25, 0.05, 0.99)

def get_alert(v, s):
    if v < 75 and s < 0.48: return "مستقر", [56, 189, 248, 255], min(v / 260.0, 1.0)
    if v < 135 and s < 0.65: return "تنبيه", [250, 204, 21, 255], min(v / 260.0, 1.0)
    if v < 190 and s < 0.80: return "حيطة", [251, 146, 60, 255], min(v / 260.0, 1.0)
    return "إنذار سيول", [248, 113, 113, 255], min(v / 260.0, 1.0)

meta = out.apply(lambda r: get_alert(r["Forecast_Rain"], r["Susceptibility_Idx"]), axis=1)
out["Alert_Level"] = [m[0] for m in meta]
out["Txt_Color"] = [m[1] for m in meta]
out["Heat_Weight"] = [min(r["Eff_AQI"] / 220.0, 1.0) for _, r in out.iterrows()] if st.session_state.map_layer == "aqi" else [m[2] for m in meta]
out["Map_Label"] = [f"{r['Station']} · {int(r['Eff_AQI'])} AQI" if st.session_state.map_layer == "aqi" else f"{r['Station']} · {r['Forecast_Rain']:.0f}mm" for _, r in out.iterrows()]

filtered = out if st.session_state.selected_gov == "الكل" else out[out["Governorate"] == st.session_state.selected_gov]
if st.session_state.picked_station not in filtered["Station"].tolist():
    st.session_state.picked_station = filtered.sort_values("Forecast_Rain", ascending=False).iloc[0]["Station"]
st_row = filtered[filtered["Station"] == st.session_state.picked_station].iloc[0]

city_meteo = None
if live_df is not None and not live_df.empty:
    m_sub = live_df[live_df["city"] == st_row["Governorate"]]
    if not m_sub.empty:
        city_meteo = m_sub.iloc[0]
    else:
        city_meteo = live_df.sort_values("max_rain_7d", ascending=False).iloc[0]

# صف 4 مؤشرات مضغوط
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-card"><div class="kpi-title">ذروة الهطول ({st.session_state.model_mode})</div><div class="kpi-val">{filtered["Forecast_Rain"].max():.1f} mm</div><div class="kpi-sub">What-If: {st.session_state.pct_boost:+d}% · {st.session_state.storm_hours}س</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi-card"><div class="kpi-title">مؤشر الحساسية (FSI)</div><div class="kpi-val">{filtered["Susceptibility_Idx"].mean():.2f}</div><div class="kpi-sub">تشبع التربة {filtered["Eff_Soil_Sat_Pct"].mean():.0f}%</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi-card"><div class="kpi-title">الجريان السطحي</div><div class="kpi-val">{filtered["Runoff_m3s"].mean():.1f} m³/s</div><div class="kpi-sub">وصول ~{filtered["Arrival_Hours"].mean():.1f} ساعة</div></div>', unsafe_allow_html=True)
if city_meteo is not None:
    meteo_tag = "تنبيه ≥20mm" if city_meteo["alert_7d"] else "طبيعي (7d)"
    k4.markdown(f'<div class="kpi-card"><div class="kpi-title">Open-Meteo ({city_meteo["city"]})</div><div class="kpi-val">{city_meteo["temp_c"]}° · {city_meteo["max_rain_7d"]}mm</div><div class="kpi-sub">{meteo_tag} · رطوبة {city_meteo["humidity"]}%</div></div>', unsafe_allow_html=True)
else:
    k4.markdown(f'<div class="kpi-card"><div class="kpi-title">جودة الهواء والرياح</div><div class="kpi-val">{int(filtered["Eff_AQI"].mean())} AQI</div><div class="kpi-sub">رياح {filtered["Eff_Wind_kmh"].mean():.0f} km/h</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)

# القسم الرئيسي: الخريطة الكبيرة + بطاقة المحطة والخطورة بجانبها بدون نزول طويل
main_map, main_side = st.columns([2.85, 1.15])

with main_map:
    st_labels = [f"{r['Station']} — {r['Basin']} ({r['Governorate']})" for _, r in filtered.iterrows()]
    st_codes = filtered["Station"].tolist()
    idx_sel = st_codes.index(st.session_state.picked_station)
    sel_lbl = st.selectbox("اختيار محطة", st_labels, index=idx_sel, label_visibility="collapsed", key="st_pick_box")
    new_st = st_codes[st_labels.index(sel_lbl)]
    if new_st != st.session_state.picked_station:
        st.session_state.picked_station = new_st
        st.rerun()
    st_row = filtered[filtered["Station"] == st.session_state.picked_station].iloc[0]

    color_rng = (
        [[56, 189, 248], [163, 230, 53], [250, 204, 21], [251, 146, 60], [220, 38, 38], [153, 27, 27]]
        if st.session_state.map_layer == "aqi"
        else [[186, 230, 253], [56, 189, 248], [2, 132, 199], [30, 64, 175], [251, 146, 60], [220, 38, 38]]
    )

    heat_pts = []
    for _, r in filtered.iterrows():
        w0 = float(r["Heat_Weight"])
        heat_pts.append({"lon": float(r["lon"]), "lat": float(r["lat"]), "w": w0})
        for dlat, dlon, fac in [(0.14, 0.0, 0.85), (-0.14, 0.0, 0.8), (0.0, 0.15, 0.85), (0.0, -0.15, 0.78)]:
            heat_pts.append({"lon": float(r["lon"]) + dlon, "lat": float(r["lat"]) + dlat, "w": max(0.08, min(w0 * fac, 1.0))})

    wadi_lines = [
        {
            "col": [248, 113, 113, 240] if r["Forecast_Rain"] >= 135 else [56, 189, 248, 230],
            "w": 4.5 if r["Forecast_Rain"] >= 135 else 2.8,
            "path": [[float(r["lon"]) + 0.10, float(r["lat"]) + 0.07], [float(r["lon"]), float(r["lat"])], [float(r["lon"]) - 0.16, float(r["lat"]) - 0.12]]
        }
        for _, r in filtered.iterrows()
    ]

    layers = [
        pdk.Layer("HeatmapLayer", data=pd.DataFrame(heat_pts), get_position=["lon", "lat"], get_weight="w", radius_pixels=110, intensity=1.2, threshold=0.04, color_range=color_rng),
        pdk.Layer("PolygonLayer", data=[{"polygon": makkah_boundary_coords}], get_polygon="polygon", get_fill_color=[56, 189, 248, 14], get_line_color=[125, 211, 252, 220], line_width_min_pixels=2.2, stroked=True, filled=True),
        pdk.Layer("PathLayer", data=wadi_lines, get_path="path", get_color="col", get_width="w", width_min_pixels=2.2),
        pdk.Layer("TextLayer", data=filtered, get_position=["lon", "lat"], get_text="Map_Label", get_color="Txt_Color", get_size=11, get_alignment_baseline="'bottom'", background=True, get_background_color=[8, 20, 38, 225], background_padding=[2, 4]),
        pdk.Layer("ScatterplotLayer", data=filtered[filtered["Station"] == st.session_state.picked_station], get_position=["lon", "lat"], get_fill_color=[255, 255, 255, 245], get_line_color=[239, 68, 68, 255], line_width_min_pixels=3.5, stroked=True, filled=True, get_radius=13000),
    ]

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=float(st_row["lat"]) if st.session_state.selected_gov != "الكل" or st.session_state.picked_station != "TA109" else 21.15,
            longitude=float(st_row["lon"]) if st.session_state.selected_gov != "الكل" or st.session_state.picked_station != "TA109" else 40.55,
            zoom=7.4 if st.session_state.selected_gov != "الكل" or st.session_state.picked_station != "TA109" else 6.75,
            pitch=0
        ),
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        tooltip={"html": "<b>{Station}</b> ({Governorate})<br/>{Basin}<br/>{Map_Label}", "style": {"backgroundColor": "#091b33", "color": "#ffffff"}}
    )
    st.pydeck_chart(deck, use_container_width=True, height=455)

    # شريط تدرج سفلي مدمج
    if st.session_state.map_layer == "aqi":
        pos = float(min(max((filtered["Eff_AQI"].mean() / 220.0) * 100.0, 2.0), 98.0))
        title_b = f"AQI: {int(filtered['Eff_AQI'].mean())} ({pos:.0f}%)"
        stops = [[0.0, "#38bdf8"], [0.3, "#a3e635"], [0.55, "#facc15"], [0.78, "#fb923c"], [1.0, "#dc2626"]]
    else:
        pos = float(min(max((st.session_state.rain_sim_val / 180.0) * 100.0, 2.0), 98.0))
        title_b = f"+هطول: {st.session_state.rain_sim_val} mm ({pos:.0f}%)"
        stops = [[0.0, "#bae6fd"], [0.3, "#38bdf8"], [0.6, "#1d4ed8"], [0.82, "#fb923c"], [1.0, "#ef4444"]]

    bfig = go.Figure(go.Heatmap(z=[np.linspace(0, 100, 101)], x=list(range(101)), y=[0], colorscale=stops, showscale=False, hoverinfo="skip"))
    bfig.add_trace(go.Scatter(x=[pos], y=[0], mode="markers", marker=dict(size=14, color="#ffffff", line=dict(color="#06101e", width=2.5)), showlegend=False))
    bfig.update_layout(
        title=dict(text=title_b, font=dict(size=10, color="#7dd3fc"), x=0.5, xanchor="center"),
        height=54, margin=dict(l=12, r=12, t=20, b=10),
        paper_bgcolor="#081426", plot_bgcolor="#081426",
        xaxis=dict(range=[0, 100], tickvals=[0, 50, 100], ticktext=["منخفض", "متوسط", "مرتفع"], tickfont=dict(size=9, color="#cbd5e1"), showgrid=False, zeroline=False),
        yaxis=dict(visible=False, range=[-0.5, 0.5])
    )
    st.plotly_chart(bfig, use_container_width=True, config={"displayModeBar": False})

with main_side:
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(float(filtered["Susceptibility_Idx"].mean()) * 100, 1),
        number={"suffix": "%", "font": {"size": 18, "color": "#ffffff"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94b2d6"},
            "bar": {"color": "#38bdf8"},
            "bgcolor": "#081426",
            "steps": [{"range": [0, 35], "color": "#0f294a"}, {"range": [35, 65], "color": "#2b2514"}, {"range": [65, 100], "color": "#3b1720"}]
        }
    ))
    gauge.update_layout(height=135, margin=dict(l=8, r=8, t=8, b=0), paper_bgcolor="#0c1c34", font={"color": "#e6eef8"})
    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})

    meteo_line = ""
    if city_meteo is not None:
        w_badge = "تنبيه ≥20mm" if city_meteo["alert_7d"] else "طبيعي"
        meteo_line = f"<div>Open-Meteo ({city_meteo['city']}): <b>{city_meteo['max_rain_7d']}mm</b> (7d) · {w_badge}</div>"
    elif live_error:
        meteo_line = "<div style='color:#f87171;'>تعذر جلب Open-Meteo حالياً</div>"

    st.markdown(f"""
        <div class="side-box">
            <div style="color:#7dd3fc;font-weight:700;">{st_row["Station"]} · {st_row["Governorate"]}</div>
            <div>الحالة: <b>{st_row["Alert_Level"]}</b> · {st_row["Forecast_Rain"]:.1f} mm</div>
            <div>الحوض: {st_row["Basin"]}</div>
            <div>وصول الجريان: ~{st_row["Arrival_Hours"]} س · الجريان: {st_row["Runoff_m3s"]:.1f} m³/s</div>
            {meteo_line}
        </div>
    """, unsafe_allow_html=True)

    tfig = go.Figure()
    if city_meteo is not None and len(city_meteo["daily_rain"]) == 7:
        xs = [d[-5:] if isinstance(d, str) and len(d) >= 5 else f"ي{i+1}" for i, d in enumerate(city_meteo["daily_dates"])]
        ys = city_meteo["daily_rain"]
    else:
        xs = [f"+{i*3}h" for i in range(9)]
        y0 = float(st_row["Forecast_Rain"])
        ys = np.round(y0 * (0.75 + 0.25 * np.sin(np.linspace(0, 3.14, 9))), 1)
    tfig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color="#38bdf8", width=2), marker=dict(size=4)))
    tfig.update_layout(
        height=145, margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="#0c1c34", plot_bgcolor="#081426",
        font={"color": "#cbd5e1", "size": 9},
        xaxis=dict(gridcolor="#162c4d"), yaxis=dict(gridcolor="#162c4d")
    )
    st.plotly_chart(tfig, use_container_width=True, config={"displayModeBar": False})
