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
    /* أزرار السيناريوهات بنص أبيض واضح */
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton > button * {
        background-color: #071b33 !important;
        color: #ffffff !important;
        border: 1px solid #0284c7 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stButton > button:hover * {
        background-color: #0f3561 !important;
        color: #7dd3fc !important;
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
    /* شريط الحالة المباشرة في الأعلى */
    .live-strip {
        background: linear-gradient(90deg, rgba(14, 116, 144, 0.24) 0%, rgba(12, 28, 52, 0.95) 100%);
        border: 1px solid #254b7a;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 12px;
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
    /* الصف العلوي: 4 كروت أرقام */
    .top-kpi {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 10px;
        padding: 13px 16px;
        box-shadow: 0 3px 10px rgba(2, 8, 20, 0.3);
        min-height: 112px;
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
        background: rgba(14, 116, 144, 0.18);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# بيانات 26 محطة MEWA لمكة المكرمة والباحة (1964–2014) مع أبعاد جيولوجية وهيدرولوجية
np.random.seed(26)
n_stations = 26
gov_pool = ["مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة", "الباحة", "المخواة"]
lat_pool = [21.4225, 21.5433, 21.2703, 20.1500, 20.1289, 20.0129, 19.9333]
lon_pool = [39.8262, 39.1728, 40.4158, 40.2667, 41.0789, 41.4677, 41.3000]
basin_pool = ["وادي فاطمة / مكة", "وادي السيل الكبير / الطائف", "وادي الليث", "وادي قنونا / القنفذة", "أودية سراة الباحة", "أودية تهامة المخواة"]
soil_perm_pool = [0.25, 0.35, 0.45, 0.60, 0.75]

coastal_govs = {"جدة", "الليث", "القنفذة"}
idx_choice = np.random.choice(len(gov_pool), n_stations)

df = pd.DataFrame({
    "Station": [f"MEWA-{i+1:02d}" for i in range(n_stations)],
    "Governorate": [gov_pool[i] for i in idx_choice],
    "Basin": [basin_pool[i % len(basin_pool)] for i in idx_choice],
    "lat": [lat_pool[i] + np.random.uniform(-0.18, 0.18) for i in idx_choice],
    "lon": [lon_pool[i] + np.random.uniform(-0.18, 0.18) for i in idx_choice],
    "Hist_Mean_Rain": np.random.uniform(18.0, 68.0, n_stations),
    "Elevation_m": np.random.uniform(12.0, 2150.0, n_stations),
    "Soil_Saturation_Pct": np.random.uniform(25.0, 92.0, n_stations),
    "Low_Perm_Factor": np.random.choice(soil_perm_pool, n_stations),
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
show_drainage = st.sidebar.checkbox("إظهار مسارات الأودية والأحواض", value=True)

st.sidebar.markdown("**سيناريوهات مطرية جاهزة:**")
b1, b2 = st.sidebar.columns(2)
if b1.button("وضع طبيعي", key="btn_normal"):
    st.session_state.rain_sim_val = 0
if b2.button("هطول متوسط", key="btn_mod"):
    st.session_state.rain_sim_val = 40
b3, b4 = st.sidebar.columns(2)
if b3.button("عاصفة غزيرة", key="btn_heavy"):
    st.session_state.rain_sim_val = 95
if b4.button("سيناريو حرج", key="btn_crit"):
    st.session_state.rain_sim_val = 155

rain_add = st.sidebar.slider(
    "محاكاة زيادة الهطول (مم)",
    min_value=0,
    max_value=180,
    value=st.session_state.rain_sim_val,
    step=5
)
st.session_state.rain_sim_val = rain_add

st.sidebar.markdown("**محاكاة What-If المخصصة:**")
pct_boost = st.sidebar.slider("نسبة زيادة الهطول (%)", min_value=-20, max_value=100, value=15, step=5)
storm_hours = st.sidebar.slider("مدة العاصفة / الهطول (ساعات)", min_value=2, max_value=24, value=6, step=2)

geojson_file = st.sidebar.file_uploader(
    "رفع حدود المحافظات / الأحواض (GeoJSON)",
    type=["geojson", "json"]
)

# الحسابات الهيدرولوجية والجيولوجية ومقارنة النماذج
filtered = (df if selected_gov == "الكل" else df[df["Governorate"] == selected_gov]).copy()

horizon_mult = 1.0 if "Nowcasting" in horizon_mode else (1.15 if "14 Days" in horizon_mode else 1.25)
duration_factor = 0.75 + (storm_hours / 12.0) * 0.45
pct_factor = 1.0 + (pct_boost / 100.0)

filtered["Rain_RF"] = np.round(
    (filtered["Hist_Mean_Rain"] * pct_factor + (rain_add * 1.25)) * horizon_mult * duration_factor,
    1
)
filtered["Rain_AHP"] = np.round(
    (filtered["Hist_Mean_Rain"] * pct_factor + (rain_add * 0.92)) * horizon_mult * duration_factor,
    1
)
filtered["Forecast_Rain"] = filtered["Rain_RF"] if model_mode == "Random Forest" else filtered["Rain_AHP"]

filtered["Eff_Soil_Sat_Pct"] = np.clip(
    filtered["Soil_Saturation_Pct"] + (filtered["Forecast_Rain"] * 0.14),
    15.0,
    100.0
)
runoff_coeff = np.clip(
    0.22 + (filtered["Eff_Soil_Sat_Pct"] / 100.0) * 0.35 + filtered["Low_Perm_Factor"] * 0.32,
    0.25,
    0.92
)
filtered["Runoff_m3s"] = np.round(
    filtered["Forecast_Rain"] * runoff_coeff * (1.2 + filtered["Elevation_m"] / 1600.0),
    1
)
filtered["Arrival_Hours"] = np.round(
    np.clip(6.5 - (filtered["Forecast_Rain"] / 55.0) + (filtered["Elevation_m"] / 1400.0), 1.2, 8.5),
    1
)
filtered["Susceptibility_Idx"] = np.clip(
    (filtered["Forecast_Rain"] / 210.0) * 0.50
    + (filtered["Eff_Soil_Sat_Pct"] / 100.0) * 0.25
    + filtered["Low_Perm_Factor"] * 0.25,
    0.05,
    0.99
)
filtered["Dew_Point_C"] = np.round(filtered["Temp_C"] - ((100.0 - filtered["Humidity_Pct"]) / 5.0), 1)

def get_alert_and_metric(row):
    r = row["Forecast_Rain"]
    s = row["Susceptibility_Idx"]
    if r < 45 and s < 0.45:
        alert_lbl, txt_col = "أزرق · مستقر", [3, 105, 161, 255]
        adv = "حالة مستقرة؛ متابعة اعتيادية للأجواء ومجاري الأودية."
    elif r < 80 and s < 0.65:
        alert_lbl, txt_col = "أصفر · تنبيه مبكر", [161, 98, 7, 255]
        adv = "تنبيه مبكر؛ تشبع جزئي للتربة واحتمال جريان متوسط في الشعاب."
    elif r < 120 and s < 0.80:
        alert_lbl, txt_col = "برتقالي · حيطة وحذر", [194, 65, 12, 255]
        adv = "حيطة وحذر؛ جريان نشط محتمل وتجنب نقاط الاختناق والأودية."
    else:
        alert_lbl, txt_col = "أحمر · إنذار سيول شديد", [185, 28, 28, 255]
        adv = "إنذار سيول شديد؛ سرعة استجابة عالية وتجنب بطون الأودية فوراً."

    if "الرياح" in map_layer:
        w = float(row["Wind_kmh"])
        weight = min(w / 65.0, 1.0)
        reading_str = f"{w:.0f} km/h"
    elif "الحساسية" in map_layer:
        weight = min(float(s), 1.0)
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

source_tag = (
    f"تاريخي (1964–2014) · What-If ({pct_boost:+d}% / {storm_hours}h)"
    if rain_add == 0
    else f"+{rain_add} مم · What-If ({pct_boost:+d}% / {storm_hours}h)"
)

top_st = filtered.sort_values("Forecast_Rain", ascending=False).iloc[0]
avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_risk = filtered["Susceptibility_Idx"].mean()
avg_runoff = filtered["Runoff_m3s"].mean()
avg_soil = filtered["Eff_Soil_Sat_Pct"].mean()
avg_arrival = filtered["Arrival_Hours"].mean()
severe_cnt = int((filtered["Forecast_Rain"] >= 80).sum())

# 1) الشريط العلوي الرئيسي
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

# شريط الحالة الفورية في الأعلى (لإثراء المساحة العلوية بمعلومات عملية مباشرة)
st.markdown(f"""
    <div class="live-strip">
        <div>
            <span style="color:#7dd3fc;font-weight:700;">حالة الرصد المباشرة:</span>
            <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]}
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            <span class="live-pill">أعلى حوض: <b>{top_st["Basin"]}</b></span>
            <span class="live-pill">وصول الجريان: <b>~{avg_arrival:.1f} س</b></span>
            <span class="live-pill">تشبع التربة: <b>{avg_soil:.0f}%</b></span>
            <span class="live-pill">محطات نشطة: <b>{len(filtered)}</b></span>
        </div>
    </div>
""", unsafe_allow_html=True)

trend_rain_cls = "trend-up" if (rain_add > 25 or pct_boost > 10) else ("trend-down" if pct_boost < 0 else "trend-flat")
trend_rain_lbl = "↑ تصاعد" if trend_rain_cls == "trend-up" else ("↓ تراجع" if trend_rain_cls == "trend-down" else "→ مستقر")

trend_risk_cls = "trend-up" if avg_risk >= 0.55 else "trend-down"
trend_risk_lbl = "↑ مرتفع" if avg_risk >= 0.55 else "↓ معتدل"

# 2) الصف الأول: 4 كروت أرقام مع مؤشرات اتجاه التغير
c1, c2, c3, c4 = st.columns(4)
if audience_mode.startswith("للفرد"):
    status_txt = "إنذار أحمر/برتقالي" if severe_cnt >= 3 else ("تنبيه أصفر" if severe_cnt > 0 else "مستقر · أزرق")
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">حالة المنطقة والإنذار</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val" style="font-size:19px;color:#7dd3fc;">{status_txt}</div><div class="top-kpi-sub">{hazard_type} · وصول محتمل خلال {avg_arrival:.1f} س</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">متوسط الهطول المتوقع</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الذروة: {max_rain:.1f} mm خلال {storm_hours} س</div></div>""",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الحرارة والرطوبة</span><span class="trend-flat">→ متابع</span></div><div class="top-kpi-val">{filtered["Temp_C"].mean():.1f} <span class="top-kpi-unit">°C</span></div><div class="top-kpi-sub">رطوبة {filtered["Humidity_Pct"].mean():.0f}% · ندى {filtered["Dew_Point_C"].mean():.1f}°C</div></div>""",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">جودة الهواء (AQI)</span><span class="trend-down">↓ آمن نسبياً</span></div><div class="top-kpi-val">{int(filtered["AQI"].mean())} <span class="top-kpi-unit">AQI</span></div><div class="top-kpi-sub">UV: {int(filtered["UV_Index"].mean())} · غبار {filtered["Dust_ugm3"].mean():.0f} µg/m³</div></div>""",
        unsafe_allow_html=True
    )
else:
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الذروة المتوقعة ({model_mode})</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{max_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">RF: {filtered["Rain_RF"].mean():.1f} mm · AHP: {filtered["Rain_AHP"].mean():.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">مؤشر الحساسية (FSI)</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val">{avg_risk:.2f}</div><div class="top-kpi-sub">تشبع التربة: {avg_soil:.0f}% · نفاذية منخفضة {filtered["Low_Perm_Factor"].mean():.2f}</div></div>""",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الجريان السطحي للأودية</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_runoff:.1f} <span class="top-kpi-unit">m³/s</span></div><div class="top-kpi-sub">زمن وصول السيل: ~{avg_arrival:.1f} ساعة</div></div>""",
        unsafe_allow_html=True
    )
    c4.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الضغط والرياح والتحذيرات</span><span class="trend-flat">→ {severe_cnt}/{len(filtered)}</span></div><div class="top-kpi-val">{filtered["Pressure_hPa"].mean():.0f} <span class="top-kpi-unit">hPa</span></div><div class="top-kpi-sub">رياح {filtered["Wind_kmh"].mean():.0f} km/h · إنذار مرتفع: {severe_cnt}</div></div>""",
        unsafe_allow_html=True
    )

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# رسالة الجمهور المباشرة عند اختيار وضع الفرد/السكان
if audience_mode.startswith("للفرد"):
    st.markdown(f"""
        <div class="public-box">
            <div style="font-size:13px;font-weight:700;color:#7dd3fc;">ماذا يعني هذا لك الآن؟ ({top_st["Governorate"]})</div>
            <div style="font-size:12px;color:#f1f5f9;margin-top:4px;">
                مستوى الحالة الحالي: <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]} (الزمن التقديري لوصول الجريان في الأودية/المجاري: <b>{top_st["Arrival_Hours"]} ساعة</b>).
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3) الصف الأوسط: المؤشر الدائري + الخريطة الفاتحة اللونية + بطاقة الإنذار
m_left, m_center, m_right = st.columns([1.05, 2.05, 1.2])

with m_left:
    st.markdown('<div class="card-box"><div class="card-title">مؤشر الخطورة والقابلية</div>', unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_risk * 100, 1),
        number={"suffix": "%", "font": {"size": 25, "color": "#ffffff"}},
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
        height=255,
        margin=dict(l=12, r=12, t=20, b=10),
        paper_bgcolor="#0c1c34",
        font={"color": "#e6eef8"}
    )
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown(f'<div class="card-sub" style="text-align:center;">المصدر: {source_tag}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with m_center:
    st.markdown(f'<div class="card-box"><div class="card-title">خريطة تفاعلية فاتحة بالقراءات اللونية · {map_layer}</div>', unsafe_allow_html=True)

    color_range = [
        [56, 189, 248],
        [125, 211, 252],
        [250, 204, 21],
        [251, 146, 60],
        [239, 68, 68]
    ]

    map_layers = [
        pdk.Layer(
            "HeatmapLayer",
            data=filtered,
            get_position=["lon", "lat"],
            get_weight="Heat_Weight",
            radius_pixels=65,
            intensity=1.2,
            threshold=0.05,
            color_range=color_range,
        ),
        pdk.Layer(
            "TextLayer",
            data=filtered,
            get_position=["lon", "lat"],
            get_text="Map_Label",
            get_color="Txt_Color",
            get_size=13,
            get_alignment_baseline="'bottom'",
            background=True,
            get_background_color=[255, 255, 255, 225],
            background_padding=[3, 6],
            pickable=True,
        )
    ]

    if show_drainage and len(filtered) > 0:
        drainage_paths = [
            {
                "basin": r_row["Basin"],
                "arrival": f"{r_row['Arrival_Hours']} س",
                "path": [[float(r_row["lon"]), float(r_row["lat"])], [float(r_row["lon"]) - 0.18, float(r_row["lat"]) - 0.14]]
            }
            for _, r_row in filtered.iterrows()
        ]
        map_layers.append(pdk.Layer(
            "PathLayer",
            data=drainage_paths,
            get_path="path",
            get_color=[2, 132, 199, 215],
            width_min_pixels=2.5,
            pickable=True,
        ))

    if geojson_file is not None:
        try:
            gj_obj = json.load(geojson_file)
            map_layers.insert(0, pdk.Layer(
                "GeoJsonLayer",
                data=gj_obj,
                stroked=True,
                filled=True,
                get_fill_color=[2, 132, 199, 25],
                get_line_color=[3, 105, 161, 190],
                line_width_min_pixels=1.8,
            ))
        except Exception:
            st.warning("تعذر قراءة ملف GeoJSON المرفوع.")

    deck = pdk.Deck(
        layers=map_layers,
        initial_view_state=pdk.ViewState(
            latitude=float(filtered["lat"].mean()),
            longitude=float(filtered["lon"].mean()),
            zoom=6.8,
            pitch=0,
        ),
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={
            "html": "<b>{Station}</b> ({Governorate})<br/>الحوض: {Basin}<br/>{Alert_Level}<br/>القراءة: <b>{Reading_Str}</b> · وصول السيل: {Arrival_Hours} س",
            "style": {"backgroundColor": "#091b33", "color": "#ffffff"}
        }
    )
    st.pydeck_chart(deck, use_container_width=True)

    sim_pct = min(max((rain_add / 180.0) * 100.0, 2.0), 100.0)
    st.markdown(f"""
        <div class="legend-strip">
            <span style="color:#38bdf8;font-weight:700;">■ أزرق: مستقر</span>
            <span style="color:#facc15;font-weight:700;">■ أصفر: تنبيه</span>
            <span style="color:#fb923c;font-weight:700;">■ برتقالي: حيطة وحذر</span>
            <span style="color:#f87171;font-weight:700;">■ أحمر: إنذار سيول</span>
        </div>
        <div style="margin-top:8px;">
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#94b2d6;margin-bottom:4px;">
                <span>منخفض (مستقر)</span>
                <span>محاكاة الهطول: +{rain_add} مم ({pct_boost:+d}% · {storm_hours} س)</span>
                <span>مرتفع (إنذار سيول)</span>
            </div>
            <div style="position:relative;height:7px;border-radius:999px;background:linear-gradient(90deg,#38bdf8 0%,#facc15 45%,#fb923c 72%,#ef4444 100%);">
                <div style="position:absolute;top:-3px;left:calc({sim_pct:.1f}% - 6px);width:13px;height:13px;border-radius:50%;background:#ffffff;border:2px solid #06101e;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with m_right:
    has_coastal = any(g in coastal_govs for g in filtered["Governorate"])
    marine_txt = "موج 1.8 م · تيارات ساحلية (جدة/الليث/القنفذة)" if has_coastal else "متابعة الأودية والجريان السطحي"
    st.markdown(f"""
        <div class="dark-side-card">
            <div style="font-size:11px;color:#7dd3fc;font-weight:700;">التنبيه اللحظي وحالة الرصد</div>
            <div style="font-size:16px;font-weight:700;margin-top:5px;">{top_st["Alert_Level"]}</div>
            <div class="alert-banner">
                <div style="font-size:12px;font-weight:700;color:#ffffff;">أعلى محطة: {top_st["Station"]} ({top_st["Governorate"]})</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:4px;">الحوض: {top_st["Basin"]} · وصول السيل: {top_st["Arrival_Hours"]} س</div>
                <div style="font-size:11px;color:#cbd5e1;margin-top:4px;">{top_st["Advice"]}</div>
            </div>
            <div style="font-size:11px;color:#cbd5e1;line-height:1.6;">
                • <b>البحري والأودية:</b> {marine_txt}<br/>
                • <b>تشبع التربة:</b> {top_st["Eff_Soil_Sat_Pct"]:.0f}% · <b>الفلك:</b> الشروق 06:34 · الغروب 17:42
            </div>
        </div>
    """, unsafe_allow_html=True)

# 4) الصف السفلي: منحنى التوقعات الزمنية بنطاق عدم اليقين + القطاعات والإجراءات التشغيلية
b_left, b_right = st.columns([2.9, 1.3])

station_list = filtered["Station"].tolist()
picked_station = st.selectbox("اختر محطة لعرض منحناها وتفاصيلها الهيدرولوجية مباشرة:", station_list)
st_row = filtered[filtered["Station"] == picked_station].iloc[0]

with b_left:
    st.markdown(
        f'<div class="card-box"><div class="card-title">التوقعات الزمنية ونطاق عدم اليقين (Random Forest vs AHP) · {picked_station} ({st_row["Governorate"]})</div>',
        unsafe_allow_html=True
    )
    if "Nowcasting" in horizon_mode:
        x_lbl = [f"+{i*2}h" for i in range(13)]
    elif "14 Days" in horizon_mode:
        x_lbl = [f"يوم {i+1}" for i in range(14)]
    else:
        x_lbl = ["الشهر 1", "الشهر 2", "الشهر 3", "الشهر 4", "الشهر 5", "الشهر 6"]

    n_pt = len(x_lbl)
    base_rf = float(st_row["Rain_RF"])
    base_ahp = float(st_row["Rain_AHP"])

    y_rf = np.round(base_rf * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_pt)) + np.linspace(0, 0.25, n_pt)), 1)
    y_ahp = np.round(base_ahp * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_pt)) + np.linspace(0, 0.22, n_pt)), 1)
    margin_err = np.round(np.maximum(3.5, y_rf * (0.08 + np.linspace(0.02, 0.12, n_pt))), 1)
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
        name="نطاق عدم اليقين (Confidence Band)"
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
        x=x_lbl, y=[110.0]*n_pt, mode="lines",
        name="عتبة السيول (110 mm)", line=dict(color="#f87171", width=2, dash="dash")
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
            <div class="card-title">مصفوفة الإجراءات والقطاعات</div>
            <div class="sector-row">
                <b>السيول والمياه ({avg_runoff:.1f} m³/s):</b> {act_water}
            </div>
            <div class="sector-row">
                <b>الطرق والملاحة ({filtered["Wind_kmh"].mean():.0f} km/h):</b> {act_road}
            </div>
            <div class="sector-row">
                <b>الزراعة والطاقة ({filtered["Temp_C"].mean():.1f}°C):</b> {act_agri}
            </div>
        </div>
    """, unsafe_allow_html=True)

exec_summary = (
    f"تنبيه RASD ({selected_gov}) | المستوى: {top_st['Alert_Level']} | "
    f"الذروة: {max_rain:.1f} mm ({model_mode}) | الجريان: {avg_runoff:.1f} m³/s | "
    f"وصول السيل: ~{avg_arrival:.1f} س | الإجراء الفوري: {act_road}"
)
with st.expander("ملخص تنفيذي وإشعار جاهز للمشاركة"):
    st.code(exec_summary, language="text")

with st.expander("عرض جدول المحطات الـ 26 وتصدير تقرير CSV"):
    cols = [
        "Station", "Governorate", "Basin", "Elevation_m", "Eff_Soil_Sat_Pct",
        "Rain_AHP", "Rain_RF", "Runoff_m3s", "Arrival_Hours", "Susceptibility_Idx", "Alert_Level"
    ]
    st.dataframe(filtered[cols], use_container_width=True)
    st.download_button(
        label="تحميل تقرير المحطات المفلترة (CSV)",
        data=filtered[cols].to_csv(index=False).encode("utf-8-sig"),
        file_name="RASD_Flood_Early_Warning.csv",
        mime="text/csv"
    )
