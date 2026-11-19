if "AQI" in map_layer:
    pos_pct = min(max((avg_aqi / 220.0) * 100.0, 4.0), 96.0)
    bar_grad = "linear-gradient(90deg,#38bdf8 0%,#a3e635 30%,#facc15 55%,#fb923c 78%,#dc2626 100%)"
    scale_mid = f"مؤشر جودة الهواء الفعلي: {avg_aqi} AQI ({pos_pct:.0f}%)"
    leg_html = """
        <span style="color:#38bdf8;font-weight:700;">■ هواء جيد/مقبول</span>
        <span style="color:#facc15;font-weight:700;">■ متوسط/غبار خفيف</span>
        <span style="color:#fb923c;font-weight:700;">■ غير صحي للفئات الحساسة</span>
        <span style="color:#f87171;font-weight:700;">■ مرتفع / إنذار بيئي</span>
    """
else:
    pos_pct = min(max((rain_add / 180.0) * 100.0, 4.0), 96.0)
    bar_grad = "linear-gradient(90deg,#bae6fd 0%,#38bdf8 30%,#1d4ed8 60%,#fb923c 82%,#ef4444 100%)"
    scale_mid = f"مؤشر محاكاة الهطول: +{rain_add} مم ({pct_boost:+d}% · {storm_hours} س) · {pos_pct:.0f}%"
    leg_html = """
        <span style="color:#7dd3fc;font-weight:700;">■ أزرق فاتح/متوسط: هطول منخفض إلى متوسط</span>
        <span style="color:#3b82f6;font-weight:700;">■ أزرق داكن: مرتفعات وهطول أعلى</span>
        <span style="color:#fb923c;font-weight:700;">■ برتقالي: حيطة وحذر</span>
        <span style="color:#f87171;font-weight:700;">■ أحمر: إنذار سيول شديد</span>
    """

st.markdown(f"""
    <div class="legend-strip">{leg_html}</div>
    <div style="margin-top:10px;background:#081426;border:1px solid #1e3a60;border-radius:8px;padding:12px 14px;">
        <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;margin-bottom:10px;font-weight:600;">
            <span>0 (منخفض)</span>
            <span style="color:#7dd3fc;">{scale_mid}</span>
            <span>100% (ذروة)</span>
        </div>
        <div style="position:relative;width:100%;height:12px;border-radius:999px;background:{bar_grad};">
            <div style="position:absolute;top:50%;left:{pos_pct:.1f}%;transform:translate(-50%,-50%);width:22px;height:22px;border-radius:50%;background:#ffffff;border:3px solid #0f172a;box-shadow:0 0 8px rgba(255,255,255,0.95);z-index:5;"></div>
        </div>
    </div>
""", unsafe_allow_html=True)
