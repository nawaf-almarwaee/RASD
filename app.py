import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# إعدادات الواجهة الرئيسية
st.set_page_config(
    page_title="نظام الإنذار المبكر للسيول - رصد",
    page_icon="🚨",
    layout="wide"
)

# ترويسة المنصة الرسمية
st.markdown("""
    <div style='background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 25px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin: 0; font-size: 28px;'>🚨 منصة رصد: نظام الإنذار المبكر لحالة الطقس وقابلية الفيضانات</h1>
        <p style='margin-top: 8px; font-size: 16px; opacity: 0.9;'>تتبع آلي وتنبؤي لحالة المحطات (مكة المكرمة والباحة) - الألوان تتغير ديناميكياً حسب مستويات الخطورة</p>
    </div>
""", unsafe_allow_html=True)

# توليد بيانات المحطات الـ 26 للطقس والتنبؤ
np.random.seed(100)
n_stations = 26

regions = ['مكة المكرمة', 'جدة', 'الطائف', 'الباحة', 'الليث', 'المخواة', 'القنفذة']
lat_base = [21.42, 21.54, 21.26, 20.01, 19.98, 19.88, 20.12]
lon_base = [39.82, 39.19, 40.41, 41.46, 40.81, 41.31, 41.07]

data = {
    "Code": [f"MEWA-{i+1:03d}" for i in range(n_stations)],
    "Region": [np.random.choice(regions) for _ in range(n_stations)],
    "lat": [np.random.choice(lat_base) + np.random.uniform(-0.12, 0.12) for _ in range(n_stations)],
    "lon": [np.random.choice(lon_base) + np.random.uniform(-0.12, 0.12) for _ in range(n_stations)],
    "Base_Rain": np.random.uniform(10, 90, n_stations),
}
df = pd.DataFrame(data)

# الشريط الجانبي للتحكم بنماذج الطقس والتنبؤ
st.sidebar.markdown("### ⚙️ لوحة التحكم والإنذار المبكر")

warning_model = st.sidebar.selectbox(
    "نموذج التنبؤ والتحليل:",
    ["نموذج التحليل الهرمي (AHP)", "نموذج الذكاء الاصطناعي (Random Forest)"]
)

selected_gov = st.sidebar.selectbox(
    "تصفية حسب المحافظة:",
    ["جميع المحافظات"] + list(df['Region'].unique())
)

# محاكي التنبؤ بالطقس الإضافي (كمية الأمطار المتوقعة)
rain_forecast = st.sidebar.slider(
    "محاكي توقعات الأمطار الإضافية (مم):", 
    min_value=0, max_value=200, value=30, step=10
)

# فلترة البيانات
if selected_gov != "جميع المحافظات":
    filtered_df = df[df['Region'] == selected_gov].copy()
else:
    filtered_df = df.copy()

# حساب مؤشر الطقس والخطورة المتوقع
if warning_model == "نموذج التحليل الهرمي (AHP)":
    filtered_df['Predicted_Rain'] = filtered_df['Base_Rain'] + (rain_forecast * 0.8)
else:
    filtered_df['Predicted_Rain'] = filtered_df['Base_Rain'] + (rain_forecast * 1.3)

# دالة لتحديد الألوان وحالة الطقس والإنذار بناءً على كمية الأمطار المتوقعة
def get_weather_status(rain):
    if rain < 50:
        return "مستقرة (آمنة)", [30, 144, 255, 200]    # أزرق (حالة مستتبة)
    elif rain < 90:
        return "تنبيه (أمطار متوسطة)", [255, 191, 0, 220] # أصفر (حذر)
    elif rain < 140:
        return "تحذير (أمطار غزيرة)", [255, 100, 0, 230]  # برتقالي (خطورة عالية)
    else:
        return "إنذار أحمر (سيول جارفة)", [220, 20, 60, 255] # أحمر قاني (خطر جداً)

status_results = filtered_df['Predicted_Rain'].apply(get_weather_status)
filtered_df['Status'] = [s[0] for s in status_results]
filtered_df['Color'] = [s[1] for s in status_results]
# حجم الدائرة يكبر كلما زادت كمية الأمطار المتوقعة
filtered_df['Radius'] = filtered_df['Predicted_Rain'].apply(lambda x: max(3000, float(x) * 120))

# مؤشرات حالة الطقس العامة
col1, col2, col3, col4 = st.columns(4)
col1.metric("المحطات المراقبَة", f"{len(filtered_df)}")
col2.metric("متوسط الأمطار المتوقعة", f"{filtered_df['Predicted_Rain'].mean():.1f} مم")
col3.metric("أقصى هطول متوقع", f"{filtered_df['Predicted_Rain'].max():.1f} مم")
red_alerts = len(filtered_df[filtered_df['Status'].str.contains('إنذار أحمر|تحذير')])
col4.metric("عدد محطات الإنذار والتحذير", f"{red_alerts}", delta="حالة حرجة" if red_alerts > 0 else "آمن", delta_color="inverse")

st.markdown("---")
st.subheader(f"🗺️ خريطة الإنذار المبكر للطقس والسيول ({warning_model})")
st.markdown("""
* **دلالة الألوان على الخريطة:** 
  <span style='color:#1E90FF; font-weight:bold;'>■ أزرق (حالة مستتبة وآمنة)</span> | 
  <span style='color:#FFBF00; font-weight:bold;'>■ أصفر (تنبيه)</span> | 
  <span style='color:#FF6400; font-weight:bold;'>■ برتقالي (تحذير أمطار غزيرة)</span> | 
  <span style='color:#DC143C; font-weight:bold;'>■ أحمر (إنذار سيول جارفة)</span>
""", unsafe_allow_html=True)

# إعداد خريطة PyDeck
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
    pitch=20,
)

r = pdk.Deck(
    layers=[map_layer], 
    initial_view_state=view_state, 
    tooltip={
        "text": "محطة رقم: {Code}\nالمنطقة: {Region}\nحالة الطقس: {Status}\nكمية الأمطار المتوقعة: {Predicted_Rain:.1f} مم"
    }
)
st.pydeck_chart(r)

st.markdown("---")
st.subheader("📋 جدول تفاصيل محطات الإنذار وحالة الطقس اللحظية")
st.dataframe(filtered_df[['Code', 'Region', 'Base_Rain', 'Predicted_Rain', 'Status']], use_container_width=True)
