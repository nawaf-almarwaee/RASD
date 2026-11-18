import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام التنبؤ بقابلية الفيضانات - مكة والباحة",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم الواجهة والعنوان الرئيسي
st.markdown("""
    <div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 25px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin: 0; font-size: 28px;'>🌊 نظام التنبؤ الذكي بقابلية الفيضانات (منطقة مكة المكرمة والباحة)</h1>
        <p style='margin-top: 8px; font-size: 16px; opacity: 0.9;'>منصة تحليل مكانية متكاملة لبيانات 26 محطة رصد (تشمل الإحداثيات، آثار العواصف، والتحليلات طويلة الأجل)</p>
    </div>
""", unsafe_allow_html=True)

# محاكاة بيانات 26 محطة رصد (مكة المكرمة والباحة)
np.random.seed(42)
n_stations = 26

regions = ['مكة المكرمة', 'جدة', 'الطائف', 'الباحة', 'الليث', 'المخواة']
lat_base = [21.42, 21.54, 21.26, 20.01, 19.98, 19.88]
lon_base = [39.82, 39.19, 40.41, 41.46, 40.81, 41.31]

data = {
    "Code": [f"MEWA-{i+1:03d}" for i in range(n_stations)],
    "Region": [np.random.choice(regions) for _ in range(n_stations)],
    "lat": [np.random.choice(lat_base) + np.random.uniform(-0.15, 0.15) for _ in range(n_stations)],
    "lon": [np.random.choice(lon_base) + np.random.uniform(-0.15, 0.15) for _ in range(n_stations)],
    "Elev": np.random.uniform(50, 2200, n_stations),
    "Mean": np.random.uniform(30.0, 180.5, n_stations),
    "Max": np.random.uniform(120.0, 350.0, n_stations)
}
df = pd.DataFrame(data)

# الشريط الجانبي (Sidebar) للتحكم والفلاتر
st.sidebar.markdown("### 🎛️ خيارات التصفية والتحكم")

model_type = st.sidebar.selectbox(
    "نموذج التحليل الذكي:",
    ["نموذج التحليل الهرمي (AHP)", "نموذج الذكاء الاصطناعي (Random Forest)"]
)

selected_region = st.sidebar.selectbox(
    "اختر المنطقة أو المحافظة:",
    ["الكل"] + list(df['Region'].unique())
)

rain_simulation = st.sidebar.slider(
    "محاكي شدة الأمطار الإضافية (مم):", 
    min_value=0, max_value=150, value=50, step=10
)

# فلترة البيانات بناءً على اختيار المستخدم
if selected_region != "الكل":
    filtered_df = df[df['Region'] == selected_region]
else:
    filtered_df = df

# مؤشرات الأداء الرئيسية (KPIs)
c1, c2, c3, c4 = st.columns(4)
c1.metric("عدد المحطات المرصودة", f"{len(filtered_df)}")
c2.metric("متوسط هطول الأمطار العام", f"{filtered_df['Mean'].mean():.1f} مم")
c3.metric("أعلى موسم مسجل", f"{filtered_df['Max'].max():.1f} مم")
c4.metric("أقصى ارتفاع للمحطات", f"{filtered_df['Elev'].max():.0f} م")

st.markdown("---")
st.subheader(f"🗺️ الخريطة التفاُعلية لتوزيع المحطات والإحداثيات ({model_type})")

# حساب مؤشر الحساسية بناءً على النموذج المختار ومحاكي الأمطار
if model_type == "نموذج التحليل الهرمي (AHP)":
    filtered_df['Susceptibility'] = (filtered_df['Max'] + rain_simulation) / 400
else:
    filtered_df['Susceptibility'] = (filtered_df['Max'] * 1.2 + rain_simulation * 1.5) / 500

filtered_df['Susceptibility'] = filtered_df['Susceptibility'].clip(0.1, 1.0)
filtered_df['Color'] = filtered_df['Susceptibility'].apply(lambda x: [int(x * 255), int((1-x) * 200), 50, 180])

# إعداد طبقة الخريطة التفاعلية باستخدام PyDeck
map_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position=["lon", "lat"],
    get_color="Color",
    get_radius=3500,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=filtered_df['lat'].mean(),
    longitude=filtered_df['lon'].mean(),
    zoom=7,
    pitch=0,
)

r = pdk.Deck(layers=[map_layer], initial_view_state=view_state, tooltip={"text": "المحطة: {Code}\nالمنطقة: {Region}\nالارتفاع: {Elev} م\nالهطول الأقصى: {Max} مم"})
st.pydeck_chart(r)

st.markdown("---")
st.subheader("📊 جدول البيانات الإحصائية والمكانية التفصيلية")
st.dataframe(filtered_df[['Code', 'Region', 'Elev', 'Mean', 'Max']], use_container_width=True)
