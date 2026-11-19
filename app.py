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
    /* أزرار الشريط الجانبي والصفحة */
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
    .bar-label {
        font-size: 11px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 4px;
    }
    /* الصف العلوي: 4 كروت أرقام */
    .top-kpi {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 10px;
        padding: 13px 16px;
        box-shadow: 0 3px 10px rgba(2, 8, 20, 0.3);
        min-height: 118px;
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

# بيانات 26 محطة MEWA لمكة المكرمة والباحة (1964–2014) مع أبعاد جيولوجية وهيدرولوجية
np.random.seed(26)
n_stations = 26
gov_pool = ["مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة", "الباحة", "المخواة"]
lat_pool = [21.4225, 21.5433, 21.2703, 20.1500, 20.1289, 20.0129, 19.9333]
lon_pool = [39.8262, 39.1728, 40.4158, 40.2667, 41.0789, 41.4677, 41.3000]
basin_pool = [
    "وادي فاطمة / مكة",
    "وادي السيل الكبير / الطائف",
    "وادي الليث",
    "وادي قنونا / القنفذة",
    "أودية سراة الباحة",
    "أودية تهامة المخواة"
]
hotspot_pool = [
    "تقاطع وادي فاطمة مع طريق الحرمين",
    "مجرى السيل الكبير ومخرج الطائف",
    "نقطة اختناق وادي الليث السفلية",
    "معبر وادي قنونا الشرقي",
    "منحدرات عقبة الباحة وتجمع الشعاب",
    "مصب أودية تهامة بالمخواة"
]
soil_perm_pool = [0.25, 0.35, 0.45, 0.60, 0.75]
coastal_govs = {"جدة", "الليث", "القنفذة"}

idx_choice = np.random.choice(len(gov_pool), n_stations)

df = pd.DataFrame({
    "Station": [f"MEWA-{i+1:02d}" for i in range(n_stations)],
    "Governorate": [gov_pool[i] for i in idx_choice],
    "Basin": [basin_pool[i % len(basin_pool)] for i in idx_choice],
    "Hotspot": [hotspot_pool[i % len(hotspot_pool)] for i in idx_choice],
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

defaults = {
    "audience_mode": "للجهة والقطاعات (Technical)",
    "selected_gov": "الكل",
    "model_mode": "Random Forest",
    "horizon_mode": "التنبؤ الآني (Nowcasting - 24h)",
    "hazard_type": "الأمطار الغزيرة والسيول",
    "map_layer": "الهطول والإنذار (مم)",
    "rain_sim_val": 25,
    "pct_boost": 15,
    "storm_hours": 6,
    "show_terrain": True,
    "show_wadis": True,
    "show_basins": True,
    "picked_station": None,
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
    st.session_state.show_terrain = True
    st.session_state.show_wadis = True
    st.session_state.show_basins = True

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

    out["Eff_Soil_Sat_Pct"] = np.clip(out["Soil_Saturation_Pct"] + (out["Forecast_Rain"] * 0.14), 15.0, 100.0)
    runoff_coeff = np.clip(0.22 + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.35 + out["Low_Perm_Factor"] * 0.32, 0.25, 0.92)
    out["Runoff_m3s"] = np.round(out["Forecast_Rain"] * runoff_coeff * (1.2 + out["Elevation_m"] / 1600.0), 1)
    out["Arrival_Hours"] = np.round(np.clip(6.5 - (out["Forecast_Rain"] / 55.0) + (out["Elevation_m"] / 1400.0), 1.2, 8.5), 1)

    storm_boost = 1.0 if "الأمطار" in h_type else 1.35
    washout_factor = np.where(out["Forecast_Rain"] > 50.0, 0.72, 1.0)
    out["Eff_Wind_kmh"] = np.round(
        out["Wind_kmh"] * (1.0 + (rain_extra / 240.0) + (0.20 if "العواصف" in h_type else 0.0)),
        0
    )
    out["Eff_Dust_ugm3"] = np.round(
        np.maximum(15.0, out["Dust_ugm3"] * (1.0 + (out["Eff_Wind_kmh"] - 25.0) / 80.0) * washout_factor),
        0
    )
    out["Eff_AQI"] = np.clip(
        np.round(out["AQI"] * 0.55 + (out["Eff_Dust_ugm3"] * 0.45) * storm_boost - (out["Forecast_Rain"] * 0.12)),
        18,
        260
    ).astype(int)

    out["Susceptibility_Idx"] = np.clip(
        (out["Forecast_Rain"] / 210.0) * 0.50
        + (out["Eff_Soil_Sat_Pct"] / 100.0) * 0.25
        + out["Low_Perm_Factor"] * 0.25,
        0.05,
        0.99
    )
    out["Dew_Point_C"] = np.round(out["Temp_C"] - ((100.0 - out["Humidity_Pct"]) / 5.0), 1)

    def _row_meta(r_item):
        rain_v = float(r_item["Forecast_Rain"])
        susc_v = float(r_item["Susceptibility_Idx"])
        if rain_v < 45 and susc_v < 0.45:
            a_lbl, t_col = "أزرق · مستقر", [3, 105, 161, 255]
            adv_txt = "حالة مستقرة؛ متابعة اعتيادية للأجواء ومجاري الأودية."
        elif rain_v < 80 and susc_v < 0.65:
            a_lbl, t_col = "أصفر · تنبيه مبكر", [161, 98, 7, 255]
            adv_txt = "تنبيه مبكر؛ تشبع جزئي للتربة واحتمال جريان متوسط في الشعاب."
        elif rain_v < 120 and susc_v < 0.80:
            a_lbl, t_col = "برتقالي · حيطة وحذر", [194, 65, 12, 255]
            adv_txt = "حيطة وحذر؛ جريان نشط محتمل وتجنب نقاط الاختناق والأودية."
        else:
            a_lbl, t_col = "أحمر · إنذار سيول شديد", [185, 28, 28, 255]
            adv_txt = "إنذار سيول شديد؛ سرعة استجابة عالية وتجنب بطون الأودية فوراً."

        if "AQI" in m_layer:
            aq_val = float(r_item["Eff_AQI"])
            w_val = min(aq_val / 220.0, 1.0)
            read_txt = f"AQI {int(aq_val)}"
        elif "الرياح" in m_layer:
            w_spd = float(r_item["Eff_Wind_kmh"])
            w_val = min(w_spd / 70.0, 1.0)
            read_txt = f"{w_spd:.0f} km/h"
        else:
            w_val = min(rain_v / 180.0, 1.0)
            read_txt = f"{rain_v:.1f} mm"

        return a_lbl, t_col, adv_txt, w_val, read_txt, f"{r_item['Governorate']} · {read_txt}"

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

top_st = filtered.sort_values("Forecast_Rain", ascending=False).iloc[0]
avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_risk = filtered["Susceptibility_Idx"].mean()
avg_runoff = filtered["Runoff_m3s"].mean()
avg_soil = filtered["Eff_Soil_Sat_Pct"].mean()
avg_arrival = filtered["Arrival_Hours"].mean()
avg_aqi = int(filtered["Eff_AQI"].mean())
severe_cnt = int((filtered["Forecast_Rain"] >= 80).sum())

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
    "الوضع الطبيعي (1964–2014)"
    if (rain_add == 0 and pct_boost == 0 and storm_hours == 6)
    else f"+{rain_add} مم · ({pct_boost:+d}% / {storm_hours} س)"
)

# 1) الشريط العلوي الرئيسي
st.markdown(f"""
    <div class="rasd-header">
        <div>
            <span class="brand-title">RASD</span>
            <span class="brand-badge">{st.session_state.selected_gov}</span>
            <span class="brand-badge">{model_mode}</span>
            <span class="brand-badge">{hazard_type}</span>
        </div>
        <div class="header-meta">
            <div><b>{source_tag}</b> · 26 محطة MEWA (مكة المكرمة والباحة)</div>
            <div>{audience_mode} · {horizon_mode}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# شريط الحالة الفورية في الأعلى
st.markdown(f"""
    <div class="live-strip">
        <div>
            <span style="color:#7dd3fc;font-weight:700;">حالة الرصد المباشرة:</span>
            <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]}
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            <span class="live-pill">أعلى حوض: <b>{top_st["Basin"]}</b></span>
            <span class="live-pill">نقطة حرجة: <b>{top_st["Hotspot"]}</b></span>
            <span class="live-pill">وصول الجريان: <b>~{avg_arrival:.1f} س</b></span>
            <span class="live-pill">تشبع التربة: <b>{avg_soil:.0f}%</b></span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2) أزرار التبديل المباشرة في نفس الصفحة
r1_a, r1_b, r1_c = st.columns([2.2, 1.4, 1.6])

with r1_a:
    st.markdown('<div class="bar-label">شريط المناطق التفاعلي السريع (نقرة واحدة)</div>', unsafe_allow_html=True)
    gov_buttons = ["الكل", "مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة", "الباحة", "المخواة"]
    g_cols = st.columns(len(gov_buttons))
    for idx_g, g_name in enumerate(gov_buttons):
        g_sub = sim_all_df if g_name == "الكل" else sim_all_df[sim_all_df["Governorate"] == g_name]
        g_max = g_sub["Forecast_Rain"].max()
        dot = "🔴" if g_max >= 120 else ("🟠" if g_max >= 80 else ("🟡" if g_max >= 45 else "🔵"))
        active_mark = "✦ " if st.session_state.selected_gov == g_name else ""
        if g_cols[idx_g].button(f"{active_mark}{dot} {g_name}", key=f"gov_btn_{g_name}"):
            st.session_state.selected_gov = g_name
            st.rerun()

with r1_b:
    st.markdown('<div class="bar-label">النموذج التحليلي</div>', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    if m_col1.button(("✦ " if model_mode == "Random Forest" else "") + "Random Forest", key="btn_rf"):
        st.session_state.model_mode = "Random Forest"
        st.rerun()
    if m_col2.button(("✦ " if model_mode == "AHP" else "") + "AHP", key="btn_ahp"):
        st.session_state.model_mode = "AHP"
        st.rerun()

with r1_c:
    st.markdown('<div class="bar-label">الأفق الزمني</div>', unsafe_allow_html=True)
    h_col1, h_col2, h_col3 = st.columns(3)
    if h_col1.button(("✦ " if "Nowcasting" in horizon_mode else "") + "Nowcasting", key="btn_now"):
        st.session_state.horizon_mode = "التنبؤ الآني (Nowcasting - 24h)"
        st.rerun()
    if h_col2.button(("✦ " if "14 Days" in horizon_mode else "") + "14 Days", key="btn_14d"):
        st.session_state.horizon_mode = "التوقعات الممتدة (14 Days)"
        st.rerun()
    if h_col3.button(("✦ " if "Seasonal" in horizon_mode else "") + "Seasonal", key="btn_seas"):
        st.session_state.horizon_mode = "النماذج الفصلية (Seasonal)"
        st.rerun()

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

r2_a, r2_b = st.columns(2)
with r2_a:
    st.markdown('<div class="bar-label">الظاهرة المرصودة</div>', unsafe_allow_html=True)
    hz_col1, hz_col2 = st.columns(2)
    if hz_col1.button(("✦ " if "الأمطار" in hazard_type else "") + "الأمطار والسيول", key="btn_hz_rain"):
        st.session_state.hazard_type = "الأمطار الغزيرة والسيول"
        st.rerun()
    if hz_col2.button(("✦ " if "العواصف" in hazard_type else "") + "العواصف والرياح", key="btn_hz_wind"):
        st.session_state.hazard_type = "العواصف الرعدية والرياح"
        st.rerun()

with r2_b:
    st.markdown('<div class="bar-label">مؤشر الخريطة اللونية</div>', unsafe_allow_html=True)
    ml_col1, ml_col2 = st.columns(2)
    if ml_col1.button(("✦ " if "الهطول" in map_layer else "") + "الهطول والإنذار", key="btn_ml_rain"):
        st.session_state.map_layer = "الهطول والإنذار (مم)"
        st.rerun()
    if ml_col2.button(("✦ " if "AQI" in map_layer else "") + "AQI جودة الهواء", key="btn_ml_aqi"):
        st.session_state.map_layer = "جودة الهواء (AQI)"
        st.rerun()

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# 3) الصف الأول: 4 كروت أرقام
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
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">متوسط الهطول المتوقع</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">مقارنة بالطبيعي: {diff_rain:+.1f} mm · الذروة {max_rain:.1f} mm</div></div>""",
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
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الذروة المتوقعة ({model_mode})</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{max_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">RF: {filtered["Rain_RF"].mean():.1f} mm · AHP: {filtered["Rain_AHP"].mean():.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">مؤشر الحساسية (FSI)</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val">{avg_risk:.2f}</div><div class="top-kpi-sub">تشبع التربة: {avg_soil:.0f}% · نفاذية منخفضة {filtered["Low_Perm_Factor"].mean():.2f}</div></div>""",
        unsafe_allow_html=True
    )
    c3.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الجريان السطحي للأودية</span><span class="{trend_runoff_cls}">{trend_runoff_lbl}</span></div><div class="top-kpi-val">{avg_runoff:.1f} <span class="top-kpi-unit">m³/s</span></div><div class="top-kpi-sub">الفرق عن الطبيعي: {diff_runoff:+.1f} m³/s · وصول ~{avg_arrival:.1f} س</div></div>""",
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
            <div style="font-size:13px;font-weight:700;color:#7dd3fc;">ماذا يعني هذا لك الآن؟ ({top_st["Governorate"]})</div>
            <div style="font-size:12px;color:#f1f5f9;margin-top:4px;">
                مستوى الحالة الحالي: <b>{top_st["Alert_Level"]}</b> — {top_st["Advice"]}
                الزمن التقديري لوصول الجريان قرب <b>{top_st["Hotspot"]}</b> هو <b>{top_st["Arrival_Hours"]} ساعة</b>، وجودة الهواء الحالية <b>{avg_aqi} AQI</b>.
            </div>
        </div>
    """, unsafe_allow_html=True)

# 4) الصف الأوسط: المؤشر الدائري + الخريطة الفاتحة + بطاقة الإنذار
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
    st.markdown(f'<div class="card-sub" style="text-align:center;">الفارق عن الطبيعي: {diff_risk*100:+.1f}% · {source_tag}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with m_center:
    st.markdown(f'<div class="card-box"><div class="card-title">خريطة تفاعلية فاتحة بالقراءات اللونية · {map_layer}</div>', unsafe_allow_html=True)

    t_col1, t_col2, t_col3 = st.columns(3)
    if t_col1.button(("● " if st.session_state.show_terrain else "○ ") + "التضاريس الجبلية", key="btn_l_terr"):
        st.session_state.show_terrain = not st.session_state.show_terrain
        st.rerun()
    if t_col2.button(("● " if st.session_state.show_wadis else "○ ") + "مسار الأودية", key="btn_l_wadi"):
        st.session_state.show_wadis = not st.session_state.show_wadis
        st.rerun()
    if t_col3.button(("● " if st.session_state.show_basins else "○ ") + "الأحواض المائية", key="btn_l_basin"):
        st.session_state.show_basins = not st.session_state.show_basins
        st.rerun()

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

    if st.session_state.show_terrain and len(filtered) > 0:
        high_elev = filtered[filtered["Elevation_m"] >= 600.0]
        if len(high_elev) > 0:
            map_layers.append(pdk.Layer(
                "ScatterplotLayer",
                data=high_elev,
                get_position=["lon", "lat"],
                get_fill_color=[120, 113, 108, 65],
                get_line_color=[87, 83, 78, 180],
                line_width_min_pixels=1.5,
                stroked=True,
                filled=True,
                get_radius="Elevation_m * 11",
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
            get_color=[3, 105, 161, 130],
            width_min_pixels=1.5,
            pickable=True,
        ))

    if st.session_state.show_wadis and len(filtered) > 0:
        wadi_paths = []
        for _, r_row in filtered.iterrows():
            sev_high = r_row["Forecast_Rain"] >= 80
            w_col = [220, 38, 38, 235] if sev_high else [2, 132, 199, 210]
            w_px = 4.5 if sev_high else 2.5
            wadi_paths.append({
                "basin": r_row["Basin"],
                "hotspot": r_row["Hotspot"],
                "arrival": f"{r_row['Arrival_Hours']} س",
                "w_col": w_col,
                "w_px": w_px,
                "path": [
                    [float(r_row["lon"]) + 0.10, float(r_row["lat"]) + 0.08],
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
            "html": "<b>{Station}</b> ({Governorate})<br/>الحوض: {Basin}<br/>نقطة حرجة: {Hotspot}<br/>{Alert_Level}<br/>القراءة: <b>{Reading_Str}</b> · وصول السيل: {Arrival_Hours} س",
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
                • <b>الارتفاع:</b> {top_st["Elevation_m"]:.0f} م · <b>AQI:</b> {int(top_st["Eff_AQI"])}
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5) الفحص المباشر للمحطة/الوادي + منحنى التوقعات الزمنية ونطاق عدم اليقين + مصفوفة القطاعات
station_list = filtered["Station"].tolist()
if st.session_state.picked_station not in station_list:
    st.session_state.picked_station = station_list[0]

st.markdown('<div class="bar-label">فحص مباشر للمحطة / الوادي (Click-to-Inspect بدون قوائم منبثقة)</div>', unsafe_allow_html=True)
pk_cols = st.columns(min(len(station_list), 7))
for i_s, s_code in enumerate(station_list[:7]):
    s_info = filtered[filtered["Station"] == s_code].iloc[0]
    mark = "✦ " if st.session_state.picked_station == s_code else ""
    if pk_cols[i_s].button(f"{mark}{s_code} ({s_info['Governorate']})", key=f"pick_{s_code}"):
        st.session_state.picked_station = s_code
        st.rerun()

st_row = filtered[filtered["Station"] == st.session_state.picked_station].iloc[0]

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
    st.markdown(
        f'<div class="card-sub">قراءات المحطة المفحوصة: <b>{st_row["Station"]}</b> | الهطول: <b>{st_row["Forecast_Rain"]:.1f} mm</b> | الجريان: <b>{st_row["Runoff_m3s"]:.1f} m³/s</b> | وصول السيل: <b>{st_row["Arrival_Hours"]} س</b> | AQI: <b>{int(st_row["Eff_AQI"])}</b></div>',
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
    f"RASD | النطاق: {st.session_state.selected_gov} | الإنذار: {top_st['Alert_Level']} | "
    f"الذروة: {max_rain:.1f} mm ({diff_rain:+.1f} عن الطبيعي) | الجريان: {avg_runoff:.1f} m³/s | "
    f"وصول السيل: ~{avg_arrival:.1f} س | AQI: {avg_aqi} | الإجراء: {act_road}"
)

st.markdown('<div class="card-box"><div class="card-title">ملخص تنفيذي وتصدير سريع للبيانات</div>', unsafe_allow_html=True)
st.markdown(f'<div class="summary-box">{exec_summary}</div>', unsafe_allow_html=True)

cols_out = [
    "Station", "Governorate", "Basin", "Hotspot", "Elevation_m",
    "Eff_Soil_Sat_Pct", "Rain_AHP", "Rain_RF", "Runoff_m3s",
    "Arrival_Hours", "Eff_Wind_kmh", "Eff_AQI", "Susceptibility_Idx", "Alert_Level"
]
st.dataframe(filtered[cols_out], use_container_width=True)

ex1, ex2 = st.columns(2)
ex1.download_button(
    label="تحميل بيانات السيناريو والمحطات (CSV)",
    data=filtered[cols_out].to_csv(index=False).encode("utf-8-sig"),
    file_name="RASD_Scenario_Report.csv",
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
    file_name="RASD_Scenario_Report.xls",
    mime="application/vnd.ms-excel"
)
st.markdown("</div>", unsafe_allow_html=True)
