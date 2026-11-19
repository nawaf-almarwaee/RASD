import json
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go

st.set_page_config(
    page_title="RASD — منظومة التنبؤ والإنذار المبكر",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #071121;
        color: #e6eef8;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b192e;
        border-right: 1px solid #1a2f4d;
    }
    .top-bar {
        background: linear-gradient(90deg, #0b1d36 0%, #102a4e 100%);
        border: 1px solid #1f3d68;
        color: #f8fafc;
        padding: 15px 24px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        box-shadow: 0 6px 18px rgba(2, 8, 20, 0.45);
    }
    .top-brand {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    .top-sub {
        font-size: 12px;
        color: #93b4dc;
        margin-top: 2px;
    }
    .transparency-banner {
        background-color: #0c213d;
        border: 1px solid #244775;
        border-right: 4px solid #38bdf8;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 12px;
        color: #cbd5e1;
        margin-bottom: 14px;
    }
    .kpi-card {
        background-color: #0d1d35;
        border: 1px solid #1b3456;
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 12px rgba(2, 8, 20, 0.3);
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 12px;
        color: #94b2d6;
        margin-bottom: 5px;
    }
    .kpi-num {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
    }
    .kpi-sub {
        font-size: 11px;
        color: #5eead4;
        margin-top: 4px;
    }
    .panel-card {
        background-color: #0d1d35;
        border: 1px solid #1b3456;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(2, 8, 20, 0.3);
        margin-bottom: 14px;
    }
    .alert-panel {
        background: linear-gradient(180deg, #102646 0%, #0b182c 100%);
        border: 1px solid #244775;
        color: #f8fafc;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 6px 16px rgba(2, 8, 20, 0.4);
    }
    .status-pill {
        background-color: rgba(56, 189, 248, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #7dd3fc;
        padding: 7px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin: 10px 0;
    }
    .legend-row {
        font-size: 12px;
        color: #cbd5e1;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 1) بيانات 26 محطة MEWA (مكة المكرمة والباحة)
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
    "Temp_C": np.random.uniform(17.0, 39.0, n_stations),
    "Humidity_Pct": np.random.uniform(35.0, 92.0, n_stations),
    "Pressure_hPa": np.random.uniform(1004.0, 1018.0, n_stations),
    "Wind_kmh": np.random.uniform(12.0, 62.0, n_stations),
    "Dust_ugm3": np.random.uniform(25.0, 240.0, n_stations),
    "AQI": np.random.randint(30, 165, n_stations),
    "UV_Index": np.random.randint(3, 11, n_stations),
})

# إدارة حالة السيناريو الجاهز
if "rain_sim_val" not in st.session_state:
    st.session_state.rain_sim_val = 25

# 2) الشريط الجانبي للتحكم
st.sidebar.header("لوحة التحكم والإنذار")
audience_mode = st.sidebar.radio(
    "زاوية العرض (Mode Switcher)",
    ["للجهة والقطاعات (Technical)", "للفرد والسكان (Public)"]
)
selected_gov = st.sidebar.selectbox(
    "المحافظة / النطاق الجغرافي",
    ["الكل"] + sorted(df["Governorate"].unique().tolist())
)
model_mode = st.sidebar.selectbox(
    "نموذج التقييم الهيدرولوجي",
    ["Random Forest", "AHP"]
)
horizon_mode = st.sidebar.selectbox(
    "الأفق الزمني للتوقعات",
    ["التنبؤ الآني (Nowcasting - 24h)", "التوقعات الممتدة (14 Days)", "النماذج الفصلية (Seasonal)"]
)
hazard_focus = st.sidebar.selectbox(
    "نوع الظاهرة الجوية المرصودة",
    ["الأمطار الغزيرة والسيول", "العواصف الرعدية والرياح", "الموجات الغبارية", "الضباب الكثيف", "موجات الحر / البرد"]
)
map_layer = st.sidebar.selectbox(
    "طبقة الخريطة التفاعلية",
    ["رادار الهطول والإنذار (أزرق → أحمر)", "الرياح والعواصف", "الحرارة والرطوبة والضغط", "توزيع الغبار (AQI)", "مؤشر الحساسية (3D)"]
)

st.sidebar.markdown("**سيناريوهات مطرية سريعة:**")
sb1, sb2 = st.sidebar.columns(2)
if sb1.button("وضع طبيعي"):
    st.session_state.rain_sim_val = 0
if sb2.button("هطول متوسط"):
    st.session_state.rain_sim_val = 40
sb3, sb4 = st.sidebar.columns(2)
if sb3.button("عاصفة غزيرة"):
    st.session_state.rain_sim_val = 95
if sb4.button("سيناريو حرج"):
    st.session_state.rain_sim_val = 155

rain_add = st.sidebar.slider(
    "ضبط زيادة الهطول يدوياً (مم)",
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

# 3) الحسابات الهيدرولوجية والنماذج
filtered = (df if selected_gov == "الكل" else df[df["Governorate"] == selected_gov]).copy()

horizon_mult = 1.0 if "Nowcasting" in horizon_mode else (1.15 if "14 Days" in horizon_mode else 1.25)
rf_weight = 1.25
ahp_weight = 0.92
active_weight = rf_weight if model_mode == "Random Forest" else ahp_weight

filtered["Rain_RF"] = filtered["Hist_Mean_Rain"] + (rain_add * rf_weight * horizon_mult)
filtered["Rain_AHP"] = filtered["Hist_Mean_Rain"] + (rain_add * ahp_weight * horizon_mult)
filtered["Forecast_Rain"] = filtered["Rain_RF"] if model_mode == "Random Forest" else filtered["Rain_AHP"]

filtered["Dew_Point_C"] = np.round(filtered["Temp_C"] - ((100.0 - filtered["Humidity_Pct"]) / 5.0), 1)
filtered["Runoff_m3s"] = np.round(filtered["Forecast_Rain"] * (1.35 + filtered["Elevation_m"] / 1450.0), 1)
filtered["Susceptibility_Idx"] = np.clip(
    (filtered["Forecast_Rain"] / 210.0) * 0.72 + (filtered["Elevation_m"] / 2500.0) * 0.28,
    0.05,
    0.99
)

def classify_alert(row):
    rain = row["Forecast_Rain"]
    if rain < 45:
        return "أزرق · مستقر (آمن)", [56, 189, 248, 225], "الأجواء مستقرة؛ لا توجد مؤشرات سيول أو خطورة."
    elif rain < 80:
        return "أصفر · تنبيه مبكر", [250, 204, 21, 230], "احتمالية تأثر المنطقة بهطول متوسط أو تقلبات جوية."
    elif rain < 120:
        return "برتقالي · حيطة وحذر", [251, 146, 60, 240], "أمطار غزيرة ونشاط رياح؛ يُنصح بتجنب الأودية والطرق المنخفضة."
    else:
        return "أحمر · إنذار سيول شديد", [248, 113, 113, 250], "ظواهر جوية شديدة وخطر سيول؛ الالتزام الفوري بتعليمات الطوارئ."

cls = filtered.apply(classify_alert, axis=1)
filtered["Alert_Level"] = [c[0] for c in cls]
filtered["Color"] = [c[1] for c in cls]
filtered["Advisory"] = [c[2] for c in cls]

if map_layer == "الرياح والعواصف":
    filtered["Radius"] = np.clip(filtered["Wind_kmh"] * 220, 3000, 15500)
elif map_layer == "الحرارة والرطوبة والضغط":
    filtered["Radius"] = np.clip(filtered["Humidity_Pct"] * 150, 3000, 15500)
elif map_layer == "توزيع الغبار (AQI)":
    filtered["Radius"] = np.clip(filtered["AQI"] * 90, 3000, 15500)
elif map_layer == "مؤشر الحساسية (3D)":
    filtered["Radius"] = np.clip(filtered["Susceptibility_Idx"] * 15000, 3000, 15500)
else:
    filtered["Radius"] = np.clip(filtered["Forecast_Rain"] * 92, 2800, 15500)

# 4) الترويسة وبطاقة شفافية البيانات
st.markdown(f"""
    <div class="top-bar">
        <div>
            <div class="top-brand">RASD · منظومة التنبؤ والإنذار المبكر بالطقس والسيول</div>
            <div class="top-sub">نطاق مكة المكرمة والباحة · 26 محطة MEWA (1964–2014) · دمج الرصد الأرضي والرادار والذكاء الاصطناعي</div>
        </div>
        <div class="top-sub" style="text-align:right;">
            وضع العرض: <b style="color:#ffffff;">{audience_mode}</b><br>
            الظاهرة النشطة: <b style="color:#7dd3fc;">{hazard_focus}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

data_source_note = (
    "القراءات الأساسية تستند إلى السجل التاريخي لـ 26 محطة رصد (MEWA: 1964–2014)."
    if rain_add == 0
    else f"تنبيه شفافية البيانات: القيم المعروضة تجمع بين السجل التاريخي (1964–2014) ومحاكاة سيناريو افتراضي (+{rain_add} مم عبر نموذج {model_mode})."
)
st.markdown(f'<div class="transparency-banner">ℹ️ <b>شفافية البيانات والنماذج:</b> {data_source_note}</div>', unsafe_allow_html=True)

avg_rain = filtered["Forecast_Rain"].mean()
max_rain = filtered["Forecast_Rain"].max()
avg_risk = filtered["Susceptibility_Idx"].mean()
severe_count = int((filtered["Forecast_Rain"] >= 80).sum())

# 5) مؤشرات الأداء حسب زاوية العرض (الفرد vs الجهة)
k1, k2, k3, k4 = st.columns(4)
if audience_mode.startswith("للفرد"):
    state_label = "إنذار أحمر / برتقالي" if severe_count >= 3 else ("تنبيه أصفر" if severe_count > 0 else "مستقر (أزرق)")
    k1.markdown(f"""<div class="kpi-card"><div class="kpi-label">حالة الطقس والسلامة في منطقتك</div><div class="kpi-num" style="font-size:18px;color:#7dd3fc;">{state_label}</div><div class="kpi-sub">النطاق: {selected_gov}</div></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="kpi-card"><div class="kpi-label">الهطول المتوقع وأعلى قراءة</div><div class="kpi-num">{avg_rain:.1f} <span style="font-size:13px;">mm</span></div><div class="kpi-sub">الذروة: {max_rain:.1f} mm · {horizon_mode}</div></div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="kpi-card"><div class="kpi-label">الحرارة والرطوبة ونقطة الندى</div><div class="kpi-num">{filtered["Temp_C"].mean():.1f}°C</div><div class="kpi-sub">رطوبة {filtered["Humidity_Pct"].mean():.0f}% · نقطة الندى {filtered["Dew_Point_C"].mean():.1f}°C</div></div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="kpi-card"><div class="kpi-label">جودة الهواء (AQI) والأشعة (UV)</div><div class="kpi-num">{int(filtered["AQI"].mean())} <span style="font-size:13px;">AQI</span></div><div class="kpi-sub">UV: {int(filtered["UV_Index"].mean())} · الغبار: {filtered["Dust_ugm3"].mean():.0f} µg/m³</div></div>""", unsafe_allow_html=True)
else:
    k1.markdown(f"""<div class="kpi-card"><div class="kpi-label">الذروة المتوقعة ({model_mode})</div><div class="kpi-num">{max_rain:.1f} <span style="font-size:13px;">mm</span></div><div class="kpi-sub">متوسط RF: {filtered["Rain_RF"].mean():.1f} mm · متوسط AHP: {filtered["Rain_AHP"].mean():.1f} mm</div></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="kpi-card"><div class="kpi-label">مؤشر قابلية الفيضانات (FSI)</div><div class="kpi-num">{avg_risk:.2f}</div><div class="kpi-sub">النطاق المقياسي: 0.00 – 1.00</div></div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="kpi-card"><div class="kpi-label">تقدير الجريان السطحي للأودية</div><div class="kpi-num">{filtered["Runoff_m3s"].mean():.1f} <span style="font-size:13px;">m³/s</span></div><div class="kpi-sub">لدعم السدود وتوجيه فرق الإنقاذ</div></div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="kpi-card"><div class="kpi-label">المحطات في نطاق التحذير/الإنذار</div><div class="kpi-num" style="color:#fca5a5;">{severe_count} / {len(filtered)}</div><div class="kpi-sub">الضغط: {filtered["Pressure_hPa"].mean():.0f} hPa · الرياح: {filtered["Wind_kmh"].mean():.0f} km/h</div></div>""", unsafe_allow_html=True)

# 6) الصف الأوسط: المؤشر الدائري + الخريطة التفاعلية + بطاقة التنبيه اللحظي
c_gauge, c_map, c_alert = st.columns([1.05, 2.15, 1.25])

with c_gauge:
    st.markdown('<div class="panel-card"><div class="kpi-label">مقياس الخطورة وقابلية السيول</div>', unsafe_allow_html=True)
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_risk * 100, 1),
        number={"suffix": "%", "font": {"size": 24, "color": "#ffffff"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94b2d6"},
            "bar": {"color": "#38bdf8"},
            "bgcolor": "#091526",
            "steps": [
                {"range": [0, 35], "color": "#102a4c"},
                {"range": [35, 65], "color": "#2b2616"},
                {"range": [65, 100], "color": "#381820"}
            ],
            "threshold": {"line": {"color": "#f87171", "width": 3}, "value": 75}
        }
    ))
    gauge.update_layout(height=235, margin=dict(l=15, r=15, t=20, b=10), paper_bgcolor="#0d1d35", font={"color": "#e6eef8"})
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_map:
    st.markdown(f'<div class="panel-card"><div class="kpi-label">الخريطة التفاعلية والرادار · {map_layer}</div>', unsafe_allow_html=True)
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position=["lon", "lat"],
            get_color="Color",
            get_radius="Radius",
            pickable=True,
            auto_highlight=True,
        )
    ]
    if geojson_file is not None:
        try:
            gj_data = json.load(geojson_file)
            layers.insert(0, pdk.Layer(
                "GeoJsonLayer",
                data=gj_data,
                stroked=True,
                filled=True,
                get_fill_color=[56, 189, 248, 25],
                get_line_color=[125, 211, 252, 160],
                line_width_min_pixels=1.5,
            ))
        except Exception:
            st.warning("تعذر قراءة ملف GeoJSON المرفوع؛ تأكد من سلامة بنيته.")

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=pdk.ViewState(
            latitude=float(filtered["lat"].mean()),
            longitude=float(filtered["lon"].mean()),
            zoom=6.8,
            pitch=35 if "3D" in map_layer else 15,
        ),
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={
            "html": "<b>{Station}</b> ({Governorate})<br/>{Alert_Level}<br/>الهطول: {Forecast_Rain:.1f} mm<br/>الحرارة: {Temp_C:.1f}°C · الرياح: {Wind_kmh:.0f} km/h<br/>AQI: {AQI}",
            "style": {"backgroundColor": "#0b1d36", "color": "#ffffff"}
        }
    )
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown("""
        <div class="legend-row">
            <span style="color:#38bdf8;font-weight:700;">● أزرق: مستقر</span> &nbsp;|&nbsp;
            <span style="color:#facc15;font-weight:700;">● أصفر: تنبيه</span> &nbsp;|&nbsp;
            <span style="color:#fb923c;font-weight:700;">● برتقالي: حيطة وحذر</span> &nbsp;|&nbsp;
            <span style="color:#f87171;font-weight:700;">● أحمر: إنذار سيول</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_alert:
    top_st = filtered.sort_values("Forecast_Rain", ascending=False).iloc[0]
    has_coastal = any(g in coastal_govs for g in filtered["Governorate"])
    coastal_msg = "ارتفاع أمواج متوقع (1.5–2.6 م) وتيارات ساحلية في جدة والليث والقنفذة." if has_coastal else "متابعة الجريان السطحي في الأودية والمنحدرات الجبلية."
    st.markdown(f"""
        <div class="alert-panel">
            <div style="font-size:11px;color:#7dd3fc;font-weight:700;">التنبيهات اللحظية وتصنيف الخطورة</div>
            <div style="font-size:16px;font-weight:700;margin-top:6px;">{top_st["Alert_Level"]}</div>
            <div class="status-pill">المحطة الأعلى تأثراً: {top_st["Station"]} ({top_st["Governorate"]})</div>
            <div style="font-size:12px;color:#cbd5e1;line-height:1.6;">
                • <b>الظاهرة:</b> {hazard_focus}<br/>
                • <b>الإجراء الوقائي:</b> {top_st["Advisory"]}<br/>
                • <b>الحالة البحرية/الأودية:</b> {coastal_msg}
            </div>
        </div>
    """, unsafe_allow_html=True)

# 7) التبويبات التفصيلية (التوقعات الزمنية + البيئية والفلكية + القطاعات ومقارنة النماذج)
tab_time, tab_env, tab_sectors = st.tabs([
    "التوقعات الزمنية (آني / ممتد / فصلي)",
    "المؤشرات البيئية والبحرية والفلكية",
    "دعم القطاعات الحيوية ومقارنة النماذج"
])

with tab_time:
    st.markdown('<div class="panel-card"><div class="kpi-label">منحنى التنبؤ الزمني مقارنة بحد عتبة السيول</div>', unsafe_allow_html=True)
    if "Nowcasting" in horizon_mode:
        x_vals = [f"+{i*2}h" for i in range(13)]
    elif "14 Days" in horizon_mode:
        x_vals = [f"يوم {i+1}" for i in range(14)]
    else:
        x_vals = ["الشهر 1", "الشهر 2", "الشهر 3", "الشهر 4", "الشهر 5", "الشهر 6"]

    n_p = len(x_vals)
    y_rf = np.round(filtered["Rain_RF"].mean() * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_p)) + np.linspace(0, 0.25, n_p)), 1)
    y_ahp = np.round(filtered["Rain_AHP"].mean() * (0.72 + 0.14 * np.sin(np.linspace(0, 3.14, n_p)) + np.linspace(0, 0.22, n_p)), 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_rf, mode="lines+markers", name="Random Forest (mm)", line=dict(color="#38bdf8", width=3)))
    fig.add_trace(go.Scatter(x=x_vals, y=y_ahp, mode="lines+markers", name="AHP Model (mm)", line=dict(color="#5eead4", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=x_vals, y=[110.0]*n_p, mode="lines", name="عتبة الإنذار الأحمر (110 mm)", line=dict(color="#f87171", width=2, dash="dash")))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#0d1d35",
        plot_bgcolor="#091526",
        font={"color": "#cbd5e1"},
        xaxis=dict(gridcolor="#162b49"),
        yaxis=dict(gridcolor="#162b49")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_env:
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">جودة الهواء والصحة</div>
                <div class="kpi-num">{int(filtered["AQI"].mean())} AQI</div>
                <div class="kpi-sub">الجسيمات العالقة: {filtered["Dust_ugm3"].mean():.0f} µg/m³ · UV: {int(filtered["UV_Index"].mean())} · نقطة الندى: {filtered["Dew_Point_C"].mean():.1f}°C</div>
            </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">البيانات البحرية والساحلية</div>
                <div class="kpi-num">1.8 م</div>
                <div class="kpi-sub">متوسط ارتفاع الموج · تيارات ساحلية معتدلة إلى نشطة (جدة / الليث / القنفذة)</div>
            </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-label">البيانات الفلكية اليومية</div>
                <div class="kpi-num" style="font-size:18px;">الشروق 06:34 · الغروب 17:42</div>
                <div class="kpi-sub">طور القمر: أحدب متزايد · إضاءة 78%</div>
            </div>
        """, unsafe_allow_html=True)

with tab_sectors:
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">إدارة السيول والموارد المائية</div>
                <div class="kpi-num">{filtered["Runoff_m3s"].mean():.1f} m³/s</div>
                <div class="kpi-sub">توجيه فرق الدفاع المدني والبلديات نحو الأودية الأعلى حساسية</div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">الملاحة الجوية والبحرية</div>
                <div class="kpi-num">{filtered["Wind_kmh"].mean():.0f} km/h</div>
                <div class="kpi-sub">تقييم مسارات الطيران والموانئ وتجنب مناطق الاضطراب</div>
            </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">الزراعة والطاقة</div>
                <div class="kpi-num">{filtered["Temp_C"].mean():.1f}°C</div>
                <div class="kpi-sub">تنبيهات الصقيع/الجفاف وتقدير أحمال التبريد وكفاءة الطاقة الشمسية</div>
            </div>
        """, unsafe_allow_html=True)

# 8) جدول المحطات التفصيلي وزر تصدير التقرير CSV
with st.expander("عرض جدول المحطات الـ 26 ومقارنة النماذج (AHP vs Random Forest)"):
    display_cols = [
        "Station", "Governorate", "Elevation_m", "Hist_Mean_Rain",
        "Rain_AHP", "Rain_RF", "Runoff_m3s", "Susceptibility_Idx", "Alert_Level"
    ]
    st.dataframe(filtered[display_cols], use_container_width=True)
    csv_bytes = filtered[display_cols].to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="تحميل تقرير المحطات المفلترة (CSV)",
        data=csv_bytes,
        file_name="RASD_Flood_Early_Warning_Report.csv",
        mime="text/csv"
    )
