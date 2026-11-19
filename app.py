import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go

st.set_page_config(
    page_title="RASD — منظومة التنبؤ والإنذار المبكر بالطقس والسيول",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* الواجهة الرئيسية الكحلية */
    .stApp {
        background-color: #06101e;
        color: #e6eef8;
    }
    /* الشريط الجانبي السماوي */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #bae6fd 0%, #7dd3fc 55%, #38bdf8 100%);
        border-right: 1px solid #0284c7;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #062038 !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * {
        background-color: #071b33 !important;
        color: #ffffff !important;
        border: 1px solid #0284c7 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100%;
    }
    .stButton > button,
    .stButton > button * {
        background-color: #0d2240 !important;
        color: #e2e8f0 !important;
        border: 1px solid #234675 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover,
    .stButton > button:hover * {
        background-color: #133461 !important;
        color: #7dd3fc !important;
        border-color: #38bdf8 !important;
    }
    /* الشريط العلوي الكحلي */
    .rasd-header {
        background: linear-gradient(90deg, #091b33 0%, #0e2647 100%);
        border: 1px solid #1d3b66;
        border-radius: 10px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 14px rgba(2, 8, 20, 0.45);
    }
    .brand-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .brand-badge {
        background-color: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #7dd3fc;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
    }
    .header-meta {
        font-size: 11px;
        color: #9cb8dc;
        text-align: right;
    }
    .live-strip {
        background: linear-gradient(90deg, rgba(14, 116, 144, 0.24) 0%, rgba(12, 28, 52, 0.95) 100%);
        border: 1px solid #254b7a;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        font-size: 12px;
    }
    .live-pill {
        background-color: rgba(6, 16, 30, 0.75);
        border: 1px solid #234675;
        border-radius: 6px;
        padding: 4px 10px;
        color: #e2e8f0;
    }
    .full-region-bar {
        background-color: #091930;
        border: 1px solid #1e3a60;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 12px;
    }
    .bar-label {
        font-size: 11px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 5px;
    }
    /* الصف العلوي: 4 كروت أرقام */
    .top-kpi {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 10px;
        padding: 13px 16px;
        box-shadow: 0 3px 10px rgba(2, 8, 20, 0.3);
        min-height: 116px;
    }
    .top-kpi-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .top-kpi-title {
        font-size: 11px;
        color: #94b2d6;
        font-weight: 600;
    }
    .trend-up {
        font-size: 11px;
        font-weight: 700;
        color: #f87171;
        background: rgba(248, 113, 113, 0.12);
        padding: 2px 6px;
        border-radius: 5px;
    }
    .trend-down {
        font-size: 11px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        padding: 2px 6px;
        border-radius: 5px;
    }
    .trend-flat {
        font-size: 11px;
        font-weight: 700;
        color: #facc15;
        background: rgba(250, 204, 21, 0.12);
        padding: 2px 6px;
        border-radius: 5px;
    }
    .top-kpi-val {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    .top-kpi-unit {
        font-size: 13px;
        font-weight: 500;
        color: #7dd3fc;
    }
    .top-kpi-sub {
        font-size: 11px;
        color: #94b2d6;
        margin-top: 5px;
    }
    /* الكروت الوسطى والسفلية */
    .card-box {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 3px 10px rgba(2, 8, 20, 0.3);
        margin-bottom: 14px;
    }
    .card-title {
        font-size: 13px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 8px;
    }
    .card-sub {
        font-size: 11px;
        color: #94b2d6;
    }
    .dark-side-card {
        background: linear-gradient(180deg, #0d2340 0%, #091629 100%);
        border: 1px solid #234675;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 14px rgba(2, 8, 20, 0.4);
        margin-bottom: 14px;
    }
    .alert-banner {
        background-color: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.32);
        border-radius: 8px;
        padding: 10px 12px;
        margin: 10px 0;
    }
    .legend-strip {
        font-size: 11px;
        color: #cbd5e1;
        margin-top: 8px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .sector-row {
        padding: 8px 0;
        border-bottom: 1px solid #183052;
        font-size: 12px;
        line-height: 1.5;
    }
    .sector-row:last-child {
        border-bottom: none;
    }
    .public-box {
        background: rgba(14, 116, 144, 0.20);
        border: 1px solid rgba(56, 189, 248, 0.40);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 14px;
    }
    .summary-box {
        background-color: #081426;
        border: 1px solid #234675;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 12px;
        color: #e2e8f0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# حدود منطقة مكة المكرمة (منطقة الدراسة)
makkah_boundary_coords = [
    [38.88, 22.92],
    [39.32, 23.12],
    [39.85, 22.85],
    [40.45, 22.78],
    [41.15, 22.65],
    [41.85, 22.55],
    [42.55, 22.35],
    [42.95, 21.85],
    [42.80, 21.20],
    [42.20, 20.65],
    [41.65, 20.15],
    [41.45, 19.55],
    [41.20, 19.05],
    [40.82, 19.35],
    [40.68, 19.95],
    [40.25, 20.15],
    [39.82, 20.75],
    [39.38, 21.35],
    [39.05, 21.95],
    [38.88, 22.92]
]

# 26 محطة MEWA مستندة إلى خريطة منطقة مكة المكرمة (1964–2014)
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

df = pd.DataFrame(stations_data, columns=[
    "Station", "Governorate", "Basin", "Hotspot", "lon", "lat",
    "Hist_Mean_Rain", "Elevation_m", "Soil_Saturation_Pct", "Low_Perm_Factor",
    "Temp_C", "Humidity_Pct", "Pressure_hPa", "Wind_kmh", "Dust_ugm3",
    "AQI", "UV_Index", "Dist_Nearest_km"
])
df["Extrapolated_Low_Conf"] = df["Dist_Nearest_km"] > 50.0

coastal_govs = {"جدة", "الليث", "القنفذة"}

defaults = {
    "audience_mode": "للجهة والقطاعات (Technical)",
    "selected_gov": "الكل",
    "model_mode": "Random Forest",
    "horizon_mode": "التنبؤ الآني (Nowcasting - 24h)",
    "hazard_type": "الأمطار الغزيرة والسيول",
    "map_layer": "الهطول والإنذار (مم)",
    "rain_sim_val": 0,
    "pct_boost": 0,
    "storm_hours": 6,
    "show_boundary": True,
    "show_terrain": True,
    "show_wadis": True,
    "show_basins": True,
    "picked_station": "TA109",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_all_controls():
    st.session_state.selected_gov = "الكل"
    st.session_state.model_mode = "Random Forest"
    st.session_state.horizon_mode = "التنبؤ الآني (Nowcasting - 24h)"
    st.session_state.hazard_type = "الأمطار الغزيرة والسيول"
    st.session_state.map_layer = "الهطول والإنذار (مم)"
    st.session_state.rain_sim_val = 0
    st.session_state.pct_boost = 0
    st.session_state.storm_hours = 6
    st.session_state.show_boundary = True
    st.session_state.show_terrain = True
    st.session_state.show_wadis = True
    st.session_state.show_basins = True
    st.session_state.picked_station = "TA109"

# الشريط الجانبي السماوي للتحكم والسيناريوهات
st.sidebar.header("لوحة التحكم والسيناريوهات")
aud_choice = st.sidebar.radio(
    "زاوية العرض",
    ["للجهة والقطاعات (Technical)", "للفرد والسكان (Public)"],
    index=0 if st.session_state.audience_mode.startswith("للجهة") else 1
)
st.session_state.audience_mode = aud_choice

st.sidebar.markdown("**سيناريوهات جاهزة + Reset:**")
sb1, sb2 = st.sidebar.columns(2)
if sb1.button("وضع طبيعي", key="sb_norm"):
    st.session_state.rain_sim_val = 0
    st.session_state.pct_boost = 0
if sb2.button("هطول متوسط", key="sb_mod"):
    st.session_state.rain_sim_val = 40
    st.session_state.pct_boost = 15

sb3, sb4 = st.sidebar.columns(2)
if sb3.button("عاصفة غزيرة", key="sb_heavy"):
    st.session_state.rain_sim_val = 95
    st.session_state.pct_boost = 35
if sb4.button("سيناريو حرج", key="sb_crit"):
    st.session_state.rain_sim_val = 155
    st.session_state.pct_boost = 60

if st.sidebar.button("إعادة ضبط سريعة (Reset)", key="sb_reset"):
    reset_all_controls()

st.session_state.rain_sim_val = st.sidebar.slider(
    "محاكاة زيادة الهطول (مم)", 0, 180, int(st.session_state.rain_sim_val), 5
)
st.session_state.pct_boost = st.sidebar.slider(
    "نسبة تغير الهطول What-If (%)", -20, 100, int(st.session_state.pct_boost), 5
)
st.session_state.storm_hours = st.sidebar.slider(
    "مدة العاصفة / الهطول (ساعات)", 2, 24, int(st.session_state.storm_hours), 2
)

def compute_hydro(base_df, rain_extra, pct_chg, dur_hrs, h_mode, m_mode, m_layer, h_type):
    out = base_df.copy()
    h_mult = 1.0 if "Nowcasting" in h_mode else (1.15 if "14 Days" in h_mode else 1.25)
    dur_factor = 0.75 + (dur_hrs / 12.0) * 0.45
    pct_factor = 1.0 + (pct_chg / 100.0)

    out["Rain_RF"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (rain_extra * 1.25)) * h_mult * dur_factor, 1)
    out["Rain_AHP"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (rain_extra * 0.92)) * h_mult * dur_factor, 1)
    out["Forecast_Rain"] = out["Rain_RF"] if m_mode == "Random Forest" else out["Rain_AHP"]

    out["Eff_Soil_Sat_Pct"] = np.clip(out["Soil_Saturation_Pct"] + (out["Forecast_Rain"] * 0.12), 15.0, 100.0)
    runoff_coeff = np.clip(0.22 + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.35 + out["Low_Perm_Factor"] * 0.32, 0.25, 0.92)
    out["Runoff_m3s"] = np.round(out["Forecast_Rain"] * runoff_coeff * (1.2 + out["Elevation_m"] / 1600.0), 1)
    out["Arrival_Hours"] = np.round(np.clip(6.5 - (out["Forecast_Rain"] / 70.0) + (out["Elevation_m"] / 1400.0), 1.2, 8.5), 1)

    storm_boost = 1.0 if "الأمطار" in h_type else 1.35
    washout_factor = np.where(out["Forecast_Rain"] > 90.0, 0.75, 1.0)
    out["Eff_Wind_kmh"] = np.round(
        out["Wind_kmh"] * (1.0 + (rain_extra / 240.0) + (0.20 if "العواصف" in h_type else 0.0)),
        0
    )
    out["Eff_Dust_ugm3"] = np.round(
        np.maximum(15.0, out["Dust_ugm3"] * (1.0 + (out["Eff_Wind_kmh"] - 25.0) / 80.0) * washout_factor),
        0
    )
    out["Eff_AQI"] = np.clip(
        np.round(out["AQI"] * 0.55 + (out["Eff_Dust_ugm3"] * 0.45) * storm_boost - (out["Forecast_Rain"] * 0.08)),
        18,
        260
    ).astype(int)

    out["Susceptibility_Idx"] = np.clip(
        (out["Forecast_Rain"] / 260.0) * 0.50
        + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.25
        + out["Low_Perm_Factor"] * 0.25,
        0.05,
        0.99
    )
    out["Dew_Point_C"] = np.round(out["Temp_C"] - ((100.0 - out["Humidity_Pct"]) / 5.0), 1)

    def _row_meta(r_item):
        rain_v = float(r_item["Forecast_Rain"])
        susc_v = float(r_item["Susceptibility_Idx"])
        if rain_v < 75 and susc_v < 0.48:
            a_lbl, t_col = "أزرق · مستقر", [3, 105, 161, 255]
            adv_txt = "حالة مستقرة؛ متابعة اعتيادية للأجواء ومجاري الأودية ضمن منطقة مكة المكرمة."
        elif rain_v < 135 and susc_v < 0.65:
            a_lbl, t_col = "أصفر · تنبيه مبكر", [161, 98, 7, 255]
            adv_txt = "تنبيه مبكر؛ تشبع جزئي للتربة واحتمال جريان متوسط في الشعاب والأودية."
        elif rain_v < 190 and susc_v < 0.80:
            a_lbl, t_col = "برتقالي · حيطة وحذر", [194, 65, 12, 255]
            adv_txt = "حيطة وحذر؛ جريان نشط محتمل وتجنب نقاط الاختناق والأودية."
        else:
            a_lbl, t_col = "أحمر · إنذار سيول شديد", [185, 28, 28, 255]
            adv_txt = "إنذار سيول شديد؛ سرعة استجابة عالية وتجنب بطون الأودية فوراً."

        if "AQI" in m_layer:
            aq_val = float(r_item["Eff_AQI"])
            w_val = min(aq_val / 220.0, 1.0)
            read_txt = f"AQI {int(aq_val)}"
        else:
            w_val = min(rain_v / 260.0, 1.0)
            read_txt = f"{rain_v:.1f} mm"

        conf_tag = " (>50km)" if bool(r_item["Extrapolated_Low_Conf"]) else ""
        return a_lbl, t_col, adv_txt, w_val, read_txt, f"{r_item['Station']} · {read_txt}{conf_tag}"

    meta_res = out.apply(_row_meta, axis=1)
    out["Alert_Level"] = [x[0] for x in meta_res]
    out["Txt_Color"] = [x[1] for x in meta_res]
    out["Advice"] = [x[2] for x in meta_res]
    out["Heat_Weight"] = [x[3] for x in meta_res]
    out["Reading_Str"] = [x[4] for x in meta_res]
    out["Map_Label"] = [x[5] for x in meta_res]
    return out

baseline_df = compute_hydro(
    df, 0, 0, 6,
    "التنبؤ الآني (Nowcasting - 24h)",
    "Random Forest",
    "الهطول والإنذار (مم)",
    "الأمطار الغزيرة والسيول"
)
sim_all_df = compute_hydro(
    df,
    st.session_state.rain_sim_val,
    st.session_state.pct_boost,
    st.session_state.storm_hours,
    st.session_state.horizon_mode,
    st.session_state.model_mode,
    st.session_state.map_layer,
    st.session_state.hazard_type
)

if st.session_state.selected_gov == "الكل":
    filtered = sim_all_df.copy()
    base_filt = baseline_df.copy()
else:
    filtered = sim_all_df[sim_all_df["Governorate"] == st.session_state.selected_gov].copy()
    base_filt = baseline_df[baseline_df["Governorate"] == st.session_state.selected_gov].copy()

station_list = filtered["Station"].tolist()
if st.session_state.picked_station not in station_list:
    st.session_state.picked_station = filtered.sort_values("Forecast_Rain", ascending=False).iloc[0]["Station"]

st_row = filtered[filtered["Station"] == st.session_state.picked_station].iloc[0]
top_st = st_row

avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_risk = filtered["Susceptibility_Idx"].mean()
avg_runoff = filtered["Runoff_m3s"].mean()
avg_soil = filtered["Eff_Soil_Sat_Pct"].mean()
avg_arrival = filtered["Arrival_Hours"].mean()
avg_aqi = int(filtered["Eff_AQI"].mean())
severe_cnt = int((filtered["Forecast_Rain"] >= 135).sum())

diff_rain = avg_rain - base_filt["Forecast_Rain"].mean()
diff_runoff = avg_runoff - base_filt["Runoff_m3s"].mean()
diff_risk = avg_risk - base_filt["Susceptibility_Idx"].mean()
diff_aqi = avg_aqi - int(base_filt["Eff_AQI"].mean())

audience_mode = st.session_state.audience_mode
model_mode = st.session_state.model_mode
horizon_mode = st.session_state.horizon_mode
hazard_type = st.session_state.hazard_type
map_layer = st.session_state.map_layer
rain_add = st.session_state.rain_sim_val
pct_boost = st.session_state.pct_boost
storm_hours = st.session_state.storm_hours

source_tag = (
    "المرجع التاريخي (1964–2014)"
    if (rain_add == 0 and pct_boost == 0 and storm_hours == 6)
    else f"+{rain_add} مم · ({pct_boost:+d}% / {storm_hours} س)"
)

# 1) الشريط العلوي الرئيسي
st.markdown(f"""
    <div class="rasd-header">
        <div>
            <span class="brand-title">RASD</span>
            <span class="brand-badge">منطقة مكة المكرمة</span>
            <span class="brand-badge">{st.session_state.selected_gov}</span>
            <span class="brand-badge">{st_row["Station"]}</span>
            <span class="brand-badge">{model_mode}</span>
        </div>
        <div class="header-meta">
            <div><b>{source_tag}</b> · 26 محطة MEWA (حدود منطقة الدراسة)</div>
            <div>{audience_mode} · {horizon_mode}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2) شريط المناطق التفاعلي بالعرض الكامل في الأعلى
st.markdown('<div class="full-region-bar"><div class="bar-label">نطاقات منطقة مكة المكرمة (نقرة واحدة لتحديث اللوحة والمنطقة والإنذار)</div>', unsafe_allow_html=True)
gov_buttons = ["الكل", "مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة"]
g_cols = st.columns(len(gov_buttons))
for idx_g, g_name in enumerate(gov_buttons):
    g_sub = sim_all_df if g_name == "الكل" else sim_all_df[sim_all_df["Governorate"] == g_name]
    g_max = g_sub["Forecast_Rain"].max()
    dot = "🔴" if g_max >= 190 else ("🟠" if g_max >= 135 else ("🟡" if g_max >= 75 else "🔵"))
    active_mark = "✦ " if st.session_state.selected_gov == g_name else ""
    if g_cols[idx_g].button(f"{active_mark}{dot} {g_name}", key=f"gov_btn_{g_name}"):
        st.session_state.selected_gov = g_name
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# شريط الحالة الفورية
st.markdown(f"""
    <div class="live-strip">
        <div>
            <span style="color:#7dd3fc;font-weight:700;">المحطة المحددة ({st_row["Station"]} · {st_row["Governorate"]}):</span>
            <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]}
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            <span class="live-pill">الحوض: <b>{top_st["Basin"]}</b></span>
            <span class="live-pill">نقطة حرجة: <b>{top_st["Hotspot"]}</b></span>
            <span class="live-pill">وصول الجريان: <b>~{top_st["Arrival_Hours"]} س</b></span>
            <span class="live-pill">تشبع التربة: <b>{top_st["Eff_Soil_Sat_Pct"]:.0f}%</b></span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3) أزرار التبديل المباشرة للنموذج والأفق والظاهرة والمؤشر
r2_1, r2_2, r2_3, r2_4 = st.columns([1.2, 1.4, 1.3, 1.3])
with r2_1:
    st.markdown('<div class="bar-label">النموذج</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    if m1.button(("✦ " if model_mode == "Random Forest" else "") + "RF", key="btn_rf"):
        st.session_state.model_mode = "Random Forest"
        st.rerun()
    if m2.button(("✦ " if model_mode == "AHP" else "") + "AHP", key="btn_ahp"):
        st.session_state.model_mode = "AHP"
        st.rerun()

with r2_2:
    st.markdown('<div class="bar-label">الأفق الزمني</div>', unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    if h1.button(("✦ " if "Nowcasting" in horizon_mode else "") + "24h", key="btn_now"):
        st.session_state.horizon_mode = "التنبؤ الآني (Nowcasting - 24h)"
        st.rerun()
    if h2.button(("✦ " if "14 Days" in horizon_mode else "") + "14d", key="btn_14d"):
        st.session_state.horizon_mode = "التوقعات الممتدة (14 Days)"
        st.rerun()
    if h3.button(("✦ " if "Seasonal" in horizon_mode else "") + "موسمي", key="btn_seas"):
        st.session_state.horizon_mode = "النماذج الفصلية (Seasonal)"
        st.rerun()

with r2_3:
    st.markdown('<div class="bar-label">الظاهرة</div>', unsafe_allow_html=True)
    z1, z2 = st.columns(2)
    if z1.button(("✦ " if "الأمطار" in hazard_type else "") + "سيول", key="btn_hz_rain"):
        st.session_state.hazard_type = "الأمطار الغزيرة والسيول"
        st.rerun()
    if z2.button(("✦ " if "العواصف" in hazard_type else "") + "عواصف", key="btn_hz_wind"):
        st.session_state.hazard_type = "العواصف الرعدية والرياح"
        st.rerun()

with r2_4:
    st.markdown('<div class="bar-label">مؤشر الخريطة</div>', unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    if l1.button(("✦ " if "الهطول" in map_layer else "") + "هطول", key="btn_ml_rain"):
        st.session_state.map_layer = "الهطول والإنذار (مم)"
        st.rerun()
    if l2.button(("✦ " if "AQI" in map_layer else "") + "AQI", key="btn_ml_aqi"):
        st.session_state.map_layer = "جودة الهواء (AQI)"
        st.rerun()

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# 4) الصف الأول: 4 كروت أرقام
trend_rain_cls = "trend-up" if diff_rain > 2 else ("trend-down" if diff_rain < -2 else "trend-flat")
trend_rain_lbl = f"↑ +{diff_rain:.1f} mm" if diff_rain > 2 else (f"↓ {diff_rain:.1f} mm" if diff_rain < -2 else "→ 0.0 mm")

trend_risk_cls = "trend-up" if diff_risk > 0.02 else ("trend-down" if diff_risk < -0.02 else "trend-flat")
trend_risk_lbl = f"↑ +{diff_risk:.2f}" if diff_risk > 0.02 else (f"↓ {diff_risk:.2f}" if diff_risk < -0.02 else "→ مستقر")

trend_runoff_cls = "trend-up" if diff_runoff > 3 else ("trend-down" if diff_runoff < -3 else "trend-flat")
trend_runoff_lbl = f"↑ +{diff_runoff:.1f}" if diff_runoff > 3 else (f"↓ {diff_runoff:.1f}" if diff_runoff < -3 else "→ ثابت")

trend_aqi_cls = "trend-up" if diff_aqi > 5 else ("trend-down" if diff_aqi < -5 else "trend-flat")
trend_aqi_lbl = f"↑ +{diff_aqi} AQI" if diff_aqi > 5 else (f"↓ {diff_aqi} AQI" if diff_aqi < -5 else "→ معتدل")

c1, c2, c3, c4 = st.columns(4)
if audience_mode.startswith("للفرد"):
    status_txt = "إنذار أحمر/برتقالي" if severe_cnt >= 3 else ("تنبيه أصفر" if severe_cnt > 0 else "مستقر · أزرق")
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">حالة المنطقة والإنذار</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val" style="font-size:19px;color:#7dd3fc;">{status_txt}</div><div class="top-kpi-sub">{hazard_type} · وصول متوقع خلال {avg_arrival:.1f} س</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">متوسط الهطول ({source_tag})</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_rain:+.1f} mm · الذروة {max_rain:.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الحرارة والرياح</span><span class="trend-flat">→ {filtered["Eff_Wind_kmh"].mean():.0f} km/h</span></div><div class="top-kpi-val">{filtered["Temp_C"].mean():.1f} <span class="top-kpi-unit">°C</span></div><div class="top-kpi-sub">رطوبة {filtered["Humidity_Pct"].mean():.0f}% · ندى {filtered["Dew_Point_C"].mean():.1f}°C</div></div>""",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">جودة الهواء والغبار (AQI)</span><span class="{trend_aqi_cls}">{trend_aqi_lbl}</span></div><div class="top-kpi-val">{avg_aqi} <span class="top-kpi-unit">AQI</span></div><div class="top-kpi-sub">غبار {filtered["Eff_Dust_ugm3"].mean():.0f} µg/m³ · UV {int(filtered["UV_Index"].mean())}</div></div>""",
        unsafe_allow_html=True
    )
else:
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الذروة ضمن الحدود ({model_mode})</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{max_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">RF: {filtered["Rain_RF"].mean():.1f} mm · AHP: {filtered["Rain_AHP"].mean():.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">مؤشر الحساسية (FSI)</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val">{avg_risk:.2f}</div><div class="top-kpi-sub">تشبع التربة: {avg_soil:.0f}% · نفاذية منخفضة {filtered["Low_Perm_Factor"].mean():.2f}</div></div>""",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الجريان السطحي للأودية</span><span class="{trend_runoff_cls}">{trend_runoff_lbl}</span></div><div class="top-kpi-val">{avg_runoff:.1f} <span class="top-kpi-unit">m³/s</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_runoff:+.1f} m³/s · وصول ~{avg_arrival:.1f} س</div></div>""",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الرياح وجودة الهواء (AQI)</span><span class="{trend_aqi_cls}">{trend_aqi_lbl}</span></div><div class="top-kpi-val">{avg_aqi} <span class="top-kpi-unit">AQI</span></div><div class="top-kpi-sub">رياح {filtered["Eff_Wind_kmh"].mean():.0f} km/h · غبار {filtered["Eff_Dust_ugm3"].mean():.0f} µg/m³</div></div>""",
        unsafe_allow_html=True
    )

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

if audience_mode.startswith("للفرد"):
    st.markdown(f"""
        <div class="public-box">
            <div style="font-size:13px;font-weight:700;color:#7dd3fc;">ماذا يعني هذا لك الآن؟ ({top_st["Governorate"]} · {top_st["Station"]})</div>
            <div style="font-size:12px;color:#f1f5f9;margin-top:4px;">
                مستوى الحالة الحالي: <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]}
                الزمن التقديري لوصول الجريان قرب <b>{top_st["Hotspot"]}</b> هو <b>{top_st["Arrival_Hours"]} ساعة</b>، وجودة الهواء الحالية <b>{avg_aqi} AQI</b>.
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5) الصف الأوسط: خريطة منطقة الدراسة الفعّالة + مؤشر الخطورة وبطاقة الإنذار
m_center, m_side = st.columns([2.65, 1.35])

with m_center:
    st.markdown(
        f'<div class="card-box"><div class="card-title">خريطة منطقة مكة المكرمة الفعّالة (حدود الدراسة و26 محطة MEWA) · {map_layer}</div>',
        unsafe_allow_html=True
    )

    t_col0, t_col1, t_col2, t_col3 = st.columns(4)
    if t_col0.button(("● " if st.session_state.show_boundary else "○ ") + "حدود المنطقة", key="btn_l_bound"):
        st.session_state.show_boundary = not st.session_state.show_boundary
        st.rerun()
    if t_col1.button(("● " if st.session_state.show_terrain else "○ ") + "تأثير المرتفعات", key="btn_l_terr"):
        st.session_state.show_terrain = not st.session_state.show_terrain
        st.rerun()
    if t_col2.button(("● " if st.session_state.show_wadis else "○ ") + "مسار الأودية", key="btn_l_wadi"):
        st.session_state.show_wadis = not st.session_state.show_wadis
        st.rerun()
    if t_col3.button(("● " if st.session_state.show_basins else "○ ") + "الأحواض المائية", key="btn_l_basin"):
        st.session_state.show_basins = not st.session_state.show_basins
        st.rerun()

    # اختيار سريع متزامن لأي محطة من النطاق الحالي ليتركز عليها المؤشر والمنحنى
    st_options = [
        f"{r['Station']} — {r['Basin']} ({r['Governorate']} | {r['Reading_Str']})"
        for _, r in filtered.iterrows()
    ]
    st_codes = filtered["Station"].tolist()
    curr_idx = st_codes.index(st.session_state.picked_station) if st.session_state.picked_station in st_codes else 0
    chosen_label = st.selectbox(
        "تحديد محطة نشطة على الخريطة والمنحنى الزمني",
        options=st_options,
        index=curr_idx,
        key="map_station_selector"
    )
    new_station = st_codes[st_options.index(chosen_label)]
    if new_station != st.session_state.picked_station:
        st.session_state.picked_station = new_station
        st.rerun()

    st_row = filtered[filtered["Station"] == st.session_state.picked_station].iloc[0]
    top_st = st_row

    if "AQI" in map_layer:
        climate_color_range = [
            [56, 189, 248],
            [163, 230, 53],
            [250, 204, 21],
            [251, 146, 60],
            [220, 38, 38],
            [153, 27, 27]
        ]
    else:
        climate_color_range = [
            [186, 230, 253],
            [56, 189, 248],
            [2, 132, 199],
            [30, 64, 175],
            [251, 146, 60],
            [220, 38, 38]
        ]

    heat_points = []
    for _, r_item in filtered.iterrows():
        base_w = float(r_item["Heat_Weight"])
        elev_boost = min(float(r_item["Elevation_m"]) / 2400.0, 0.22) if (st.session_state.show_terrain and "AQI" not in map_layer) else 0.0
        w_main = min(base_w + elev_boost, 1.0)
        heat_points.append({"lon": float(r_item["lon"]), "lat": float(r_item["lat"]), "w": w_main})
        for d_lat, d_lon, factor in [
            (0.15, 0.0, 0.85), (-0.15, 0.0, 0.80),
            (0.0, 0.16, 0.85), (0.0, -0.16, 0.78),
            (0.11, 0.12, 0.72), (-0.11, -0.12, 0.72),
        ]:
            heat_points.append({
                "lon": float(r_item["lon"]) + d_lon,
                "lat": float(r_item["lat"]) + d_lat,
                "w": max(0.08, min(w_main * factor, 1.0))
            })

    active_df = filtered[filtered["Station"] == st.session_state.picked_station]

    map_layers = [
        pdk.Layer(
            "HeatmapLayer",
            data=pd.DataFrame(heat_points),
            get_position=["lon", "lat"],
            get_weight="w",
            radius_pixels=115,
            intensity=1.25,
            threshold=0.04,
            color_range=climate_color_range,
        ),
        pdk.Layer(
            "TextLayer",
            data=filtered,
            get_position=["lon", "lat"],
            get_text="Map_Label",
            get_color="Txt_Color",
            get_size=12,
            get_alignment_baseline="'bottom'",
            background=True,
            get_background_color=[255, 255, 255, 235],
            background_padding=[3, 6],
            pickable=True,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=active_df,
            get_position=["lon", "lat"],
            get_fill_color=[255, 255, 255, 230],
            get_line_color=[220, 38, 38, 255],
            line_width_min_pixels=3.5,
            stroked=True,
            filled=True,
            get_radius=14000,
            pickable=True,
        )
    ]

    if st.session_state.show_boundary:
        map_layers.append(pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": makkah_boundary_coords, "name": "حدود منطقة مكة المكرمة (منطقة الدراسة)"}],
            get_polygon="polygon",
            get_fill_color=[14, 165, 233, 18],
            get_line_color=[15, 23, 42, 240],
            line_width_min_pixels=3.0,
            stroked=True,
            filled=True,
            pickable=True,
        ))

    if st.session_state.show_basins and len(filtered) > 0:
        basin_rings = [
            {
                "basin": r_row["Basin"],
                "hotspot": r_row["Hotspot"],
                "path": [
                    [float(r_row["lon"]) - 0.14, float(r_row["lat"]) - 0.10],
                    [float(r_row["lon"]) + 0.14, float(r_row["lat"]) - 0.10],
                    [float(r_row["lon"]) + 0.14, float(r_row["lat"]) + 0.10],
                    [float(r_row["lon"]) - 0.14, float(r_row["lat"]) + 0.10],
                    [float(r_row["lon"]) - 0.14, float(r_row["lat"]) - 0.10],
                ]
            }
            for _, r_row in filtered.iterrows()
        ]
        map_layers.append(pdk.Layer(
            "PathLayer",
            data=basin_rings,
            get_path="path",
            get_color=[30, 58, 138, 120],
            width_min_pixels=1.4,
            pickable=True,
        ))

    if st.session_state.show_wadis and len(filtered) > 0:
        wadi_paths = []
        for _, r_row in filtered.iterrows():
            sev_high = r_row["Forecast_Rain"] >= 135
            w_col = [185, 28, 28, 235] if sev_high else [3, 105, 161, 215]
            w_px = 4.5 if sev_high else 2.5
            wadi_paths.append({
                "basin": r_row["Basin"],
                "hotspot": r_row["Hotspot"],
                "arrival": f"{r_row['Arrival_Hours']} س",
                "w_col": w_col,
                "w_px": w_px,
                "path": [
                    [float(r_row["lon"]) + 0.11, float(r_row["lat"]) + 0.08],
                    [float(r_row["lon"]), float(r_row["lat"])],
                    [float(r_row["lon"]) - 0.18, float(r_row["lat"]) - 0.14]
                ]
            })
        map_layers.append(pdk.Layer(
            "PathLayer",
            data=wadi_paths,
            get_path="path",
            get_color="w_col",
            get_width="w_px",
            width_min_pixels=2.0,
            pickable=True,
        ))

    if st.session_state.selected_gov == "الكل":
        view_lat = float(st_row["lat"]) if st.session_state.picked_station != "TA109" else 21.15
        view_lon = float(st_row["lon"]) if st.session_state.picked_station != "TA109" else 40.55
        view_zoom = 7.4 if st.session_state.picked_station != "TA109" else 6.7
    else:
        view_lat = float(st_row["lat"])
        view_lon = float(st_row["lon"])
        view_zoom = 7.6

    deck = pdk.Deck(
        layers=map_layers,
        initial_view_state=pdk.ViewState(
            latitude=view_lat,
            longitude=view_lon,
            zoom=view_zoom,
            pitch=0,
        ),
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={
            "html": "<b>{Station}</b> ({Governorate})<br/>الحوض: {Basin}<br/>نقطة حرجة: {Hotspot}<br/>{Alert_Level}<br/>القراءة: <b>{Reading_Str}</b> · بعد أقرب محطة: {Dist_Nearest_km} كم",
            "style": {"backgroundColor": "#091b33", "color": "#ffffff"}
        }
    )
    st.pydeck_chart(deck, use_container_width=True, height=500)

    if "AQI" in map_layer:
        sim_pct = min(max((avg_aqi / 220.0) * 100.0, 2.0), 100.0)
        bar_grad = "linear-gradient(90deg,#38bdf8 0%,#a3e635 30%,#facc15 55%,#fb923c 78%,#dc2626 100%)"
        scale_mid = f"متوسط جودة الهواء الحالي: {avg_aqi} AQI"
        leg_html = """
            <span style="color:#38bdf8;font-weight:700;">■ هواء جيد/مقبول</span>
            <span style="color:#facc15;font-weight:700;">■ متوسط/غبار خفيف</span>
            <span style="color:#fb923c;font-weight:700;">■ غير صحي للفئات الحساسة</span>
            <span style="color:#f87171;font-weight:700;">■ مرتفع / إنذار بيئي</span>
        """
    else:
        sim_pct = min(max((rain_add / 180.0) * 100.0, 2.0), 100.0)
        bar_grad = "linear-gradient(90deg,#bae6fd 0%,#38bdf8 30%,#1d4ed8 60%,#fb923c 82%,#ef4444 100%)"
        scale_mid = f"محاكاة الهطول: +{rain_add} مم ({pct_boost:+d}% · {storm_hours} س)"
        leg_html = """
            <span style="color:#7dd3fc;font-weight:700;">■ أزرق فاتح/متوسط: هطول منخفض إلى متوسط</span>
            <span style="color:#3b82f6;font-weight:700;">■ أزرق داكن: مرتفعات وهطول أعلى</span>
            <span style="color:#fb923c;font-weight:700;">■ برتقالي: حيطة وحذر</span>
            <span style="color:#f87171;font-weight:700;">■ أحمر: إنذار سيول شديد</span>
        """

    st.markdown(f"""
        <div class="legend-strip">{leg_html}</div>
        <div style="margin-top:8px;">
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#94b2d6;margin-bottom:4px;">
                <span>منخفض</span>
                <span>{scale_mid}</span>
                <span>مرتفع</span>
            </div>
            <div style="position:relative;height:7px;border-radius:999px;background:{bar_grad};">
                <div style="position:absolute;top:-3px;left:calc({sim_pct:.1f}% - 6px);width:13px;height:13px;border-radius:50%;background:#ffffff;border:2px solid #06101e;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with m_side:
    st.markdown('<div class="card-box"><div class="card-title">مؤشر الخطورة والقابلية</div>', unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_risk * 100, 1),
        number={"suffix": "%", "font": {"size": 24, "color": "#ffffff"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94b2d6"},
            "bar": {"color": "#38bdf8"},
            "bgcolor": "#081426",
            "steps": [
                {"range": [0, 35], "color": "#0f294a"},
                {"range": [35, 65], "color": "#2b2514"},
                {"range": [65, 100], "color": "#3b1720"}
            ],
            "threshold": {"line": {"color": "#f87171", "width": 3}, "value": 75}
        }
    ))
    gauge.update_layout(
        height=215,
        margin=dict(l=10, r=10, t=15, b=5),
        paper_bgcolor="#0c1c34",
        font={"color": "#e6eef8"}
    )
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown(f'<div class="card-sub" style="text-align:center;">الفارق عن المرجع: {diff_risk*100:+.1f}% · {source_tag}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    has_coastal = any(g in coastal_govs for g in filtered["Governorate"])
    marine_txt = "موج 1.8 م · تيارات ساحلية (جدة/الليث/القنفذة)" if has_coastal else "متابعة الأودية والجريان السطحي"
    conf_note = "أبعد من 50 كم عن أقرب محطة (ثقة منخفضة)" if bool(top_st["Extrapolated_Low_Conf"]) else "ضمن نطاق تغطية المحطات المباشر"
    st.markdown(f"""
        <div class="dark-side-card">
            <div style="font-size:11px;color:#7dd3fc;font-weight:700;">التنبيه اللحظي ونقطة التقاطع الحرجة</div>
            <div style="font-size:16px;font-weight:700;margin-top:5px;">{top_st["Alert_Level"]}</div>
            <div class="alert-banner">
                <div style="font-size:12px;font-weight:700;color:#ffffff;">{top_st["Station"]} ({top_st["Governorate"]})</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:4px;"><b>الحوض:</b> {top_st["Basin"]}</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:2px;"><b>نقطة حرجة:</b> {top_st["Hotspot"]}</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:2px;"><b>وصول السيل:</b> {top_st["Arrival_Hours"]} س · <b>تشبع التربة:</b> {top_st["Eff_Soil_Sat_Pct"]:.0f}%</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:4px;">{top_st["Advice"]}</div>
            </div>
            <div style="font-size:11px;color:#cbd5e1;line-height:1.6;">
                • <b>البحري والأودية:</b> {marine_txt}<br/>
                • <b>نطاق الثقة:</b> {conf_note} ({top_st["Dist_Nearest_km"]:.0f} كم)
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6) منحنى التوقعات الزمنية ونطاق عدم اليقين + مصفوفة القطاعات
b_left, b_right = st.columns([2.9, 1.3])

with b_left:
    st.markdown(
        f'<div class="card-box"><div class="card-title">التوقعات الزمنية ونطاق عدم اليقين (Random Forest vs AHP) · {st_row["Station"]} — {st_row["Basin"]}</div>',
        unsafe_allow_html=True
    )
    if "Nowcasting" in horizon_mode:
        x_lbl = [f"+{i*2}h" for i in range(13)]
    elif "14 Days" in horizon_mode:
        x_lbl = [f"يوم {i+1}" for i in range(14)]
    else:
        x_lbl = ["موسم 1 (الربيع)", "موسم 2 (الصيف)", "موسم 3 (الخريف)", "موسم 4 (الشتاء)", "موسم 5", "موسم 6"]

    n_pt = len(x_lbl)
    base_rf = float(st_row["Rain_RF"])
    base_ahp = float(st_row["Rain_AHP"])

    y_rf = np.round(base_rf * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_pt)) + np.linspace(0, 0.25, n_pt)), 1)
    y_ahp = np.round(base_ahp * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_pt)) + np.linspace(0, 0.22, n_pt)), 1)
    ext_pen = 0.08 if bool(st_row["Extrapolated_Low_Conf"]) else 0.0
    margin_err = np.round(np.maximum(4.0, y_rf * (0.08 + ext_pen + np.linspace(0.02, 0.12, n_pt))), 1)
    y_upper = np.round(y_rf + margin_err, 1)
    y_lower = np.round(np.maximum(0.0, y_rf - margin_err), 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_lbl + x_lbl[::-1],
        y=list(y_upper) + list(y_lower)[::-1],
        fill="toself",
        fillcolor="rgba(125, 211, 252, 0.14)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="نطاق عدم اليقين (Uncertainty Band)"
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=y_rf, mode="lines+markers",
        name="Random Forest (mm)", line=dict(color="#38bdf8", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=y_ahp, mode="lines+markers",
        name="AHP Model (mm)", line=dict(color="#5eead4", width=2, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=[165.0]*n_pt, mode="lines",
        name="عتبة السيول العالية (165 mm)", line=dict(color="#f87171", width=2, dash="dash")
    ))
    fig.update_layout(
        height=235,
        margin=dict(l=15, r=15, t=15, b=15),
        paper_bgcolor="#0c1c34",
        plot_bgcolor="#081426",
        font={"color": "#cbd5e1"},
        xaxis=dict(gridcolor="#162c4d"),
        yaxis=dict(gridcolor="#162c4d")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        f'<div class="card-sub">قراءات المحطة المفحوصة: <b>{st_row["Station"]}</b> | الهطول: <b>{st_row["Forecast_Rain"]:.1f} mm</b> | المرجع السنوي (1964–2014): <b>{st_row["Hist_Mean_Rain"]:.1f} mm</b> | الجريان: <b>{st_row["Runoff_m3s"]:.1f} m³/s</b> | AQI: <b>{int(st_row["Eff_AQI"])}</b></div>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with b_right:
    if "أحمر" in top_st["Alert_Level"]:
        act_water = "تفعيل غرفة الطوارئ وتصريف السدود عند الحد الآمن."
        act_road = "إغلاق المعابر المنخفضة وبطون الأودية فوراً."
        act_agri = "إيقاف العمليات الميدانية وحماية الثروة الحيوانية."
    elif "برتقالي" in top_st["Alert_Level"]:
        act_water = "رفع جاهزية فرق الصيانة ومراقبة مناسيب الأودية."
        act_road = "إصدار تنبيهات سرعة ومراقبة الطرق الجبلية والساحلية."
        act_agri = "تأجيل الرحلات الميدانية وتأمين المعدات الزراعية."
    else:
        act_water = "متابعة دورية لمحطات الرصد وتصريف المجاري."
        act_road = "رصد اعتيادي لحركة المرور والرؤية الأفقية."
        act_agri = "جدولة الري والطاقة وفق الظروف المناخية الحالية."

    st.markdown(f"""
        <div class="card-box">
            <div class="card-title">مصفوفة الإجراءات ({top_st["Alert_Level"]})</div>
            <div class="sector-row">
                <b>السيول والمياه ({avg_runoff:.1f} m³/s):</b> {act_water}
            </div>
            <div class="sector-row">
                <b>الطرق والملاحة ({filtered["Eff_Wind_kmh"].mean():.0f} km/h):</b> {act_road}
            </div>
            <div class="sector-row">
                <b>الزراعة والبيئة (AQI {avg_aqi}):</b> {act_agri}
            </div>
        </div>
    """, unsafe_allow_html=True)

exec_summary = (
    f"RASD | منطقة مكة المكرمة ({st.session_state.selected_gov}) | المحطة: {st_row['Station']} | الإنذار: {top_st['Alert_Level']} | "
    f"الذروة: {max_rain:.1f} mm ({diff_rain:+.1f} عن المرجع) | الجريان: {avg_runoff:.1f} m³/s | "
    f"وصول السيل: ~{avg_arrival:.1f} س | AQI: {avg_aqi} | الإجراء: {act_road}"
)

st.markdown('<div class="card-box"><div class="card-title">ملخص تنفيذي وتصدير سريع لبيانات منطقة الدراسة</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-box">{exec_summary}</div>', unsafe_allow_html=True)

cols_out = [
    "Station", "Governorate", "Basin", "Hotspot", "Hist_Mean_Rain",
    "Elevation_m", "Dist_Nearest_km", "Rain_AHP", "Rain_RF",
    "Runoff_m3s", "Arrival_Hours", "Eff_AQI", "Susceptibility_Idx", "Alert_Level"
]
st.dataframe(filtered[cols_out], use_container_width=True)

ex1, ex2 = st.columns(2)
ex1.download_button(
    label="تحميل بيانات السيناريو والمحطات (CSV)",
    data=filtered[cols_out].to_csv(index=False).encode("utf-8-sig"),
    file_name="RASD_Makkah_Province_Scenario.csv",
    mime="text/csv"
)

excel_rows = "".join(
    "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
    for row in filtered[cols_out].values
)
excel_headers = "".join(f"<th>{h}</th>" for h in cols_out)
excel_html = f"<html><head><meta charset='utf-8'></head><body><table border='1'><tr>{excel_headers}</tr>{excel_rows}</table></body></html>"
ex2.download_button(
    label="تحميل التقرير بصيغة Excel (.xls)",
    data=excel_html.encode("utf-8-sig"),
    file_name="RASD_Makkah_Province_Scenario.xls",
    mime="application/vnd.ms-excel"
)
st.markdown("</div>", unsafe_allow_html=True)
