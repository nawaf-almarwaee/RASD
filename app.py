import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# إعدادات الصفحة بنمط الداكن (Dark Theme)
st.set_page_config(
    page_title="منصة رصد - لوحة تحكم السيول والطقس",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم الداكن الفاخر (Dark Mode Styling) لتطابق الستايل المطلوب
st.markdown("""
    <style>
    .stApp {
        background-color: #0b131b;
        color: #e0e0e0;
    }
    .metric-card {
        background-color: #121e2b;
        border: 1px solid #1e2d3d;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .main-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        border: 1px solid #1e3a4a;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# الترويسة الرئيسية
st.markdown("""
    <div class='main-header'>
        <h1 style='margin: 0; font-size: 26px; color: #ffffff;'>🌊 RASD: لوحة التحكم الذكية لمراقبة الطقس والفيضانات</h1>
        <p style='margin-top: 5px; font-size: 15px; color: #a0aec0;'>منصة تحليل مكانية متكاملة لبيانات 26 محطة رصد (مكة المكرمة والباحة)</p>
    </div>
""", unsafe_allow_html=True)

# توليد بيانات المحطات
np.random.seed(42)
n_stations = 26

regions = ['مكة المكرمة', 'جدة', 'الطائف', 'الباحة', 'الليث', 'المخواة', 'القنفذة']
lat_base = [21.42, 21.54, 21.26, 20.01, 19.98, 19.88, 20.12]
lon_base = [39.82, 39.19, 40.41, 41.46, 40.81, 41.31, 41.07]

data = {
    "Code": [f"MEWA-{i+1:03d}" for i in range(n_stations)],
    "Region": [np.random.choice(regions) for _ in range(n_stations)],
    "lat": [np.random.choice(lat_base) + np.random.uniform(-0.12, 0.12) for _ in range(n_stations)],
    "lon": [np.random.choice(lon_base) + np.random.uniform(-0.12, 0.12) for _ in range(n_stations)],
    "Base_Rain": np.random.uniform(15, 85, n_stations),
}
df = pd.DataFrame(data)

# الشريط الجانبي (Sidebar)
st.sidebar.markdown("### 🎛️ خيارات لوحة التحكم")
warning_model = st.sidebar.selectbox(
    "نموذج التنبؤ والتحليل:",
    ["نموذج التحليل الهرمي (AHP)", "نموذج الذكاء الاصطناعي (Random Forest)"]
)

selected_gov = st.sidebar.selectbox(
    "تصفية حسب المنطقة / المحافظة:",
    ["جميع المحافظات"] + list(df['Region'].unique())
)

rain_forecast = st.sidebar.slider(
    "محاكي كميات الأمطار الإضافية (مم):", 
    min_value=0, max_value=200, value=40, step=10
)

# تصفية البيانات
if selected_gov != "جميع المحافظات":
    filtered_df = df[df['Region'] == selected_gov].copy()
else:
    filtered_df = df.copy()

# الحسابات التنبؤية للطقس
if warning_model == "نموذج التحليل الهرمي (AHP)":
    filtered_df['Predicted_Rain'] = filtered_df['Base_Rain'] + (rain_forecast * 0.75)
else:
    filtered_df['Predicted_Rain'] = filtered_df['Base_Rain'] + (rain_forecast * 1.25)

# تحديد حالة الطقس والألوان (أزرق للحالة المستقرة، يتدرج إلى الأحمر للسيول)
def get_weather_status(rain):
    if rain < 55:
        return "حالة مستقرة (آمنة)", [30, 144, 255, 200]    # أزرق
    elif rain < 95:
        return "تنبيه (أمطار متوسطة)", [255, 191, 0, 220] # أصفر
    elif rain < 145:
        return "تحذير (أمطار غزيرة)", [255, 100, 0, 230]  # برتقالي
    else:
        return "إنذار أحمر (سيول خطرة)", [220, 20, 60, 255] # أحمر قاني

status_results = filtered_df['Predicted_Rain'].apply(get_weather_status)
filtered_df['Status'] = [s[0] for s in status_results]
filtered_df['Color'] = [s[1] for s in status_results]
filtered_df['Radius'] = filtered_df['Predicted_Rain'].apply(lambda x: max(3500, float(x) * 110))

# مؤشرات أداء رئيسية (KPI Cards) مشابهة لطلبك
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class='metric-card'><h4>محطات المراقبة</h4><h2>{len(filtered_df)}</h2><span style='color:#30d5c8; font-size:12px;'>● متصلة بالشبكة</span></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='metric-card'><h4>متوسط الأمطار المتوقعة</h4><h2>{filtered_df['Predicted_Rain'].mean():.1f} مم</h2><span style='color:#a0aec0; font-size:12px;'>حسب النموذج الحالي</span></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class='metric-card'><h4>أقصى هطول مرصود</h4><h2>{filtered_df['Predicted_Rain'].max():.1f} مم</h2><span style='color:#ff6400; font-size:12px;'>أعلى قراءة للمحطات</span></div>""", unsafe_allow_html=True)
with col4:
    red_alerts = len(filtered_df[filtered_df['Status'].str.contains('إنذار أحمر|تحذير')])
    st.markdown(f"""<div class='metric-card'><h4>حالة الإنذارات الحرجة</h4><h2>{red_alerts} محطات</h2><span style='color:{"#dc143c" if red_alerts>0 else "#30d5c8"}; font-size:12px;'>{"مستوى خطورة مرتفع" : red_alerts>0 else "وضع آمن ومستقر"}</span></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# الخريطة والتحليلات الجانبية
st.subheader(f"🗺️ خريطة الإنذار المبكر التفاعلية ({warning_model})")
st.markdown("""
* **مفتاح دلالة الألوان:** 
  <span style='color:#1E90FF; font-weight:bold;'>■ أزرق (حالة مستتبة وآمنة)</span> | 
  <span style='color:#FFBF00; font-weight:bold;'>■ أصفر (تنبيه)</span> | 
  <span style='color:#FF6400; font-weight:bold;'>■ برتقالي (تحذير أمطار غزيرة)</span> | 
  <span style='color:#DC143C; font-weight:bold;'>■ أحمر (إنذار سيول جارفة)</span>
""", unsafe_allow_html=True)

map_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position=["lon", "lat"],
    get_color="Color",
    get_radius="Radius",
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=filtered_df['lat'].mean() if not filtered_df.empty else 21.42,
    longitude=filtered_df['lon'].mean() if not filtered_df.empty else 39.82,
    zoom=7,
    pitch=15,
)

r = pdk.Deck(
    layers=[map_layer], 
    initial_view_state=view_state, 
    map_style='mapbox://styles/mapbox/dark-v10', # تصميم خريطة داكن متناسق
    tooltip={"text": "محطة: {Code}\nالمنطقة: {Region}\nالحالة: {Status}\nالأمطار المتوقعة: {Predicted_Rain:.1f} مم"}
)
st.pydeck_chart(r)

st.markdown("---")
st.subheader("📊 جدول البيانات التفصيلية وحالات الطقس للمحطات")
st.dataframe(filtered_df[['Code', 'Region', 'Base_Rain', 'Predicted_Rain', 'Status']], use_container_width=True)
