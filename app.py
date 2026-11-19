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
            get_background_color=[255, 255, 255, 215],
            background_padding=[3, 6],
            pickable=True,
        )
    ]

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
            "html": "<b>{Station}</b> ({Governorate})<br/>{Alert_Level}<br/>القراءة: <b>{Reading_Str}</b><br/>الهطول: {Forecast_Rain:.1f} mm · الحرارة: {Temp_C:.1f}°C",
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
                <span>محاكاة الهطول: +{rain_add} مم</span>
                <span>مرتفع (إنذار سيول)</span>
            </div>
            <div style="position:relative;height:7px;border-radius:999px;background:linear-gradient(90deg,#38bdf8 0%,#facc15 45%,#fb923c 72%,#ef4444 100%);">
                <div style="position:absolute;top:-3px;left:calc({sim_pct:.1f}% - 6px);width:13px;height:13px;border-radius:50%;background:#ffffff;border:2px solid #06101e;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
