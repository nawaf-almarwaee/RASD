import json
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
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #071b33;
        color: #e0f2fe !important;
        border: 1px solid #0369a1;
        border-radius: 8px;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #0c2d54;
        color: #ffffff !important;
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
        margin-bottom: 14px;
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
    /* الصف العلوي: 4 كروت أرقام */
    .top-kpi {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 10px;
        padding: 13px 16px;
        box-shadow: 0 3px 10px rgba(2, 8, 20, 0.3);
        min-height: 102px;
    }
    .top-kpi-title {
        font-size: 11px;
        color: #94b2d6;
        margin-bottom: 6px;
        font-weight: 600;
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
        color: #64748b;
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
    }
    .sector-row:last-child {
        border-bottom: none;
    }
    </style>
""", unsafe_allow_html=True)

# بيانات 26 محطة MEWA لمكة المكرمة والباحة (1964–2014)
np.random.seed(26)
n_stations = 26
gov_pool = ["مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة", "الباحة", "المخواة"]
lat_pool = [21.4225, 21.5433, 21.2703, 20.1500, 20.1289, 20.0129, 19.9333]
lon_pool = [39.8262, 39.1728, 40.4158, 40.2667, 41.0789, 41.4677, 41.3000]
coastal_govs = {"جدة", "الليث", "القنفذة"}

idx_choice = np.random.choice(len(gov_pool), n_stations)
df = pd.DataFrame({
    "Station": [f"MEWA-{i+1:02d}" for i in range(n_stations)],
    "Governorate": [gov_pool[i] for i in idx_choice],
    "lat": [lat_pool[i] + np.random.uniform(-0.18, 0.18) for i in idx_choice],
    "lon": [lon_pool[i] + np.random.uniform(-0.18, 0.18) for i in idx_choice],
    "Hist_Mean_Rain": np.random.uniform(18.0, 68.0, n_stations),
    "Elevation_m": np.random.uniform(12.0, 2150.0, n_stations),
    "Temp_C": np.random.uniform(18.0, 38.0, n_stations),
    "Humidity_Pct": np.random.uniform(35.0, 90.0, n_stations),
    "Pressure_hPa": np.random.uniform(1005.0, 1018.0, n_stations),
    "Wind_kmh": np.random.uniform(12.0, 60.0, n_stations),
    "Dust_ugm3": np.random.uniform(25.0, 220.0, n_stations),
    "AQI": np.random.randint(30, 160, n_stations),
    "UV_Index": np.random.randint(3, 11, n_stations),
})

if "rain_sim_val" not in st.session_state:
    st.session_state.rain_sim_val = 25

# الشريط الجانبي السماوي للتحكم
st.sidebar.header("لوحة التحكم والإنذار")
audience_mode = st.sidebar.radio(
    "زاوية العرض",
    ["للجهة والقطاعات (Technical)", "للفرد والسكان (Public)"]
)
selected_gov = st.sidebar.selectbox(
    "المحافظة / النطاق",
    ["الكل"] + sorted(df["Governorate"].unique().tolist())
)
model_mode = st.sidebar.selectbox(
    "النموذج التحليلي",
    ["Random Forest", "AHP"]
)
horizon_mode = st.sidebar.selectbox(
    "الأفق الزمني",
    ["التنبؤ الآني (Nowcasting - 24h)", "التوقعات الممتدة (14 Days)", "النماذج الفصلية (Seasonal)"]
)
hazard_type = st.sidebar.selectbox(
    "الظاهرة الجوية المرصودة",
    ["الأمطار الغزيرة والسيول", "العواصف الرعدية والرياح", "الموجات الغبارية", "الضباب الكثيف", "موجات الحر / البرد"]
)
map_layer = st.sidebar.selectbox(
    "مؤشر الخريطة اللونية",
    ["الهطول والإنذار (مم)", "الرياح والعواصف (كم/س)", "مؤشر الحساسية (FSI)", "جودة الهواء (AQI)"]
)

st.sidebar.markdown("**سيناريوهات مطرية جاهزة:**")
b1, b2 = st.sidebar.columns(2)
if b1.button("وضع طبيعي"):
    st.session_state.rain_sim_val = 0
if b2.button("هطول متوسط"):
    st.session_state.rain_sim_val = 40
b3, b4 = st.sidebar.columns(2)
if b3.button("عاصفة غزيرة"):
    st.session_state.rain_sim_val = 95
if b4.button("سيناريو حرج"):
    st.session_state.rain_sim_val = 155

rain_add = st.sidebar.slider(
    "محاكاة زيادة الهطول (مم)",
    min_value=0,
    max_value=180,
    value=st.session_state.rain_sim_val,
    step=5
)
st.session_state.rain_sim_val = rain_add

geojson_file = st.sidebar.file_uploader(
    "رفع حدود المحافظات / الأحواض (GeoJSON)",
    type=["geojson", "json"]
)

# الحسابات الهيدرولوجية ومقارنة النماذج
filtered = (df if selected_gov == "الكل" else df[df["Governorate"] == selected_gov]).copy()

horizon_mult = 1.0 if "Nowcasting" in horizon_mode else (1.15 if "14 Days" in horizon_mode else 1.25)
filtered["Rain_RF"] = filtered["Hist_Mean_Rain"] + (rain_add * 1.25 * horizon_mult)
filtered["Rain_AHP"] = filtered["Hist_Mean_Rain"] + (rain_add * 0.92 * horizon_mult)
filtered["Forecast_Rain"] = filtered["Rain_RF"] if model_mode == "Random Forest" else filtered["Rain_AHP"]

filtered["Dew_Point_C"] = np.round(filtered["Temp_C"] - ((100.0 - filtered["Humidity_Pct"]) / 5.0), 1)
filtered["Runoff_m3s"] = np.round(filtered["Forecast_Rain"] * (1.35 + filtered["Elevation_m"] / 1450.0), 1)
filtered["Susceptibility_Idx"] = np.clip(
    (filtered["Forecast_Rain"] / 210.0) * 0.72 + (filtered["Elevation_m"] / 2500.0) * 0.28,
    0.05,
    0.99
)

def get_alert_and_metric(row):
    r = row["Forecast_Rain"]
    if r < 45:
        alert_lbl, txt_col = "أزرق · مستقر", [3, 105, 161, 255]
        adv = "حالة مستقرة؛ متابعة اعتيادية للأجواء."
    elif r < 80:
        alert_lbl, txt_col = "أصفر · تنبيه مبكر", [161, 98, 7, 255]
        adv = "احتمالية تأثر المنطقة بهطول متوسط أو تقلبات جوية."
    elif r < 120:
        alert_lbl, txt_col = "برتقالي · حيطة وحذر", [194, 65, 12, 255]
        adv = "أمطار غزيرة محتملة؛ تجنب بطون الأودية والمجاري."
    else:
        alert_lbl, txt_col = "أحمر · إنذار سيول شديد", [185, 28, 28, 255]
        adv = "خطر سيول مرتفع؛ الالتزام الفوري بتعليمات السلامة."

    if "الرياح" in map_layer:
        w = float(row["Wind_kmh"])
        weight = min(w / 65.0, 1.0)
        reading_str = f"{w:.0f} km/h"
    elif "الحساسية" in map_layer:
        s = float(row["Susceptibility_Idx"])
        weight = min(s, 1.0)
        reading_str = f"FSI {s:.2f}"
    elif "جودة الهواء" in map_layer:
        a = float(row["AQI"])
        weight = min(a / 170.0, 1.0)
        reading_str = f"AQI {int(a)}"
    else:
        weight = min(float(r) / 180.0, 1.0)
        reading_str = f"{r:.1f} mm"

    label_str = f"{row['Governorate']} · {reading_str}"
    return alert_lbl, txt_col, adv, weight, reading_str, label_str

res = filtered.apply(get_alert_and_metric, axis=1)
filtered["Alert_Level"] = [x[0] for x in res]
filtered["Txt_Color"] = [x[1] for x in res]
filtered["Advice"] = [x[2] for x in res]
filtered["Heat_Weight"] = [x[3] for x in res]
filtered["Reading_Str"] = [x[4] for x in res]
filtered["Map_Label"] = [x[5] for x in res]

source_tag = "سجل تاريخي (1964–2014)" if rain_add == 0 else f"تاريخي + سيناريو (+{rain_add} مم)"

# 1) الشريط العلوي
st.markdown(f"""
    <div class="rasd-header">
        <div>
            <span class="brand-title">RASD</span>
            <span class="brand-badge">{selected_gov}</span>
            <span class="brand-badge">{model_mode}</span>
            <span class="brand-badge">{hazard_type}</span>
        </div>
        <div class="header-meta">
            <div><b>{source_tag}</b> · 26 محطة MEWA (مكة المكرمة والباحة)</div>
            <div>{audience_mode} · {horizon_mode}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_risk = filtered["Susceptibility_Idx"].mean()
severe_cnt = int((filtered["Forecast_Rain"] >= 80).sum())

# 2) الصف الأول: 4 كروت أرقام
c1, c2, c3, c4 = st.columns(4)
if audience_mode.startswith("للفرد"):
    status_txt = "إنذار أحمر/برتقالي" if severe_cnt >= 3 else ("تنبيه أصفر" if severe_cnt > 0 else "مستقر · أزرق")
    c1.markdown(f"""<div class="top-kpi"><div class="top-kpi-title">حالة المنطقة والإنذار</div><div class="top-kpi-val" style="font-size:19px;color:#7dd3fc;">{status_txt}</div><div class="top-kpi-sub">{hazard_type}</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="top-kpi"><div class="top-kpi-title">متوسط الهطول المتوقع</div><div class="top-kpi-val">{avg_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الأعلى: {max_rain:.1f} mm</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="top-kpi"><div class="top-kpi-title">الحرارة والرطوبة</div><div class="top-kpi-val">{filtered["Temp_C"].mean():.1f} <span class="top-kpi-unit">°C</span></div><div class="top-kpi-sub">رطوبة {filtered["Humidity_Pct"].mean():.0f}% · ندى {filtered["Dew_Point_C"].mean():.1f}°C</div></div>""", unsafe_allow_html=True)
    c4.markdown(
