import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go

st.set_page_config(
    page_title="RASD — منظومة التنبؤ والإنذار المبكر بالطقس والسيول",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #06101e;
        color: #e6eef8;
    }
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 0.75rem !important;
        max-width: 100% !important;
    }
    section[data-testid="stSidebar"] {
        display: none;
    }
    button[kind="header"] {
        display: none;
    }
    .stButton > button,
    .stButton > button * {
        background-color: #0d2240 !important;
        color: #e2e8f0 !important;
        border: 1px solid #234675 !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        padding: 0.3rem 0.55rem !important;
    }
    .stButton > button:hover,
    .stButton > button:hover * {
        background-color: #153969 !important;
        color: #7dd3fc !important;
        border-color: #38bdf8 !important;
    }
    .top-control-panel {
        background: linear-gradient(135deg, #0b2442 0%, #091b33 65%, #071426 100%);
        border: 1px solid #255285;
        border-radius: 10px;
        padding: 9px 14px;
        margin-bottom: 8px;
    }
    .rasd-header {
        background: linear-gradient(90deg, #091b33 0%, #0e2647 100%);
        border: 1px solid #1d3b66;
        border-radius: 9px;
        padding: 8px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .brand-title {
        font-size: 16px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .brand-badge {
        background-color: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #7dd3fc;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 5px;
    }
    .header-meta {
        font-size: 11px;
        color: #9cb8dc;
        text-align: left;
    }
    .bar-label {
        font-size: 11px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 4px;
    }
    .whatif-pill {
        background-color: #081426;
        border: 1px solid #234675;
        border-radius: 7px;
        padding: 6px 10px;
        font-size: 11px;
        color: #cbd5e1;
        margin-top: 4px;
    }
    .top-kpi {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 9px;
        padding: 9px 13px;
        min-height: 76px;
    }
    .top-kpi-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3px;
    }
    .top-kpi-title {
        font-size: 11px;
        color: #94b2d6;
        font-weight: 600;
    }
    .trend-up {
        font-size: 10px;
        font-weight: 700;
        color: #f87171;
        background: rgba(248, 113, 113, 0.14);
        padding: 1px 6px;
        border-radius: 5px;
    }
    .trend-down {
        font-size: 10px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.14);
        padding: 1px 6px;
        border-radius: 5px;
    }
    .trend-flat {
        font-size: 10px;
        font-weight: 700;
        color: #facc15;
        background: rgba(250, 204, 21, 0.14);
        padding: 1px 6px;
        border-radius: 5px;
    }
    .top-kpi-val {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
    }
    .top-kpi-unit {
        font-size: 12px;
        font-weight: 500;
        color: #7dd3fc;
    }
    .top-kpi-sub {
        font-size: 11px;
        color: #9cb8dc;
        margin-top: 2px;
    }
    .card-box {
        background-color: #0c1c34;
        border: 1px solid #1b3456;
        border-radius: 9px;
        padding: 10px 13px;
        margin-bottom: 8px;
    }
    .card-title {
        font-size: 12px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .dark-side-card {
        background: linear-gradient(180deg, #0d2340 0%, #091629 100%);
        border: 1px solid #234675;
        border-radius: 9px;
        padding: 11px 13px;
        margin-bottom: 8px;
    }
    .alert-banner {
        background-color: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.32);
        border-radius: 7px;
        padding: 8px 10px;
        margin: 7px 0;
        font-size: 11px;
    }
    .legend-strip {
        font-size: 10px;
        color: #cbd5e1;
        margin-top: 6px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .sector-row {
        padding: 5px 0;
        border-bottom: 1px solid #183052;
        font-size: 11px;
        line-height: 1.4;
    }
    .sector-row:last-child {
        border-bottom: none;
    }
    .summary-box {
        background-color: #081426;
        border: 1px solid #234675;
        border-radius: 7px;
        padding: 7px 11px;
        font-size: 11px;
        color: #e2e8f0;
        margin-bottom: 6px;
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

def set_scenario(r_val, p_val, h_val=None):
    st.session_state.rain_sim_val = r_val
    st.session_state.pct_boost = p_val
    st.session_state["sl_rain"] = r_val
    st.session_state["sl_pct"] = p_val
    if h_val is not None:
        st.session_state.storm_hours = h_val
        st.session_state["sl_hrs"] = h_val

def reset_all_controls():
    st.session_state.selected_gov = "الكل"
    st.session_state.model_mode = "Random Forest"
    st.session_state.horizon_mode = "التنبؤ الآني (Nowcasting - 24h)"
    st.session_state.hazard_type = "الأمطار الغزيرة والسيول"
    st.session_state.map_layer = "الهطول والإنذار (مم)"
    st.session_state.rain_sim_val = 0
    st.session_state.pct_boost = 0
    st.session_state.storm_hours = 6
    st.session_state["sl_rain"] = 0
    st.session_state["sl_pct"] = 0
    st.session_state["sl_hrs"] = 6
    st.session_state.show_boundary = True
    st.session_state.show_terrain = True
    st.session_state.show_wadis = True
    st.session_state.show_basins = True
    st.session_state.picked_station = "TA109"

# 1) لوحة التحكم والسيناريوهات بالعرض فوق
st.markdown('<div class="top-control-panel">', unsafe_allow_html=True)
top_c1, top_c2, top_c3 = st.columns([1.25, 2.25, 2.3])

with top_c1:
    st.markdown('<div class="bar-label">زاوية العرض</div>', unsafe_allow_html=True)
    aud_choice = st.radio(
        "زاوية العرض",
        ["للجهة والقطاعات (Technical)", "للفرد والسكان (Public)"],
        index=0 if st.session_state.audience_mode.startswith("للجهة") else 1,
        label_visibility="collapsed",
        key="top_aud_radio"
    )
    st.session_state.audience_mode = aud_choice

with top_c2:
    st.markdown('<div class="bar-label">سيناريوهات جاهزة + Reset</div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    if sc1.button("وضع طبيعي", key="top_sb_norm"):
        set_scenario(0, 0, 6)
        st.rerun()
    if sc2.button("هطول متوسط", key="top_sb_mod"):
        set_scenario(40, 15, 8)
        st.rerun()
    if sc3.button("عاصفة غزيرة", key="top_sb_heavy"):
        set_scenario(95, 35, 12)
        st.rerun()
    if sc4.button("سيناريو حرج", key="top_sb_crit"):
        set_scenario(155, 60, 18)
        st.rerun()
    if sc5.button("Reset", key="top_sb_reset"):
        reset_all_controls()
        st.rerun()

with top_c3:
    sl1, sl2, sl3 = st.columns(3)
    st.session_state.rain_sim_val = sl1.slider(
        "زيادة الهطول (مم)", 0, 180, int(st.session_state.rain_sim_val), 5, key="sl_rain"
    )
    st.session_state.pct_boost = sl2.slider(
        "What-If الهطول (%)", -20, 100, int(st.session_state.pct_boost), 5, key="sl_pct"
    )
    st.session_state.storm_hours = sl3.slider(
        "مدة العاصفة (ساعات)", 2, 24, int(st.session_state.storm_hours), 2, key="sl_hrs"
    )

st.markdown("</div>", unsafe_allow_html=True)

def compute_hydro(base_df, rain_extra, pct_chg, dur_hrs, h_mode, m_mode, m_layer, h_type):
    out = base_df.copy()
    is_seasonal = "Seasonal" in h_mode
    h_mult = 1.0 if "Nowcasting" in h_mode else (1.15 if "14 Days" in h_mode else 1.25)
    dur_factor = 0.75 + (dur_hrs / 12.0) * 0.45
    pct_factor = 1.0 + (pct_chg / 100.0)

    out["Rain_RF"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (rain_extra * 1.25)) * h_mult * dur_factor, 1)
    out["Rain_AHP"] = np.round((out["Hist_Mean_Rain"] * pct_factor + (rain_extra * 0.92)) * h_mult * dur_factor, 1)
    out["Forecast_Rain"] = out["Rain_RF"] if m_mode == "Random Forest" else out["Rain_AHP"]

    # مؤشر التراكم / التكرار الموسمي عند اختيار النطاق الموسمي
    out["Seasonal_Accum_mm"] = np.round(out["Forecast_Rain"] * 2.4, 1)
    out["Recurrence_Pct"] = np.clip(
        np.round(28.0 + (out["Forecast_Rain"] / 260.0) * 52.0 + (out["Low_Perm_Factor"] * 15.0)),
        15.0,
        96.0
    )

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
            a_lbl, t_col = "أزرق · مستقر", [56, 189, 248, 255]
            adv_txt = "حالة مستقرة؛ متابعة اعتيادية للأجواء ومجاري الأودية."
        elif rain_v < 135 and susc_v < 0.65:
            a_lbl, t_col = "أصفر · تنبيه مبكر", [250, 204, 21, 255]
            adv_txt = "تنبيه مبكر؛ تشبع جزئي للتربة واحتمال جريان متوسط."
        elif rain_v < 190 and susc_v < 0.80:
            a_lbl, t_col = "برتقالي · حيطة وحذر", [251, 146, 60, 255]
            adv_txt = "حيطة وحذر؛ جريان نشط محتمل وتجنب نقاط الاختناق."
        else:
            a_lbl, t_col = "أحمر · إنذار سيول شديد", [248, 113, 113, 255]
            adv_txt = "إنذار سيول شديد؛ تجنب بطون الأودية فوراً."

        if "AQI" in m_layer:
            aq_val = float(r_item["Eff_AQI"])
            w_val = min(aq_val / 220.0, 1.0)
            read_txt = f"AQI {int(aq_val)}"
        elif is_seasonal:
            acc_v = float(r_item["Seasonal_Accum_mm"])
            w_val = min(acc_v / 520.0, 1.0)
            read_txt = f"{acc_v:.0f}mm موسمي"
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

audience_mode = st.session_state.audience_mode
model_mode = st.session_state.model_mode
horizon_mode = st.session_state.horizon_mode
hazard_type = st.session_state.hazard_type
map_layer = st.session_state.map_layer
rain_add = st.session_state.rain_sim_val
pct_boost = st.session_state.pct_boost
storm_hours = st.session_state.storm_hours
is_seasonal = "Seasonal" in horizon_mode

avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_seasonal_acc = filtered["Seasonal_Accum_mm"].mean()
avg_recurrence = filtered["Recurrence_Pct"].mean()
avg_risk = filtered["Susceptibility_Idx"].mean()
avg_runoff = filtered["Runoff_m3s"].mean()
avg_arrival = filtered["Arrival_Hours"].mean()
avg_aqi = int(filtered["Eff_AQI"].mean())
severe_cnt = int((filtered["Forecast_Rain"] >= 135).sum())

diff_rain = avg_rain - base_filt["Forecast_Rain"].mean()
diff_runoff = avg_runoff - base_filt["Runoff_m3s"].mean()
diff_risk = avg_risk - base_filt["Susceptibility_Idx"].mean()
diff_aqi = avg_aqi - int(base_filt["Eff_AQI"].mean())
whatif_net_rain = avg_rain * (1.0 + pct_boost / 100.0)

source_tag = (
    "المرجع التاريخي (1964–2014)"
    if (rain_add == 0 and pct_boost == 0 and storm_hours == 6 and "Nowcasting" in horizon_mode)
    else f"+{rain_add} مم · What-If {pct_boost:+d}% · {storm_hours} س"
)

# 2) الشريط العلوي المختصر
st.markdown(f"""
    <div class="rasd-header">
        <div>
            <span class="brand-title">RASD</span>
            <span class="brand-badge">{st.session_state.selected_gov}</span>
            <span class="brand-badge">{st_row["Station"]} · {st_row["Basin"]}</span>
            <span class="brand-badge">{model_mode}</span>
        </div>
        <div class="header-meta">
            <b>{source_tag}</b> · {horizon_mode} · {hazard_type}
        </div>
    </div>
""", unsafe_allow_html=True)

# 3) صف أفق واحد منظم للمناطق + النموذج + الأفق + الظاهرة + المؤشر + What-If
c_gov, c_mod, c_hor, c_haz, c_lay = st.columns([2.2, 0.9, 1.25, 1.0, 0.95])

with c_gov:
    st.markdown('<div class="bar-label">المحافظة / النطاق</div>', unsafe_allow_html=True)
    gov_buttons = ["الكل", "مكة المكرمة", "جدة", "الطائف", "الليث", "القنفذة"]
    g_cols = st.columns(len(gov_buttons))
    for idx_g, g_name in enumerate(gov_buttons):
        mark = "✦ " if st.session_state.selected_gov == g_name else ""
        if g_cols[idx_g].button(f"{mark}{g_name}", key=f"gov_btn_{g_name}"):
            st.session_state.selected_gov = g_name
            st.rerun()

with c_mod:
    st.markdown('<div class="bar-label">النموذج</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    if m1.button(("✦ " if model_mode == "Random Forest" else "") + "RF", key="btn_rf"):
        st.session_state.model_mode = "Random Forest"
        st.rerun()
    if m2.button(("✦ " if model_mode == "AHP" else "") + "AHP", key="btn_ahp"):
        st.session_state.model_mode = "AHP"
        st.rerun()

with c_hor:
    st.markdown('<div class="bar-label">الأفق الزمني</div>', unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    if h1.button(("✦ " if "Nowcasting" in horizon_mode else "") + "+24h", key="btn_now"):
        st.session_state.horizon_mode = "التنبؤ الآني (Nowcasting - 24h)"
        st.rerun()
    if h2.button(("✦ " if "14 Days" in horizon_mode else "") + "14d", key="btn_14d"):
        st.session_state.horizon_mode = "التوقعات الممتدة (14 Days)"
        st.rerun()
    if h3.button(("✦ " if is_seasonal else "") + "موسمي", key="btn_seas"):
        st.session_state.horizon_mode = "النماذج الفصلية (Seasonal)"
        st.rerun()

with c_haz:
    st.markdown('<div class="bar-label">الظاهرة</div>', unsafe_allow_html=True)
    z1, z2 = st.columns(2)
    if z1.button(("✦ " if "الأمطار" in hazard_type else "") + "سيول", key="btn_hz_rain"):
        st.session_state.hazard_type = "الأمطار الغزيرة والسيول"
        st.rerun()
    if z2.button(("✦ " if "العواصف" in hazard_type else "") + "عواصف", key="btn_hz_wind"):
        st.session_state.hazard_type = "العواصف الرعدية والرياح"
        st.rerun()

with c_lay:
    st.markdown('<div class="bar-label">مؤشر الخريطة</div>', unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    if l1.button(("✦ " if "الهطول" in map_layer else "") + "هطول", key="btn_ml_rain"):
        st.session_state.map_layer = "الهطول والإنذار (مم)"
        st.rerun()
    if l2.button(("✦ " if "AQI" in map_layer else "") + "AQI", key="btn_ml_aqi"):
        st.session_state.map_layer = "جودة الهواء (AQI)"
        st.rerun()

# شريط What-If واضح ومباشر
st.markdown(
    f'<div class="whatif-pill"><b>مؤشر What-If النشط:</b> نسبة التغير <b>{pct_boost:+d}%</b> · الهطول الفعلي المتوقع بعد التعديل: <b>{whatif_net_rain:.1f} mm</b> · مدة العاصفة: <b>{storm_hours} ساعات</b></div>',
    unsafe_allow_html=True
)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# 4) 4 كروت أرقام مختصرة وواضحة
trend_rain_cls = "trend-up" if diff_rain > 2 else ("trend-down" if diff_rain < -2 else "trend-flat")
trend_rain_lbl = f"+{diff_rain:.1f} mm" if diff_rain > 2 else (f"{diff_rain:.1f} mm" if diff_rain < -2 else "0.0 mm")

trend_risk_cls = "trend-up" if diff_risk > 0.02 else ("trend-down" if diff_risk < -0.02 else "trend-flat")
trend_risk_lbl = f"+{diff_risk:.2f}" if diff_risk > 0.02 else (f"{diff_risk:.2f}" if diff_risk < -0.02 else "مستقر")

trend_runoff_cls = "trend-up" if diff_runoff > 3 else ("trend-down" if diff_runoff < -3 else "trend-flat")
trend_runoff_lbl = f"+{diff_runoff:.1f}" if diff_runoff > 3 else (f"{diff_runoff:.1f}" if diff_runoff < -3 else "ثابت")

trend_aqi_cls = "trend-up" if diff_aqi > 5 else ("trend-down" if diff_aqi < -5 else "trend-flat")
trend_aqi_lbl = f"+{diff_aqi} AQI" if diff_aqi > 5 else (f"{diff_aqi} AQI" if diff_aqi < -5 else "معتدل")

c1, c2, c3, c4 = st.columns(4)
if is_seasonal:
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">التراكم الفصلي المتوقع</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_seasonal_acc:.0f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_rain:+.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">احتمالية التكرار الموسمي</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val">{avg_recurrence:.0f}<span class="top-kpi-unit">%</span></div><div class="top-kpi-sub">درجة الحساسية: {avg_risk:.2f}</div></div>""",
        unsafe_allow_html=True
    )
elif audience_mode.startswith("للفرد"):
    status_txt = "إنذار مرتفع" if severe_cnt >= 3 else ("تنبيه مبكر" if severe_cnt > 0 else "مستقر")
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">حالة الإنذار اللحظية</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val" style="font-size:18px;color:#7dd3fc;">{status_txt}</div><div class="top-kpi-sub">وصول متوقع خلال {avg_arrival:.1f} س</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">متوسط الهطول المتوقع</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{avg_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_rain:+.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
else:
    c1.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">ذروة الهطول ({model_mode})</span><span class="{trend_rain_cls}">{trend_rain_lbl}</span></div><div class="top-kpi-val">{max_rain:.1f} <span class="top-kpi-unit">mm</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_rain:+.1f} mm</div></div>""",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">مؤشر الحساسية (FSI)</span><span class="{trend_risk_cls}">{trend_risk_lbl}</span></div><div class="top-kpi-val">{avg_risk:.2f}</div><div class="top-kpi-sub">الفارق عن المرجع: {diff_risk*100:+.1f}%</div></div>""",
        unsafe_allow_html=True
    )

c3.markdown(
    f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">الجريان السطحي للأودية</span><span class="{trend_runoff_cls}">{trend_runoff_lbl}</span></div><div class="top-kpi-val">{avg_runoff:.1f} <span class="top-kpi-unit">m³/s</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_runoff:+.1f} m³/s</div></div>""",
    unsafe_allow_html=True
)
c4.markdown(
    f"""<div class="top-kpi"><div class="top-kpi-head"><span class="top-kpi-title">جودة الهواء والغبار</span><span class="{trend_aqi_cls}">{trend_aqi_lbl}</span></div><div class="top-kpi-val">{avg_aqi} <span class="top-kpi-unit">AQI</span></div><div class="top-kpi-sub">الفرق عن المرجع: {diff_aqi:+d} AQI</div></div>""",
    unsafe_allow_html=True
)

st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# 5) القسم الرئيسي: خريطة داكنة + مؤشر التدرج وبطاقة الإنذار + المنحنى الزمني
m_center, m_side = st.columns([2.6, 1.35])

with m_center:
    st.markdown(
        f'<div class="card-box"><div class="card-title">خريطة منطقة مكة المكرمة ({st.session_state.selected_gov}) · {map_layer}</div>',
        unsafe_allow_html=True
    )

    t_col0, t_col1, t_col2, t_col3 = st.columns(4)
    if t_col0.button(("● " if st.session_state.show_boundary else "○ ") + "الحدود", key="btn_l_bound"):
        st.session_state.show_boundary = not st.session_state.show_boundary
        st.rerun()
    if t_col1.button(("● " if st.session_state.show_terrain else "○ ") + "التضاريس", key="btn_l_terr"):
        st.session_state.show_terrain = not st.session_state.show_terrain
        st.rerun()
    if t_col2.button(("● " if st.session_state.show_wadis else "○ ") + "الأودية", key="btn_l_wadi"):
        st.session_state.show_wadis = not st.session_state.show_wadis
        st.rerun()
    if t_col3.button(("● " if st.session_state.show_basins else "○ ") + "الأحواض", key="btn_l_basin"):
        st.session_state.show_basins = not st.session_state.show_basins
        st.rerun()

    st_options = [
        f"{r['Station']} — {r['Basin']} ({r['Governorate']} | {r['Reading_Str']})"
        for _, r in filtered.iterrows()
    ]
    st_codes = filtered["Station"].tolist()
    curr_idx = st_codes.index(st.session_state.picked_station) if st.session_state.picked_station in st_codes else 0
    chosen_label = st.selectbox(
        "المحطة النشطة",
        options=st_options,
        index=curr_idx,
        label_visibility="collapsed",
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
            [56, 189, 248], [163, 230, 53], [250, 204, 21],
            [251, 146, 60], [220, 38, 38], [153, 27, 27]
        ]
    else:
        climate_color_range = [
            [186, 230, 253], [56, 189, 248], [2, 132, 199],
            [30, 64, 175], [251, 146, 60], [220, 38, 38]
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
            get_size=11,
            get_alignment_baseline="'bottom'",
            background=True,
            get_background_color=[8, 20, 38, 230],
            background_padding=[3, 5],
            pickable=True,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=active_df,
            get_position=["lon", "lat"],
            get_fill_color=[255, 255, 255, 240],
            get_line_color=[239, 68, 68, 255],
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
            data=[{"polygon": makkah_boundary_coords, "name": "حدود منطقة مكة المكرمة"}],
            get_polygon="polygon",
            get_fill_color=[56, 189, 248, 16],
            get_line_color=[125, 211, 252, 230],
            line_width_min_pixels=2.5,
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
            get_color=[148, 163, 184, 130],
            width_min_pixels=1.4,
            pickable=True,
        ))

    if st.session_state.show_wadis and len(filtered) > 0:
        wadi_paths = []
        for _, r_row in filtered.iterrows():
            sev_high = r_row["Forecast_Rain"] >= 135
            w_col = [248, 113, 113, 245] if sev_high else [56, 189, 248, 235]
            w_px = 5.0 if sev_high else 3.2
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
            width_min_pixels=2.5,
            pickable=True,
        ))

    if st.session_state.selected_gov == "الكل":
        view_lat = float(st_row["lat"]) if st.session_state.picked_station != "TA109" else 21.15
        view_lon = float(st_row["lon"]) if st.session_state.picked_station != "TA109" else 40.55
        view_zoom = 7.3 if st.session_state.picked_station != "TA109" else 6.65
    else:
        view_lat = float(st_row["lat"])
        view_lon = float(st_row["lon"])
        view_zoom = 7.5

    deck = pdk.Deck(
        layers=map_layers,
        initial_view_state=pdk.ViewState(
            latitude=view_lat,
            longitude=view_lon,
            zoom=view_zoom,
            pitch=0,
        ),
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        tooltip={
            "html": "<b>{Station}</b> ({Governorate})<br/>الحوض: {Basin}<br/>{Alert_Level}<br/>القراءة: <b>{Reading_Str}</b>",
            "style": {"backgroundColor": "#091b33", "color": "#ffffff"}
        }
    )
    st.pydeck_chart(deck, use_container_width=True, height=345)

    if "AQI" in map_layer:
        pos_pct = float(min(max((avg_aqi / 220.0) * 100.0, 2.0), 98.0))
        scale_mid = f"جودة الهواء: {avg_aqi} AQI ({pos_pct:.0f}%)"
        leg_html = """
            <span style="color:#38bdf8;font-weight:700;">■ جيد/مقبول</span>
            <span style="color:#facc15;font-weight:700;">■ متوسط</span>
            <span style="color:#fb923c;font-weight:700;">■ حساس</span>
            <span style="color:#f87171;font-weight:700;">■ إنذار بيئي</span>
            <span style="color:#38bdf8;font-weight:700;">━ مسار وادي</span>
        """
        c_stops = [[0.0, "#38bdf8"], [0.3, "#a3e635"], [0.55, "#facc15"], [0.78, "#fb923c"], [1.0, "#dc2626"]]
    else:
        pos_pct = float(min(max((rain_add / 180.0) * 100.0, 2.0), 98.0))
        scale_mid = f"مؤشر الهطول: +{rain_add} مم ({pct_boost:+d}% · {storm_hours} س) · {pos_pct:.0f}%"
        leg_html = """
            <span style="color:#7dd3fc;font-weight:700;">■ هطول منخفض/متوسط</span>
            <span style="color:#3b82f6;font-weight:700;">■ مرتفعات وهطول أعلى</span>
            <span style="color:#fb923c;font-weight:700;">■ حيطة وحذر</span>
            <span style="color:#f87171;font-weight:700;">■ إنذار سيول شديد</span>
            <span style="color:#38bdf8;font-weight:700;">━ مسار وادي</span>
        """
        c_stops = [[0.0, "#bae6fd"], [0.3, "#38bdf8"], [0.6, "#1d4ed8"], [0.82, "#fb923c"], [1.0, "#ef4444"]]

    st.markdown(f'<div class="legend-strip">{leg_html}</div>', unsafe_allow_html=True)
    bar_fig = go.Figure(go.Heatmap(
        z=[np.linspace(0, 100, 101)],
        x=list(range(101)),
        y=[0],
        colorscale=c_stops,
        showscale=False,
        hoverinfo="skip"
    ))
    bar_fig.add_trace(go.Scatter(
        x=[pos_pct],
        y=[0],
        mode="markers",
        marker=dict(size=15, color="#ffffff", line=dict(color="#06101e", width=2.5)),
        showlegend=False,
        hovertemplate=f"{scale_mid}<extra></extra>"
    ))
    bar_fig.update_layout(
        title=dict(text=scale_mid, font=dict(size=11, color="#7dd3fc"), x=0.5, xanchor="center"),
        height=66,
        margin=dict(l=15, r=15, t=22, b=14),
        paper_bgcolor="#081426",
        plot_bgcolor="#081426",
        xaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100], ticktext=["0%", "25%", "50%", "75%", "100%"], tickfont=dict(size=9, color="#cbd5e1"), showgrid=False, zeroline=False),
        yaxis=dict(visible=False, range=[-0.5, 0.5])
    )
    st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with m_side:
    st.markdown('<div class="card-box"><div class="card-title">مؤشر الخطورة والقابلية</div>', unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_risk * 100, 1),
        number={"suffix": "%", "font": {"size": 20, "color": "#ffffff"}},
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
        height=155,
        margin=dict(l=10, r=10, t=10, b=0),
        paper_bgcolor="#0c1c34",
        font={"color": "#e6eef8"}
    )
    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    has_coastal = any(g in coastal_govs for g in filtered["Governorate"])
    marine_txt = "موج 1.8 م · تيارات ساحلية" if has_coastal else "متابعة الأودية والجريان"
    st.markdown(f"""
        <div class="dark-side-card">
            <div style="font-size:11px;color:#7dd3fc;font-weight:700;">التنبيه اللحظي</div>
            <div style="font-size:14px;font-weight:700;margin-top:3px;">{top_st["Alert_Level"]}</div>
            <div class="alert-banner">
                <div><b>{top_st["Station"]}</b> ({top_st["Governorate"]}) · {top_st["Hotspot"]}</div>
                <div style="margin-top:3px;">وصول السيل: <b>~{top_st["Arrival_Hours"]} س</b> · تشبع التربة: <b>{top_st["Eff_Soil_Sat_Pct"]:.0f}%</b></div>
                <div style="color:#cbd5e1;margin-top:3px;">{top_st["Advice"]}</div>
            </div>
            <div style="font-size:11px;color:#cbd5e1;">• <b>الحالة البحرية/الأودية:</b> {marine_txt}</div>
        </div>
    """, unsafe_allow_html=True)

# 6) الصف السفلي المدمج: المنحنى الزمني/الموسمي + الإجراءات المختصرة في صفحة واحدة
b_left, b_right = st.columns([2.6, 1.35])

with b_left:
    chart_title = (
        f"التراكم الموسمي واحتمالية التكرار ({model_mode}) · {st_row['Station']}"
        if is_seasonal
        else f"التوقعات الزمنية ونطاق عدم اليقين ({model_mode}) · {st_row['Station']}"
    )
    st.markdown(f'<div class="card-box"><div class="card-title">{chart_title}</div>', unsafe_allow_html=True)

    if "Nowcasting" in horizon_mode:
        x_lbl = [f"+{i*2}h" for i in range(13)]
    elif "14 Days" in horizon_mode:
        x_lbl = [f"يوم {i+1}" for i in range(14)]
    else:
        x_lbl = ["الربيع", "الصيف", "الخريف", "الشتاء", "موسم 5", "موسم 6"]

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
        name="عدم اليقين"
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=y_rf, mode="lines+markers",
        name="Random Forest", line=dict(color="#38bdf8", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=y_ahp, mode="lines+markers",
        name="AHP", line=dict(color="#5eead4", width=2, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=x_lbl, y=[165.0]*n_pt, mode="lines",
        name="عتبة 165 mm", line=dict(color="#f87171", width=1.8, dash="dash")
    ))
    fig.update_layout(
        height=165,
        margin=dict(l=10, r=10, t=8, b=8),
        paper_bgcolor="#0c1c34",
        plot_bgcolor="#081426",
        font={"color": "#cbd5e1", "size": 10},
        xaxis=dict(gridcolor="#162c4d"),
        yaxis=dict(gridcolor="#162c4d"),
        legend=dict(orientation="h", y=1.18, x=0)
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with b_right:
    if "أحمر" in top_st["Alert_Level"]:
        act_water = "تفعيل الطوارئ وتصريف السدود عند الحد الآمن."
        act_road = "إغلاق المعابر المنخفضة وبطون الأودية فوراً."
        act_agri = "إيقاف العمليات الميدانية وحماية المواشي."
    elif "برتقالي" in top_st["Alert_Level"]:
        act_water = "رفع جاهزية الصيانة ومراقبة مناسيب الأودية."
        act_road = "تنبيهات سرعة ومراقبة الطرق الجبلية والساحلية."
        act_agri = "تأجيل الأعمال الميدانية وتأمين المعدات."
    else:
        act_water = "متابعة دورية لمحطات الرصد وتصريف المجاري."
        act_road = "رصد اعتيادي للحركة المرورية والرؤية."
        act_agri = "جدولة الري والطاقة وفق الأجواء الحالية."

    st.markdown(f"""
        <div class="card-box">
            <div class="card-title">الإجراءات والتوصيات ({top_st["Alert_Level"]})</div>
            <div class="sector-row"><b>المياه والسيول:</b> {act_water}</div>
            <div class="sector-row"><b>الطرق والمرور:</b> {act_road}</div>
            <div class="sector-row"><b>البيئة والزراعة:</b> {act_agri}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(
    f'<div class="summary-box"><b>ملخص الحالة:</b> {st.session_state.selected_gov} · المحطة {st_row["Station"]} ({top_st["Alert_Level"]}) · الهطول {avg_rain:.1f} mm · الجريان {avg_runoff:.1f} m³/s · AQI {avg_aqi}</div>',
    unsafe_allow_html=True
)
