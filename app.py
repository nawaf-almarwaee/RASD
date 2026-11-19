<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Flood_Dashboard — لوحة تحليل مخاطر السيول والطقس المباشر</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">

  <!-- Leaflet للخرائط التفاعلية -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <!-- D3.js للرسوم البيانية -->
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

  <style>
    :root {
      /* هوية الألوان المستوحاة من الصورة (خلفية بيضاء + أخضر زمردي داكن ونعناعي) */
      --bg-page: #f4f7f6;
      --bg-surface: #ffffff;
      --bg-soft: #f0f5f3;
      --teal-dark: #064e3b;
      --teal-mid: #0f766e;
      --mint: #10b981;
      --mint-soft: #d1fae5;
      --border: #dce5e1;
      --text-main: #0f172a;
      --text-muted: #526071;
      --alert-red: #dc2626;
      --alert-red-bg: #fef2f2;
      --alert-red-border: #fecaca;
      --warn-amber: #d97706;
      --warn-amber-bg: #fffbeb;
      --info-blue: #0284c7;
      --info-blue-bg: #f0f9ff;
      --radius: 14px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Cairo', sans-serif;
      background-color: var(--bg-page);
      color: var(--text-main);
      direction: rtl;
      text-align: right;
      line-height: 1.65;
      padding: 18px;
    }

    .container {
      max-width: 1520px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    /* شريط علوي باللون الأخضر الزمردي الداكن كما في الصورة */
    .top-header {
      background: linear-gradient(90deg, var(--teal-dark) 0%, var(--teal-mid) 100%);
      color: #ffffff;
      border-radius: var(--radius);
      padding: 14px 20px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 6px 18px rgba(6, 78, 59, 0.14);
    }

    .top-header h1 {
      font-size: 1.15rem;
      font-weight: 800;
      color: #ffffff;
    }

    .header-sub {
      font-size: 0.82rem;
      color: #d1fae5;
    }

    .meta-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 0.82rem;
    }

    .pill {
      background: rgba(255, 255, 255, 0.14);
      border: 1px solid rgba(255, 255, 255, 0.22);
      padding: 4px 11px;
      border-radius: 999px;
      color: #ecfdf5;
    }

    .pill strong {
      color: #ffffff;
    }

    /* الصف الرئيسي: لوحة التحكم بالسيناريوهات يمين + الخريطة والمؤشر يسار */
    .main-grid {
      display: grid;
      grid-template-columns: minmax(340px, 1fr) minmax(0, 1.55fr);
      gap: 18px;
      align-items: stretch;
    }

    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .section-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--teal-dark);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .sub-text {
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    /* عمود السيناريوهات */
    .scenarios-col {
      display: flex;
      flex-direction: column;
      gap: 14px;
      height: 100%;
    }

    .stats-strip {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    .mini-stat {
      background: var(--bg-soft);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
    }

    .mini-stat .val {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--teal-dark);
    }

    .scenario-btns {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }

    .sc-btn {
      background: var(--bg-soft);
      color: var(--text-main);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 8px 10px;
      font-family: 'Cairo', sans-serif;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      transition: 0.15s ease;
    }

    .sc-btn.active {
      background: var(--teal-dark);
      border-color: var(--teal-dark);
      color: #ffffff;
    }

    .alert-box {
      background: var(--alert-red-bg);
      border: 1px solid var(--alert-red-border);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }

    .badge {
      display: inline-block;
      background: var(--alert-red);
      color: #ffffff;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 3px 11px;
      border-radius: 999px;
      width: fit-content;
    }

    .alert-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 0.88rem;
      color: var(--text-main);
    }

    /* عمود الخريطة والمؤشر */
    .map-col {
      display: flex;
      flex-direction: column;
      gap: 12px;
      height: 100%;
    }

    #map {
      width: 100%;
      height: 430px;
      border-radius: 12px;
      border: 1px solid var(--border);
      z-index: 1;
    }

    .slider-panel {
      background: var(--bg-soft);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 16px;
    }

    .slider-top {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--teal-dark);
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--teal-mid);
      cursor: pointer;
    }

    /* مصفوفة الإجراءات أسفل خط المؤشر */
    .matrix-card {
      width: 100%;
    }

    .matrix-head {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      padding-bottom: 10px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }

    .matrix-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
    }

    .matrix-item {
      background: var(--bg-soft);
      border: 1px solid var(--border);
      border-right: 4px solid var(--teal-mid);
      border-radius: 12px;
      padding: 12px 14px;
    }

    .matrix-item-title {
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--teal-dark);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .tag {
      font-size: 0.74rem;
      padding: 2px 8px;
      border-radius: 6px;
      background: var(--mint-soft);
      color: var(--teal-dark);
      font-weight: 700;
    }

    /* التحليلات وجدول الطقس المباشر */
    .analytics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 18px;
    }

    .table-wrap {
      overflow-x: auto;
      margin-top: 8px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }

    th, td {
      border: 1px solid var(--border);
      padding: 8px 10px;
      text-align: center;
      white-space: nowrap;
    }

    th {
      background: var(--bg-soft);
      color: var(--teal-dark);
      font-weight: 700;
    }

    .rain-alert-cell {
      background: #fee2e2 !important;
      color: #991b1b;
      font-weight: 800;
    }

    #ahpChart {
      width: 100%;
      min-height: 220px;
    }

    @media (max-width: 1024px) {
      .main-grid {
        grid-template-columns: 1fr;
      }
      #map {
        height: 350px;
      }
    }
  </style>
</head>
<body>
  <div class="container">

    <!-- شريط علوي بالهوية الخضراء الداكنة -->
    <header class="top-header">
      <div>
        <h1>Flood_Dashboard — لوحة تحليل مخاطر السيول والطقس المباشر</h1>
        <div class="header-sub">بيانات ثابتة مدمجة (JSON) + تحديث مباشر كل 15 دقيقة عبر Open-Meteo API</div>
      </div>
      <div class="meta-pills">
        <span class="pill">مساحة الدراسة: <strong>151,288 كم²</strong></span>
        <span class="pill">محطات الأمطار: <strong>26 محطة</strong></span>
        <span class="pill">اتساق AHP: <strong>CR = 0.011</strong></span>
        <span class="pill" id="lastSyncPill">آخر تحديث للطقس: <strong>جاري الجلب...</strong></span>
      </div>
    </header>

    <!-- الصف الرئيسي: السيناريوهات بجانب الخريطة والمؤشر -->
    <div class="main-grid">

      <!-- يمين: لوحة التحكم بالسيناريوهات -->
      <aside class="card scenarios-col">
        <div class="section-title">
          <span>لوحة التحكم بالسيناريوهات</span>
          <span class="sub-text" id="scenarioCodeLabel">TA109</span>
        </div>

        <div class="stats-strip">
          <div class="mini-stat">
            <div class="sub-text">مؤشر شدة الحالة</div>
            <div class="val" id="intensityVal">84.7%</div>
          </div>
          <div class="mini-stat">
            <div class="sub-text">أرض جرداء / عمران</div>
            <div class="val">94.6% / 1.0%</div>
          </div>
        </div>

        <div class="scenario-btns">
          <button class="sc-btn active" data-sc="TA109" onclick="setScenario('TA109')">TA109 (الطائف)</button>
          <button class="sc-btn" data-sc="TA204" onclick="setScenario('TA204')">TA204 (الأودية)</button>
          <button class="sc-btn" data-sc="TA305" onclick="setScenario('TA305')">TA305 (الساحل)</button>
        </div>

        <div class="alert-box" id="alertBox">
          <span class="badge" id="alertBadge">أحمر • إنذار سيول شديد</span>
          <div style="font-weight: 800; font-size: 1rem;" id="alertTitle">المحطة: (الطائف) TA109</div>
          <ul class="alert-list" id="alertList">
            <li><strong>الحوض:</strong> مرتفعات الشفا / الطائف</li>
            <li><strong>الطقس المباشر الآن:</strong> جاري القراءة من Open-Meteo...</li>
            <li><strong>هطول اليوم المتوقع:</strong> جاري التحديث...</li>
            <li><strong>الإجراء الفوري:</strong> الحذر من جريان السيول في مجاري الأودية</li>
          </ul>
        </div>
      </aside>

      <!-- يسار: الخريطة التفاعلية + المؤشر أسفلها -->
      <section class="card map-col">
        <div class="section-title">
          <span>الخريطة التفاعلية لنطاق الهطول والمخاطر</span>
          <span class="sub-text" id="rainSummaryTop">الهطول: +85 مم (+50%)</span>
        </div>

        <div id="map"></div>

        <!-- خط المؤشر أسفل الخريطة -->
        <div class="slider-panel">
          <div class="slider-top">
            <label for="simSlider" id="simSliderLabel">مؤشر محاكاة الهطول: +85 مم (+50% • 6 س)</label>
            <span class="sub-text">العتبة الاسترشادية: ≥ 20 ملم/يوم تنبيه</span>
          </div>
          <input id="simSlider" type="range" min="10" max="100" step="0.1" value="84.7" oninput="updateSimulation(this.value)" />
        </div>
      </section>

    </div>

    <!-- مصفوفة الإجراءات أسفل خط المؤشر -->
    <section class="card matrix-card">
      <div class="matrix-head">
        <div class="section-title" style="margin-bottom: 0;">
          <span>مصفوفة الإجراءات</span>
        </div>
        <span class="badge" id="matrixBadge">أحمر • إنذار سيول شديد</span>
      </div>

      <div class="matrix-grid">
        <div class="matrix-item">
          <div class="matrix-item-title">
            <span>السيول والمياه</span>
            <span class="tag">أولوية قصوى</span>
          </div>
          <p class="sub-text">مراقبة منسوب الجريان وتصريف السدود عند الحد الآمن ومتابعة محطات الأمطار الـ26.</p>
        </div>

        <div class="matrix-item">
          <div class="matrix-item-title">
            <span>الطرق والملاحة</span>
            <span class="tag">تحذير مروري</span>
          </div>
          <p class="sub-text">تجنب المسارات المنخفضة وبطون الأودية أثناء ارتفاع الهطول أو رصد تجمع للمياه.</p>
        </div>

        <div class="matrix-item">
          <div class="matrix-item-title">
            <span>الغطاء الأرضي والتربة</span>
            <span class="tag">ESA WorldCover</span>
          </div>
          <p class="sub-text">مراعاة سرعة الجريان السطحي في الأراضي الجرداء (94.6%) مقارنة بالمناطق العمرانية (1.0%).</p>
        </div>

        <div class="matrix-item">
          <div class="matrix-item-title">
            <span>التنبيه الاسترشادي (20 ملم)</span>
            <span class="tag">استرشادي</span>
          </div>
          <p class="sub-text">تلوين خلية التوقع باللون الأحمر عند بلوغ 20 ملم أو أكثر في يوم واحد كتنبيه استرشادي غير رسمي.</p>
        </div>
      </div>
    </section>

    <!-- التحليلات الثابتة (D3.js) + توقعات الطقس المباشرة لـ 7 أيام -->
    <section class="analytics-grid">
      <div class="card">
        <div class="section-title">
          <span>أوزان معايير AHP (CR = 0.011)</span>
          <span class="sub-text">رسم بياني عبر D3.js</span>
        </div>
        <div id="ahpChart"></div>
      </div>

      <div class="card">
        <div class="section-title">
          <span>الطقس المباشر وتوقعات 7 أيام (Open-Meteo)</span>
          <span class="sub-text">تنبيه أحمر عند ≥ 20 ملم/يوم</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>المدينة</th>
                <th>الحالة الآن</th>
                <th>الحرارة</th>
                <th>الرطوبة</th>
                <th>الرياح</th>
                <th>اليوم (ملم)</th>
                <th>أقصى توقع 7 أيام</th>
              </tr>
            </thead>
            <tbody id="weatherTableBody">
              <tr><td colspan="7">جاري تحميل بيانات الطقس المباشرة...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

  </div>

  <script>
    const STATIC_PROJECT_DATA = {
      studyAreaKm2: 151288,
      rainStationsCount: 26,
      landCover: { bareSoilPct: 94.6, builtUpPct: 1.0 },
      ahpConsistencyRatio: 0.011,
      rainThresholdMm: 20,
      ahpWeights: [
        { criterion: "شدة وهطول الأمطار", weight: 0.38 },
        { criterion: "الانحدار والطبوغرافيا", weight: 0.27 },
        { criterion: "الغطاء الأرضي (WorldCover)", weight: 0.19 },
        { criterion: "كثافة شبكة التصريف", weight: 0.16 }
      ],
      scenarios: {
        TA109: {
          code: "TA109",
          station: "المحطة: (الطائف) TA109",
          basin: "مرتفعات الشفا / الطائف",
          cityKey: "taif",
          lat: 21.27,
          lng: 40.41,
          defaultPct: 84.7
        },
        TA204: {
          code: "TA204",
          station: "المحطة: (بيشة / الأودية) TA204",
          basin: "حوض الأودية الجنوبية",
          cityKey: "bishah",
          lat: 19.99,
          lng: 42.60,
          defaultPct: 68.0
        },
        TA305: {
          code: "TA305",
          station: "المحطة: (جدة / الساحل) TA305",
          basin: "السهول الساحلية الغربية",
          cityKey: "jeddah",
          lat: 21.54,
          lng: 39.17,
          defaultPct: 52.0
        }
      },
      cities: [
        { key: "taif", name: "الطائف", lat: 21.2703, lon: 40.4158 },
        { key: "makkah", name: "مكة المكرمة", lat: 21.3891, lon: 39.8579 },
        { key: "jeddah", name: "جدة", lat: 21.5433, lon: 39.1728 },
        { key: "bishah", name: "بيشة", lat: 20.0006, lon: 42.5994 },
        { key: "abha", name: "أبها", lat: 18.2164, lon: 42.5053 }
      ]
    };

    let activeScenario = "TA109";
    let liveWeatherMap = {};

    // خريطة فاتحة متناسقة مع الخلفية البيضاء والهوية الخضراء
    const map = L.map("map").setView([21.27, 40.41], 7);
    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      attribution: "&copy; OpenStreetMap &copy; CARTO",
      maxZoom: 18
    }).addTo(map);

    const hazardCircle = L.circle([21.27, 40.41], {
      color: "#0f766e",
      fillColor: "#10b981",
      fillOpacity: 0.25,
      radius: 45000
    }).addTo(map);

    const stationMarker = L.marker([21.27, 40.41]).addTo(map);

    function renderAhpChart() {
      const container = d3.select("#ahpChart");
      container.selectAll("*").remove();

      const width = container.node().clientWidth || 420;
      const height = 220;
      const margin = { top: 14, right: 20, bottom: 28, left: 150 };

      const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height);

      const x = d3.scaleLinear()
        .domain([0, 0.45])
        .range([0, width - margin.left - margin.right]);

      const y = d3.scaleBand()
        .domain(STATIC_PROJECT_DATA.ahpWeights.map(d => d.criterion))
        .range([margin.top, height - margin.bottom])
        .padding(0.28);

      const g = svg.append("g")
        .attr("transform", `translate(${margin.left}, 0)`);

      g.selectAll("rect")
        .data(STATIC_PROJECT_DATA.ahpWeights)
        .enter()
        .append("rect")
        .attr("x", 0)
        .attr("y", d => y(d.criterion))
        .attr("width", d => x(d.weight))
        .attr("height", y.bandwidth())
        .attr("rx", 6)
        .attr("fill", "#0f766e");

      g.selectAll(".bar-label")
        .data(STATIC_PROJECT_DATA.ahpWeights)
        .enter()
        .append("text")
        .attr("class", "bar-label")
        .attr("x", d => x(d.weight) + 6)
        .attr("y", d => y(d.criterion) + y.bandwidth() / 2 + 4)
        .attr("fill", "#064e3b")
        .attr("font-size", "12px")
        .attr("font-weight", "700")
        .text(d => `${(d.weight * 100).toFixed(0)}%`);

      svg.append("g")
        .attr("transform", `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(y).tickSize(0))
        .selectAll("text")
        .attr("fill", "#0f172a")
        .attr("font-family", "Cairo, sans-serif")
        .attr("font-size", "12px")
        .attr("dx", "-6");

      svg.selectAll(".domain, .tick line").attr("stroke", "#cbd5e1");
    }

    function describeWeatherCode(code) {
      if (code === 0) return "صحو";
      if ([1, 2, 3].includes(code)) return "غائم جزئياً / غائم";
      if ([45, 48].includes(code)) return "ضباب";
      if ([51, 53, 55, 56, 57].includes(code)) return "رذاذ";
      if ([61, 63, 65, 80, 81, 82].includes(code)) return "أمطار / زخات";
      if ([95, 96, 99].includes(code)) return "عواصف رعدية";
      return "متقلب";
    }

    async function fetchLiveWeather() {
      const rows = [];
      for (const city of STATIC_PROJECT_DATA.cities) {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${city.lat}&longitude=${city.lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&daily=precipitation_sum&timezone=auto&forecast_days=7`;
        try {
          const res = await fetch(url);
          const data = await res.json();
          const cur = data.current || {};
          const dailyRain = data.daily?.precipitation_sum || [];
          const todayRain = Number(dailyRain[0] ?? 0);
          const max7Rain = dailyRain.length ? Math.max(...dailyRain.map(Number)) : 0;

          const item = {
            name: city.name,
            condition: describeWeatherCode(cur.weather_code),
            temp: cur.temperature_2m !== undefined ? `${cur.temperature_2m}°C` : "-",
            humidity: cur.relative_humidity_2m !== undefined ? `${cur.relative_humidity_2m}%` : "-",
            wind: cur.wind_speed_10m !== undefined ? `${cur.wind_speed_10m} كم/س` : "-",
            todayRain,
            max7Rain
          };
          liveWeatherMap[city.key] = item;
          rows.push(item);
        } catch (err) {
          rows.push({
            name: city.name,
            condition: "تعذر الجلب",
            temp: "-",
            humidity: "-",
            wind: "-",
            todayRain: 0,
            max7Rain: 0
          });
        }
      }

      const tbody = document.getElementById("weatherTableBody");
      tbody.innerHTML = rows.map(r => {
        const todayAlert = r.todayRain >= STATIC_PROJECT_DATA.rainThresholdMm ? "rain-alert-cell" : "";
        const weekAlert = r.max7Rain >= STATIC_PROJECT_DATA.rainThresholdMm ? "rain-alert-cell" : "";
        return `
          <tr>
            <td><strong>${r.name}</strong></td>
            <td>${r.condition}</td>
            <td>${r.temp}</td>
            <td>${r.humidity}</td>
            <td>${r.wind}</td>
            <td class="${todayAlert}">${r.todayRain.toFixed(1)}</td>
            <td class="${weekAlert}">${r.max7Rain.toFixed(1)}</td>
          </tr>
        `;
      }).join("");

      const nowStr = new Date().toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" });
      document.getElementById("lastSyncPill").innerHTML = `آخر تحديث للطقس: <strong>${nowStr}</strong>`;
      refreshScenarioCard();
    }

    function setScenario(code) {
      activeScenario = code;
      document.querySelectorAll(".sc-btn").forEach(b => b.classList.toggle("active", b.dataset.sc === code));
      const sc = STATIC_PROJECT_DATA.scenarios[code];
      map.setView([sc.lat, sc.lng], 8);
      hazardCircle.setLatLng([sc.lat, sc.lng]);
      stationMarker.setLatLng([sc.lat, sc.lng]).bindPopup(`${sc.code} - ${sc.basin}`).openPopup();

      const slider = document.getElementById("simSlider");
      slider.value = sc.defaultPct;
      updateSimulation(sc.defaultPct);
    }

    function refreshScenarioCard() {
      const sc = STATIC_PROJECT_DATA.scenarios[activeScenario];
      const w = liveWeatherMap[sc.cityKey];
      document.getElementById("scenarioCodeLabel").textContent = sc.code;
      document.getElementById("alertTitle").textContent = sc.station;
      document.getElementById("alertList").innerHTML = `
        <li><strong>الحوض:</strong> ${sc.basin}</li>
        <li><strong>الطقس المباشر الآن:</strong> ${w ? `${w.condition} (${w.temp})` : "جاري القراءة..."}</li>
        <li><strong>هطول اليوم المتوقع:</strong> ${w ? `${w.todayRain.toFixed(1)} ملم` : "جاري التحديث..."}</li>
        <li><strong>الإجراء الفوري:</strong> الحذر من جريان السيول في مجاري الأودية</li>
      `;
    }

    function updateSimulation(val) {
      const pct = parseFloat(val);
      const mm = Math.round((pct / 100) * 100);
      document.getElementById("intensityVal").textContent = `${pct.toFixed(1)}%`;
      document.getElementById("rainSummaryTop").textContent = `الهطول: +${mm} مم (+${Math.round(pct * 0.6)}%)`;
      document.getElementById("simSliderLabel").textContent =
        `مؤشر محاكاة الهطول: +${mm} مم (+${Math.round(pct * 0.6)}% • 6 س)`;

      const badge = document.getElementById("alertBadge");
      const mBadge = document.getElementById("matrixBadge");
      const alertBox = document.getElementById("alertBox");

      if (pct >= 75) {
        badge.textContent = "أحمر • إنذار سيول شديد";
        mBadge.textContent = "أحمر • إنذار سيول شديد";
        badge.style.background = "#dc2626";
        mBadge.style.background = "#dc2626";
        alertBox.style.background = "#fef2f2";
        alertBox.style.borderColor = "#fecaca";
        hazardCircle.setStyle({ color: "#dc2626", fillColor: "#ef4444" });
      } else if (pct >= 45) {
        badge.textContent = "برتقالي • حيطة وحذر";
        mBadge.textContent = "برتقالي • حيطة وحذر";
        badge.style.background = "#d97706";
        mBadge.style.background = "#d97706";
        alertBox.style.background = "#fffbeb";
        alertBox.style.borderColor = "#fde68a";
        hazardCircle.setStyle({ color: "#d97706", fillColor: "#f59e0b" });
      } else {
        badge.textContent = "أخضر زمردي • متابعة أمطار";
        mBadge.textContent = "أخضر زمردي • متابعة أمطار";
        badge.style.background = "#0f766e";
        mBadge.style.background = "#0f766e";
        alertBox.style.background = "#f0fdf4";
        alertBox.style.borderColor = "#bbf7d0";
        hazardCircle.setStyle({ color: "#0f766e", fillColor: "#10b981" });
      }

      hazardCircle.setRadius(15000 + pct * 550);
      refreshScenarioCard();
    }

    renderAhpChart();
    updateSimulation(84.7);
    fetchLiveWeather();
    setInterval(fetchLiveWeather, 15 * 60 * 1000);
    window.addEventListener("resize", renderAhpChart);
  </script>
</body>
</html>
