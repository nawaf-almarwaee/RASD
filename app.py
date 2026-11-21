<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>لوحة مشروع قابلية الفيضانات</title>
<style>
:root{--bg:#f6f5f1;--panel:#ffffff;--fg:#1d1d1b;--muted:#6b6a64;--line:#e3e1da;--accent:#2a78d6;--accent2:#e3872d;--accent3:#1f9e74;--ok:#1f8a5b;--warn:#c27a12;--bad:#c0392b;--chip:#eef3fb;--grid:#ecebe6}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--panel:#1f1f1d;--fg:#ecebe6;--muted:#a3a19a;--line:#33322f;--accent:#5b9ef0;--accent2:#f0a052;--accent3:#3cc39a;--ok:#41b883;--warn:#e0a03a;--bad:#e5675a;--chip:#22303f;--grid:#2a2a28}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Segoe UI",Tahoma,"Noto Naskh Arabic",Arial,sans-serif;line-height:1.5}
.wrap{max-width:1280px;margin:0 auto;padding:24px 20px 48px}
header h1{font-size:28px;margin:0 0 4px;font-weight:700}
header .sub{color:var(--muted);margin:0 0 10px}
header .lead{font-size:17px;margin:0 0 20px}
h2{font-size:18px;margin:0 0 4px}
.note{color:var(--muted);font-size:13px;margin:0 0 10px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:16px}
.tile .k{color:var(--muted);font-size:13px}.tile .v{font-size:30px;font-weight:600;font-variant-numeric:tabular-nums;margin-top:4px}.tile .u{color:var(--muted);font-size:12px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:16px;margin-bottom:16px}
section.card{margin-bottom:16px}
.wx-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.btn{font:inherit;font-size:13px;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:5px 14px;cursor:pointer}
.btn:hover{border-color:var(--accent)}
.wx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(135px,1fr));gap:12px;margin-top:12px}
.wx{border:1px solid var(--line);border-radius:10px;padding:12px;position:relative}
.wx .city{font-weight:600}.wx .t{font-size:28px;font-weight:600;font-variant-numeric:tabular-nums}.wx .d{color:var(--muted);font-size:13px}
.wx .row{display:flex;flex-direction:column;font-size:12px;color:var(--muted);margin-top:4px;white-space:nowrap}
.wx.alert{border-color:var(--bad);box-shadow:0 0 0 1px var(--bad) inset}
.badge{display:inline-block;white-space:nowrap;font-size:11px;border-radius:999px;padding:1px 8px;border:1px solid currentColor}
.badge.bad{color:var(--bad)}.badge.warn{color:var(--warn)}.badge.ok{color:var(--ok)}
.wx-status{font-size:13px;color:var(--muted)}
.fc{margin-top:16px}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:right;color:var(--muted);font-weight:600;font-size:12px;padding:6px 8px;border-bottom:1px solid var(--line)}
td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.tablewrap{overflow-x:auto}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;white-space:nowrap;border:1px solid currentColor}
.pill.ok{color:var(--ok)}.pill.warn{color:var(--warn)}.pill.todo{color:var(--muted)}
.chart{position:relative;min-height:200px}
.map{position:relative;min-height:380px}
.tip{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--line);box-shadow:0 6px 18px rgba(0,0,0,.15);border-radius:8px;padding:6px 9px;font-size:12px;line-height:1.5;white-space:nowrap;z-index:5}
.tip .m{color:var(--muted)}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:12px;color:var(--muted);margin-top:6px}
.sw{display:inline-block;width:10px;height:10px;border-radius:50%;margin-left:6px;vertical-align:middle}
.sq{display:inline-block;width:12px;height:12px;border-radius:2px;margin-left:6px;vertical-align:middle}
.ahp-row{display:grid;grid-template-columns:minmax(120px,160px) 1fr 56px;align-items:center;gap:10px;padding:4px 0}
.ahp-row .grp{display:block;color:var(--muted);font-size:11px}
.track{position:relative;height:22px}
.base{position:absolute;top:3px;height:16px;right:0;background:var(--line);border-radius:0 3px 3px 0}
.adj{position:absolute;top:7px;height:8px;right:0;border-radius:0 3px 3px 0;background:var(--accent)}
.ahp-row input[type=range]{width:100%;margin:2px 0 0;accent-color:var(--accent)}
.val{font-variant-numeric:tabular-nums;text-align:left;direction:ltr}
select{font:inherit;font-size:13px;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:4px 10px}
.ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.placeholder{border:1px dashed var(--line);border-radius:10px;padding:18px;color:var(--muted);text-align:center;line-height:1.9}
svg{direction:ltr}
svg text{font-family:inherit}
.axis text{fill:var(--muted);font-size:11px}.axis path,.axis line{stroke:var(--line)}.grid line{stroke:var(--grid)}.grid path{display:none}
footer{color:var(--muted);font-size:12px;margin-top:20px;line-height:1.8}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>لوحة مشروع قابلية الفيضانات</h1>
  <p class="sub">منطقة مكة المكرمة والباحة — نظم المعلومات الجغرافية وطريقة التحليل الهرمي (AHP)</p>
  <p class="lead" id="lead">—</p>
</header>

<div class="tiles">
  <div class="card tile"><div class="k">مساحة منطقة الدراسة</div><div class="v" id="kArea">—</div><div class="u">كم² (مكة المكرمة + الباحة)</div></div>
  <div class="card tile"><div class="k">محطات الأمطار</div><div class="v" id="kSt">—</div><div class="u">محطة لوزارة البيئة والمياه والزراعة</div></div>
  <div class="card tile"><div class="k">نسبة الاتساق (CR)</div><div class="v" id="kCR">—</div><div class="u">مقبولة إذا كانت أقل من 0.10</div></div>
  <div class="card tile"><div class="k">الأرض الجرداء</div><div class="v" id="kBare">—</div><div class="u">% من مساحة منطقة مكة</div></div>
  <div class="card tile"><div class="k">العمران</div><div class="v" id="kBuilt">—</div><div class="u">% من مساحة منطقة مكة</div></div>
</div>

<section class="card" id="weather">
  <div class="wx-head">
    <div><h2>الطقس الآن</h2><p class="note" style="margin:0">بيانات مباشرة من Open-Meteo، وتتحدّث تلقائياً كل 15 دقيقة.</p></div>
    <div style="display:flex;gap:10px;align-items:center"><span class="wx-status" id="wxStatus">جارٍ التحميل…</span><button class="btn" id="wxRefresh" type="button">تحديث</button></div>
  </div>
  <div class="wx-grid" id="wxGrid"></div>
  <div class="fc">
    <h2 style="font-size:15px">توقعات الأمطار للأيام السبعة القادمة (ملم/يوم)</h2>
    <p class="note">تظهر الخلية باللون الأحمر عند توقع 20 ملم أو أكثر في يوم واحد، وهذه عتبة استرشادية للتنبيه وليست تحذيراً رسمياً. للتحذيرات الرسمية: المركز الوطني للأرصاد.</p>
    <div class="tablewrap"><table id="fcTable"></table></div>
  </div>
</section>

<section class="card" id="progress">
  <h2>تقدّم المشروع</h2>
  <p class="note">حالة كل جزء من العمل العملي والنظري.</p>
  <div class="tablewrap"><table><thead><tr><th>المكوّن</th><th>الحالة</th><th>ملاحظات</th></tr></thead><tbody id="progRows"></tbody></table></div>
</section>

<div class="grid2">
  <section class="card">
    <h2>منطقة الدراسة ومحطات الأمطار</h2>
    <p class="note">حجم الدائرة يمثّل المعدل السنوي للأمطار في المحطة. مرّر المؤشر على المحطة لعرض بياناتها.</p>
    <div class="map" id="map"></div>
    <div class="legend"><span><i class="sq" style="background:var(--panel);border:1.5px solid var(--fg)"></i>مكة المكرمة</span><span><i class="sq" style="background:var(--line)"></i>الباحة</span><span><i class="sw" style="background:var(--fg)"></i>مدينة</span><span><i class="sw" style="background:var(--accent)"></i>محطة أمطار</span></div>
  </section>
  <section class="card">
    <h2>أوزان العوامل (AHP)</h2>
    <p class="note">الشريط الرمادي هو الوزن الأصلي من مصفوفة المقارنات. حرّك المؤشر لتغيير أهمية أي عامل، وتُعاد معايرة الأوزان بحيث يبقى مجموعها 100%.</p>
    <div class="ctl"><button class="btn" id="ahpReset" type="button">إعادة الأوزان الأصلية</button></div>
    <div id="ahpRows"></div>
  </section>
</div>

<div class="grid2">
  <section class="card">
    <h2>الغطاء الأرضي</h2>
    <div class="ctl"><select id="lcRegion" aria-label="المنطقة"><option>مكة المكرمة</option><option>الباحة</option></select></div>
    <p class="note">من بيانات ESA WorldCover 2020 بدقة 10 م. النسبة من مساحة المنطقة المختارة.</p>
    <div class="chart" id="lc"></div>
  </section>
  <section class="card">
    <h2>المناخ: الحرارة والرطوبة</h2>
    <p class="note">متوسطات شهرية. جدة ومكة: معدلات 1991–2020. منحدرات الطائف: شبكة CRU TS 3.1.</p>
    <div class="chart" id="temp"></div>
    <div class="legend"><span><i class="sw" style="background:var(--accent)"></i>جدة</span><span><i class="sw" style="background:var(--accent2)"></i>مكة المكرمة</span><span><i class="sw" style="background:var(--accent3)"></i>منحدرات الطائف</span></div>
    <div class="chart" id="rh" style="margin-top:14px"></div>
  </section>
</div>

<section class="card">
  <h2>خريطة قابلية الفيضانات النهائية</h2>
  <div class="placeholder">بانتظار نتائج الفريق: تُضاف هنا خريطة مؤشر قابلية الفيضانات (FSI) بفئاتها الخمس، ونسبة مساحة كل فئة، ونتيجة التحقق (ROC)، بعد اكتمال عوامل نموذج الارتفاعات الرقمي والتربة والجيولوجيا.</div>
</section>

<footer>
المصادر: محطات الأمطار — وزارة البيئة والمياه والزراعة (1964–2014) · الغطاء الأرضي — ESA WorldCover 2020 · المناخ — climate-zone.com (1991–2020) و CRU TS 3.1 · الطقس الحالي والتوقعات — Open-Meteo.com (CC BY 4.0) · الحدود — ملف Study_Area_Corrected للفريق.
</footer>
</div>

<script src="https://unpkg.com/d3@7.9.0/dist/d3.min.js"></script>
<script src="data.js"></script>
<script>
(function(){
const D = window.FD_DATA;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmt = (v, d) => (v == null || isNaN(+v)) ? '—' : (+v).toLocaleString('en-US', {minimumFractionDigits: d || 0, maximumFractionDigits: d || 0});
const el = (tag, cls, txt) => { const e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
function tipFor(host){ let t = host.querySelector(':scope > .tip'); if (!t){ t = el('div','tip'); t.hidden = true; host.appendChild(t);} return {
  show(ev, lines){ t.replaceChildren(...lines.map((l,i)=>el('div', i? 'm':'', l))); t.hidden=false; const r=host.getBoundingClientRect(); let x=ev.clientX-r.left+12, y=ev.clientY-r.top+12; if(x+t.offsetWidth>host.clientWidth) x=Math.max(0,ev.clientX-r.left-t.offsetWidth-12); if(y+t.offsetHeight>host.clientHeight) y=Math.max(0,ev.clientY-r.top-t.offsetHeight-12); t.style.left=x+'px'; t.style.top=y+'px'; },
  hide(){ t.hidden=true; } }; }

// header + KPIs
const done = D.progress.filter(r=>r.status==='مكتمل').length, cur = D.progress.filter(r=>r.status==='قيد التنفيذ').map(r=>r.component).join('، ');
document.getElementById('lead').textContent = `اكتمل ${done} من أصل ${D.progress.length} مكوّناً من مكونات المشروع، والعمل جارٍ الآن على: ${cur || '—'}.`;
document.getElementById('kArea').textContent = fmt(d3.sum(D.boundary.features, f=>f.properties.area_km2));
document.getElementById('kSt').textContent = D.stations.length;
document.getElementById('kCR').textContent = fmt(D.cons.CR, 3);
const lc = c => (D.lulc.find(r=>r.region==='مكة المكرمة'&&r.class===c)||{}).pct;
document.getElementById('kBare').textContent = fmt(lc('Bare / sparse vegetation'),1);
document.getElementById('kBuilt').textContent = fmt(lc('Built-up'),1);

// progress
const pc = {'مكتمل':'ok','قيد التنفيذ':'warn','قيد المراجعة':'warn','جزئي':'warn'};
const tb = document.getElementById('progRows');
D.progress.forEach(r=>{ const tr=el('tr'); tr.append(el('td','',r.component)); const td=el('td'); td.append(el('span','pill '+(pc[r.status]||'todo'), r.status)); tr.append(td); const n=el('td','',r.note); n.style.color='var(--muted)'; tr.append(n); tb.append(tr); });

// ---------- weather ----------
const CITIES = [
  {ar:'جدة', lat:21.54, lon:39.17},{ar:'مكة المكرمة', lat:21.42, lon:39.83},{ar:'الطائف', lat:21.27, lon:40.42},
  {ar:'رابغ', lat:22.80, lon:39.03},{ar:'الليث', lat:20.15, lon:40.27},{ar:'القنفذة', lat:19.13, lon:41.08},
  {ar:'الباحة', lat:20.01, lon:41.47},{ar:'تربة', lat:21.21, lon:41.63}];
const WMO = {0:'صحو',1:'صحو غالباً',2:'غائم جزئياً',3:'غائم',45:'ضباب',48:'ضباب متجمّد',51:'رذاذ خفيف',53:'رذاذ',55:'رذاذ كثيف',61:'مطر خفيف',63:'مطر',65:'مطر غزير',66:'مطر متجمّد',67:'مطر متجمّد غزير',71:'ثلج خفيف',73:'ثلج',75:'ثلج كثيف',80:'زخات خفيفة',81:'زخات مطر',82:'زخات غزيرة',95:'عاصفة رعدية',96:'عاصفة رعدية مع برد',99:'عاصفة رعدية شديدة مع برد'};
const DIR = d => ['شمالية','شمالية شرقية','شرقية','جنوبية شرقية','جنوبية','جنوبية غربية','غربية','شمالية غربية'][Math.round(((d%360)/45))%8];
const ALERT_MM = 20;
async function loadWeather(){
  const st = document.getElementById('wxStatus'); st.textContent = 'جارٍ التحميل…';
  const url = 'https://api.open-meteo.com/v1/forecast?latitude=' + CITIES.map(c=>c.lat).join(',') + '&longitude=' + CITIES.map(c=>c.lon).join(',') +
    '&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m' +
    '&daily=precipitation_sum,precipitation_probability_max,temperature_2m_max,temperature_2m_min&forecast_days=7&timezone=Asia%2FRiyadh';
  try {
    const res = await fetch(url); if (!res.ok) throw new Error(res.status);
    let js = await res.json(); if (!Array.isArray(js)) js = [js];
    renderWeather(js);
    st.textContent = 'آخر تحديث: ' + new Date().toLocaleTimeString('ar-SA', {hour:'2-digit', minute:'2-digit'});
  } catch(e) {
    st.textContent = 'تعذّر جلب الطقس — تأكد من الاتصال بالإنترنت';
    if (!document.getElementById('wxGrid').children.length) document.getElementById('wxGrid').append(el('div','placeholder','لا توجد بيانات طقس حالياً. باقي أقسام اللوحة تعمل بدون إنترنت.'));
  }
}
function renderWeather(js){
  const g = document.getElementById('wxGrid'); g.replaceChildren();
  js.forEach((w,i)=>{
    const c = CITIES[i], cu = w.current, dmax = d3.max(w.daily.precipitation_sum);
    const card = el('div','wx' + (dmax >= ALERT_MM ? ' alert' : ''));
    const top = el('div'); top.style.display='flex'; top.style.justifyContent='space-between'; top.style.alignItems='center'; top.style.flexWrap='wrap'; top.style.gap='4px';
    top.append(el('span','city',c.ar));
    if (cu.precipitation > 0) top.append(el('span','badge warn','يمطر الآن'));
    else if (dmax >= ALERT_MM) top.append(el('span','badge bad','مطر غزير متوقع'));
    card.append(top, el('div','t', fmt(cu.temperature_2m,0) + '°'), el('div','d', WMO[cu.weather_code] || '—'));
    const r1 = el('div','row'); r1.append(el('span','', 'الرطوبة ' + fmt(cu.relative_humidity_2m) + '%'), el('span','', 'هطول ' + fmt(cu.precipitation,1) + ' ملم'));
    const r2 = el('div','row'); r2.append(el('span','', 'رياح ' + fmt(cu.wind_speed_10m) + ' كم/س'), el('span','', DIR(cu.wind_direction_10m)));
    card.append(r1, r2); g.append(card);
  });
  const t = document.getElementById('fcTable'); t.replaceChildren();
  const days = js[0].daily.time; const th = el('thead'); const hr = el('tr'); hr.append(el('th','','المدينة'));
  days.forEach(d => hr.append(el('th','', new Date(d+'T12:00:00').toLocaleDateString('ar-SA-u-ca-gregory', {weekday:'short', day:'numeric', month:'numeric'}))));
  th.append(hr); t.append(th); const bd = el('tbody');
  js.forEach((w,i)=>{ const tr = el('tr'); tr.append(el('td','',CITIES[i].ar));
    w.daily.precipitation_sum.forEach((p,j)=>{ const td = el('td','', fmt(p,1)); const pr = w.daily.precipitation_probability_max[j];
      td.title = 'احتمال الهطول ' + (pr ?? '—') + '% · العظمى ' + fmt(w.daily.temperature_2m_max[j]) + '° · الصغرى ' + fmt(w.daily.temperature_2m_min[j]) + '°';
      td.style.fontVariantNumeric='tabular-nums';
      if (p >= ALERT_MM) { td.style.color='var(--bad)'; td.style.fontWeight='700'; } else if (p > 0) { td.style.color='var(--accent)'; } else td.style.color='var(--muted)';
      tr.append(td); });
    bd.append(tr); });
  t.append(bd);
}
document.getElementById('wxRefresh').addEventListener('click', loadWeather);
loadWeather(); setInterval(loadWeather, 15*60*1000);

// ---------- map ----------
function drawMap(){
  const host = document.getElementById('map'); host.replaceChildren();
  const w = host.clientWidth || 460, h = Math.max(360, Math.round(w*0.95)), k = Math.cos(21*Math.PI/180);
  const sc = {type:'FeatureCollection', features: D.boundary.features.map(f=>({type:'Feature', properties:f.properties, geometry:{type:f.geometry.type, coordinates: JSON.parse(JSON.stringify(f.geometry.coordinates),(key,v)=>Array.isArray(v)&&v.length===2&&typeof v[0]==='number'?[v[0]*k,v[1]]:v)}}))};
  const P = d3.geoIdentity().reflectY(true).fitExtent([[12,12],[w-12,h-12]], sc), path = d3.geoPath(P), xy = (lon,lat)=>P([lon*k,lat]);
  const svg = d3.select(host).append('svg').attr('width','100%').attr('viewBox',`0 0 ${w} ${h}`).attr('role','img').attr('aria-label','خريطة منطقة الدراسة');
  svg.append('g').selectAll('path').data(sc.features).join('path').attr('d',path).style('fill',d=>d.properties.region==='Makkah'?css('--panel'):css('--line')).style('stroke',css('--fg')).style('stroke-width',1.2);
  const g = svg.append('g');
  D.towns.forEach(t=>{ const p=xy(t.lon,t.lat); g.append('circle').attr('cx',p[0]).attr('cy',p[1]).attr('r',3).style('fill',css('--fg'));
    g.append('text').attr('x',p[0]-5).attr('y',p[1]-5).attr('text-anchor','end').style('font-size','11px').style('fill',css('--fg')).style('paint-order','stroke').style('stroke',css('--panel')).style('stroke-width',3).text(t.town_ar); });
  const tip = tipFor(host), r = d3.scaleSqrt().domain([0, d3.max(D.stations,d=>d.mean_annual_mm)]).range([0,13]);
  svg.append('g').selectAll('circle').data(D.stations.filter(d=>d.mean_annual_mm!=null)).join('circle')
    .attr('cx',d=>xy(d.lon,d.lat)[0]).attr('cy',d=>xy(d.lon,d.lat)[1]).attr('r',d=>Math.max(3,r(d.mean_annual_mm)))
    .style('fill',css('--accent')).style('fill-opacity',.55).style('stroke',css('--accent')).style('cursor','pointer')
    .on('mousemove',(ev,d)=>tip.show(ev,[d.name+' ('+d.code+')','الارتفاع: '+(d.elevation_m!=null?fmt(d.elevation_m)+' م':'غير معروف'),'المعدل السنوي: '+fmt(d.mean_annual_mm,1)+' ملم','أقصى مطر يومي: '+fmt(d.max_daily_mm,1)+' ملم']))
    .on('mouseleave',()=>tip.hide());
}

// ---------- AHP ----------
let adjM = {};
function drawAHP(){
  const host = document.getElementById('ahpRows'); host.replaceChildren(); host.style.position='relative';
  const rows = D.ahp.map(r=>({...r, w:+r.weight_pct, m: adjM[r.factor] ?? 1})), els=[], tip = tipFor(host);
  const re = ()=>{ const tot=d3.sum(rows,r=>r.w*r.m)||1; rows.forEach(r=>r.adj=r.w*r.m/tot*100); const mx=Math.max(d3.max(rows,r=>r.w),d3.max(rows,r=>r.adj));
    els.forEach(({r,b,a,v})=>{ b.style.width=(r.w/mx*100)+'%'; a.style.width=(r.adj/mx*100)+'%'; v.textContent=fmt(r.adj,1)+'%'; }); };
  rows.forEach(r=>{ const row=el('div','ahp-row'); const lab=el('div','',r.factor_ar); lab.append(el('span','grp',r.group_ar+' · '+r.status_ar));
    const mid=el('div'), tr=el('div','track'), b=el('div','base'), a=el('div','adj'); tr.append(b,a);
    tr.addEventListener('mousemove',ev=>tip.show(ev,[r.factor_ar,'الوزن الأصلي: '+fmt(r.w,2)+'%','الوزن بعد التعديل: '+fmt(r.adj,2)+'%','نطاق الترتيب عند تغيير ±10%: '+r.rank_min_10+'–'+r.rank_max_10]));
    tr.addEventListener('mouseleave',()=>tip.hide());
    const rg=el('input'); rg.type='range'; rg.min=0; rg.max=300; rg.step=5; rg.value=Math.round(r.m*100); rg.setAttribute('aria-label','أهمية '+r.factor_ar);
    rg.addEventListener('input',()=>{ r.m=+rg.value/100; adjM[r.factor]=r.m; re(); });
    mid.append(tr,rg); const v=el('div','val'); row.append(lab,mid,v); host.append(row); els.push({r,b,a,v}); });
  re();
}
document.getElementById('ahpReset').addEventListener('click',()=>{ adjM={}; drawAHP(); });

// ---------- land cover ----------
function drawLC(){
  const host=document.getElementById('lc'); host.replaceChildren(); const region=document.getElementById('lcRegion').value;
  const data=D.lulc.filter(r=>r.region===region&&r.pct>0).sort((a,b)=>b.pct-a.pct);
  const w=host.clientWidth||460, bh=22, h=data.length*(bh+8)+10;
  const svg=d3.select(host).append('svg').attr('width','100%').attr('viewBox',`0 0 ${w} ${h}`).attr('role','img').attr('aria-label','الغطاء الأرضي في '+region);
  const tmp=svg.append('g'); let lw=0; data.forEach(d=>{ const t=tmp.append('text').style('font-size','12px').text(d.class_ar); lw=Math.max(lw,t.node().getComputedTextLength()); }); tmp.remove(); lw=Math.min(lw+10,w*.45);
  const x=d3.scaleLinear().domain([0,100]).range([0,w-lw-50]), tip=tipFor(host);
  data.forEach((d,i)=>{ const y=5+i*(bh+8), bw=Math.max(2,x(d.pct));
    svg.append('text').attr('x',w).attr('y',y+bh/2+4).attr('direction','rtl').attr('text-anchor','start').style('font-size','12px').style('fill',css('--fg')).text(d.class_ar);
    svg.append('rect').attr('x',w-lw-bw).attr('y',y).attr('width',bw).attr('height',bh).attr('rx',3).style('fill',d.class==='Built-up'?css('--bad'):css('--accent'))
      .on('mousemove',ev=>tip.show(ev,[d.class_ar,fmt(d.pct,2)+'% من المساحة',fmt(d.area_km2)+' كم²'])).on('mouseleave',()=>tip.hide());
    svg.append('text').attr('x',w-lw-bw-6).attr('y',y+bh/2+4).attr('text-anchor','end').style('font-size','11px').style('fill',css('--muted')).text(fmt(d.pct,d.pct<1?2:1)+'%'); });
}
document.getElementById('lcRegion').addEventListener('change',drawLC);

// ---------- climate ----------
function line(id, series, yLabel){
  const host=document.getElementById(id); host.replaceChildren();
  const rows=D.climate, w=host.clientWidth||460, h=210, m={t:18,r:34,b:26,l:10};
  const vals=series.flatMap(s=>rows.map(r=>r[s.key]));
  const y=d3.scaleLinear().domain([Math.floor(d3.min(vals)/5)*5,Math.ceil(d3.max(vals)/5)*5]).range([h-m.b,m.t]);
  const x=d3.scalePoint().domain(d3.range(1,13)).range([w-m.r,m.l+8]);
  const svg=d3.select(host).append('svg').attr('width','100%').attr('viewBox',`0 0 ${w} ${h}`).attr('role','img').attr('aria-label',yLabel);
  svg.append('g').attr('class','grid').attr('transform',`translate(${w-m.r},0)`).call(d3.axisLeft(y).ticks(4).tickSize(w-m.r-m.l).tickFormat(''));
  svg.append('g').attr('class','axis').attr('transform',`translate(${w-m.r},0)`).call(d3.axisRight(y).ticks(4).tickSize(0).tickPadding(6)).call(g=>g.select('.domain').remove());
  svg.append('g').attr('class','axis').attr('transform',`translate(0,${h-m.b})`).call(d3.axisBottom(x).tickSize(0).tickPadding(8).tickFormat(i=>(w<460&&!(i%2))?'':rows[i-1].month_ar.slice(0,3))).call(g=>g.select('.domain').remove());
  svg.append('text').attr('x',w).attr('y',11).attr('text-anchor','end').style('font-size','11px').style('fill',css('--muted')).text(yLabel);
  const tip=tipFor(host);
  series.forEach(s=>{ const c=css(s.c);
    svg.append('path').datum(rows).attr('d',d3.line().x(r=>x(r.month)).y(r=>y(r[s.key]))).style('fill','none').style('stroke',c).style('stroke-width',2);
    svg.append('g').selectAll('circle').data(rows).join('circle').attr('cx',r=>x(r.month)).attr('cy',r=>y(r[s.key])).attr('r',3.5).style('fill',c)
      .on('mousemove',(ev,r)=>tip.show(ev,[s.name+' — '+r.month_ar, fmt(r[s.key],1)+' '+s.u])).on('mouseleave',()=>tip.hide()); });
}
function drawClimate(){
  line('temp',[{key:'jeddah_temp_c',name:'جدة',c:'--accent',u:'°م'},{key:'makkah_temp_c',name:'مكة المكرمة',c:'--accent2',u:'°م'},{key:'taif_temp_c',name:'منحدرات الطائف',c:'--accent3',u:'°م'}],'متوسط الحرارة (°م)');
  line('rh',[{key:'jeddah_rh_pct',name:'جدة',c:'--accent',u:'%'},{key:'makkah_rh_pct',name:'مكة المكرمة',c:'--accent2',u:'%'}],'الرطوبة النسبية (%)');
}

function drawAll(){ drawMap(); drawAHP(); drawLC(); drawClimate(); }
drawAll();
let rt; window.addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(()=>{ drawMap(); drawLC(); drawClimate(); },200); });
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', drawAll);
})();
</script>
</body>
</html>
