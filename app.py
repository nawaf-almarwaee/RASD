import streamlit as st
import pandas as pd
import numpy as np

# إعدادات الصفحة بنمط الداكن (Dark Mode)
st.set_page_config(
    page_title="RASD Dashboard - لوحة التحكم الهندسية",
    page_icon="🌊",
    layout="wide"
)

# تخصيص التصميم الداكن الفاخر المطابق لستايل منصة ثروة الهندسية
st.markdown("""
    <style>
    .stApp {
        background-color: #0b131b;
        color: #e0e0e0;
    }
    /* الشريط العلوي الاحترافي */
    .top-nav {
        background: #0f1c24;
        border: 1px solid #192a38;
        padding: 15px 25px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .top-nav h3 {
        color: #30d5c8;
        margin: 0;
        font-size: 20px;
        font-weight: 600;
    }
    .nav-links span {
        margin-left: 20px;
        color: #8899a6;
        font-size: 14px;
        cursor: pointer;
    }
    .nav-links span.active {
        color: #ffffff;
        font-weight: bold;
        border-bottom: 2px solid #30d5c8;
        padding-bottom: 4px;
    }
    /* كروت المؤشرات العلوية */
    .kpi-box {
        background-color: #121e2b;
        border: 1px solid #1a2c3d;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .kpi-title {
        color: #8899a6;
        font-size: 13px;
        margin-bottom: 5px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
    }
    .kpi-sub {
        color: #30d5c8;
        font-size: 11px;
        margin-top: 5px;
    }
    /* بطاقة كشف الحالات والإنذار */
    .alert-box {
        background-color: #0f2422;
        border: 1px solid #163d38;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط العلوي للمنصة (Top Navbar)
st.markdown("""
    <div class='top-nav'>
        <div>
            <h3>🌊 THARWA / RASD PLATFORM</h3>
        </div>
        <div class='nav-links'>
            <span class='active'>Overview</span>
            <span>Trends</span>
            <span>Assets</span>
            <span>Settings</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# الشريط الجانبي للتحكم والمحاكاة
st.sidebar.markdown("### 🎛️ إعدادات النموذج والمحاكاة")
model_choice = st.sidebar.selectbox("نموذج التحليل الذكي:", ["نموذج التحليل الهرمي (AHP)", "نموذج الذكاء الاصطناعي (Random Forest)"])
rain_sim = st.sidebar.slider("محاكي شدة الأمطار الإضافية (مم):", 0, 150, 45, 5)

# صف المؤشرات العلوي (4 كروت متجاورة تماماً مثل الصورة)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class='kpi-box'>
            <div class='kpi-title'>1 Model prediction</div>
            <div class='kpi-value'>1,394 <span style='font-size:13px; color:#8899a6;'>mm/L</span></div>
            <div class='kpi-sub'>Model estimate (AHP/RF)</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>🌡️ Water Temperature</div>
            <div class='kpi-value'>{42.0 + (rain_sim*0.02):.1f} °C</div>
            <div class='kpi-sub'>Sensor reading</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>⚡ Flow Velocity (EC)</div>
            <div class='kpi-value'>{2.0 + (rain_sim*0.01):.1f} <span style='font-size:13px; color:#8899a6;'>m/s</span></div>
            <div class='kpi-sub'>Sensor reading</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    status_text = "Within limit" if rain_sim < 90 else "Critical Alert"
    status_color = "#30d5c8" if rain_sim < 90 else "#ff4d4d"
    st.markdown(f"""
        <div class='kpi-box'>
            <div class='kpi-title'>📍 Threshold Status</div>
            <div class='kpi-value' style='color:{status_color};'>{status_text}</div>
            <div class='kpi-sub'>Based on model estimate</div>
        </div>
    """, unsafe_allow_html=True)

# الصف الثاني: قسم التحليل المكاني والذكاء الاصطناعي للكشف عن الحالات
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
        <div class='kpi-box'>
            <h4 style='color:#ffffff; margin-top:0; font-size:16px;'>🗺️ Flood & Watershed Intelligence / 3D View</h4>
            <p style='color:#8899a6; font-size:13px;'>تحليل النطاق الجغرافي لمحطات مكة المكرمة والباحة (26 محطة رصد)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # محاكاة خريطة البيانات عبر جدول هندسي تفصيلي متناسق مع الستايل الداكن
    np.random.seed(42)
    stations_data = pd.DataFrame({
        "Station Code": [f"MEWA-{i+1:03d}" for i in range(5)],
        "Region": ["مكة المكرمة", "جدة", "الطائف", "الباحة", "الليث"],
        "Rainfall (mm)": [45.2 + rain_sim, 88.5 + rain_sim*1.2, 112.0 + rain_sim*1.5, 34.0 + rain_sim, 95.0 + rain_sim],
        "Status": ["Stable", "Warning", "Critical Alert", "Stable", "Warning"]
    })
    st.dataframe(stations_data, use_container_width=True)

with col_right:
    st.markdown("""
        <div class='alert-box'>
            <div style='color:#30d5c8; font-size:12px; font-weight:bold;'>2 Anomaly result</div>
            <h4 style='color:#ffffff; margin-top:5px; font-size:16px;'>🟢 Normal & Monitored</h4>
            <p style='color:#8899a6; font-size:12px; line-height:1.5;'>Current sensor data is consistent with expected hydrological patterns.</p>
            <hr style='border-color: #1a3d38; margin: 12px 0;'>
            <div style='color:#8899a6; font-size:11px;'>Leak/Spill status: <b>Active Monitoring</b></div>
            <div style='color:#30d5c8; font-size:11px; margin-top:5px;'>Model active: <b>{}</b></div>
        </div>
    """.format(model_choice), unsafe_allow_html=True)

# الصف الثالث: الرسم البياني الزمني المتطور (Time-series chart)
st.markdown("""
    <div class='kpi-box'>
        <h4 style='color:#ffffff; margin-top:0; font-size:16px;'>📈 Prediction History Over Time (سجل التنبؤات والتدفقات الزمنية)</h4>
    </div>
""", unsafe_allow_html=True)

# توليد رسم بياني زمني تفاعلي باستخدام Streamlit
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * [10, 50] + [500, 1000 + rain_sim * 2],
    columns=['Historical Avg', 'Predicted Model Flow']
)
st.line_chart(chart_data, color=["#30d5c8", "#ff6b6b"])
