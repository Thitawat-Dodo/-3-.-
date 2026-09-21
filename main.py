# -*- coding: utf-8 -*-
"""
main.py
สคริปต์ Python ที่รองรับการแสดงผลบน Streamlit แบบเต็มหน้าจอ (No Scrollbar)
และรันผ่าน `python main.py` เพื่อสร้างไฟล์ slides.html ได้เช่นกัน

วิธีใช้งาน:
    streamlit run main.py
    หรือ
    python main.py
"""

HTML = r"""
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>เศษส่วน อัตราส่วน ร้อยละ</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700;800&family=Kanit:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f4f7fb; --ink:#1e2a3a; --muted:#5b6b7f;
  --blue:#2563eb; --blue-soft:#dbeafe;
  --teal:#0d9488; --teal-soft:#ccfbf1;
  --orange:#ea580c; --orange-soft:#ffedd5;
  --purple:#7c3aed; --purple-soft:#ede9fe;
  --card:#ffffff; --line:#e2e8f0;
  --green:#16a34a; --red:#dc2626;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;width:100%;overflow:hidden}
body{font-family:'Sarabun',sans-serif;background:#0f172a;color:var(--ink)}
#deck{position:fixed;inset:0}
.slide{position:absolute;inset:0;display:none;flex-direction:column;padding:3vh 4vw 7vh;background:var(--bg);overflow-y:auto}
.slide.active{display:flex;animation:fadein .35s ease}
@keyframes fadein{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.slide::before{content:"";position:absolute;top:0;left:0;right:0;height:.9vh;background:var(--accent,var(--blue))}
h1{font-family:'Kanit',sans-serif;font-size:clamp(24px,4.5vmin,48px);line-height:1.2}
h2{font-family:'Kanit',sans-serif;font-size:clamp(20px,3.8vmin,36px);color:var(--accent,var(--blue));margin-bottom:1.8vh}
h3{font-family:'Kanit',sans-serif;font-size:clamp(16px,2.6vmin,24px);margin-bottom:1vh}
p,li{font-size:clamp(13px,2.2vmin,20px);line-height:1.5}
.small{font-size:clamp(11px,1.7vmin,16px);color:var(--muted)}
.kicker{font-family:'Kanit',sans-serif;letter-spacing:.14em;text-transform:uppercase;font-size:clamp(10px,1.6vmin,14px);color:var(--muted);margin-bottom:1vh}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.footer-tag{position:absolute;bottom:2vh;left:4vw;font-size:clamp(10px,1.5vmin,13px);color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:2vh 1.4vw;box-shadow:0 2px 10px rgba(15,23,42,.05)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1.4vw}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2vw}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:1vw}
.center{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;flex:1}
/* fractions */
.frac{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 .25em;line-height:1.05;font-size:.85em}
.frac>span:first-child{border-bottom:2px solid currentColor;padding:0 .3em}
.frac>span:last-child{padding:0 .3em}
/* chips / badges */
.chip{display:inline-block;padding:.25em .8em;border-radius:999px;font-weight:600;font-size:clamp(11px,1.8vmin,15px)}
.chip.blue{background:var(--blue-soft);color:var(--blue)}
.chip.teal{background:var(--teal-soft);color:var(--teal)}
.chip.orange{background:var(--orange-soft);color:var(--orange)}
.chip.purple{background:var(--purple-soft);color:var(--purple)}
/* title slide */
.title-slide{background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 55%,#0d9488 100%);color:#fff;justify-content:center}
.title-slide::before{background:#fbbf24}
.title-slide .kicker{color:#bfdbfe}
.title-slide .sub{color:#dbeafe}
/* divider slides */
.divider{color:#fff;justify-content:center}
.divider .big-num{font-family:'Kanit',sans-serif;font-size:clamp(50px,12vmin,130px);font-weight:700;opacity:.25;line-height:1}
.d1{background:linear-gradient(135deg,#1e40af,#2563eb)}
.d2{background:linear-gradient(135deg,#0f766e,#14b8a6)}
.d3{background:linear-gradient(135deg,#c2410c,#f97316)}
.d4{background:linear-gradient(135deg,#5b21b6,#8b5cf6)}

/* nav - ปรับแต่งขยายขนาดปุ่มที่นี่ที่เดียว */
#nav{position:fixed;bottom:0;left:0;right:0;height:6.5vh;min-height:50px;background:rgba(15,23,42,.95);display:flex;align-items:center;justify-content:center;gap:20px;z-index:50}
#nav button{font-family:'Sarabun',sans-serif;background:#334155;color:#e2e8f0;border:none;border-radius:10px;padding:8px 24px;font-size:clamp(15px,2.2vmin,20px);font-weight:600;cursor:pointer;transition:all 0.2s ease}
#nav button:hover{background:var(--blue);color:#fff;transform:scale(1.05)}
#counter{color:#94a3b8;font-size:clamp(13px,1.8vmin,16px);min-width:90px;text-align:center;font-weight:600}
#bar{position:fixed;bottom:6.5vh;left:0;height:.4vh;background:#fbbf24;z-index:50;transition:width .3s}

/* quiz */
.opt{display:block;width:100%;text-align:left;background:#fff;border:2px solid var(--line);border-radius:12px;padding:1.4vh 1.2vw;margin-bottom:1vh;font-family:'Sarabun',sans-serif;font-size:clamp(13px,2.2vmin,19px);cursor:pointer;transition:.15s}
.opt:hover{border-color:var(--accent,var(--blue));background:#f8fafc}
.opt.correct{border-color:var(--green);background:#f0fdf4;font-weight:700}
.opt.wrong{border-color:var(--red);background:#fef2f2}
.explain{display:none;margin-top:1vh;background:#fffbeb;border:1px solid #fcd34d;border-radius:12px;padding:1.4vh 1.2vw}
.explain.show{display:block;animation:fadein .3s ease}
.reveal-btn{font-family:'Sarabun',sans-serif;background:var(--accent,var(--blue));color:#fff;border:none;border-radius:10px;padding:1vh 1.8vw;font-size:clamp(12px,2vmin,17px);cursor:pointer;margin-top:1vh}
/* symbol grid */
.sym{background:#fff;border:1px solid var(--line);border-radius:12px;padding:1.4vh .8vw;text-align:center}
.sym .s{font-family:'Kanit',sans-serif;font-size:clamp(16px,3vmin,26px);color:var(--blue);font-weight:700}
.sym .d{font-size:clamp(10px,1.7vmin,15px);color:var(--muted);margin-top:.3vh}
/* example visuals */
.ex-visual{display:flex;gap:1.2vw;align-items:stretch;flex-wrap:wrap}
.ex-item{flex:1;min-width:160px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:1.5vh 1vw;text-align:center}
.ex-item .icon{font-size:clamp(22px,4.5vmin,38px)}
.num{font-family:'Kanit',sans-serif;font-weight:700;color:var(--accent,var(--blue))}
.ansline{background:#f0fdf4;border-left:5px solid var(--green);border-radius:8px;padding:1vh 1vw;margin-top:.6vh}
.stepbox{background:#eff6ff;border-left:5px solid var(--blue);border-radius:8px;padding:1vh 1vw;margin-top:.8vh}
ol.qlist{padding-left:1.4em}
ol.qlist li{margin-bottom:1vh}
/* sidebar */
#sidebar{position:fixed;left:0;top:0;bottom:6.5vh;width:210px;background:#0f172a;color:#cbd5e1;padding:5vh 1vw 2vh;display:flex;flex-direction:column;gap:.5vh;z-index:40;border-right:1px solid rgba(255,255,255,.08);transition:transform .3s ease}
#sidebar.collapsed{transform:translateX(-210px)}
#sidebar .brand{font-family:'Kanit',sans-serif;font-weight:700;font-size:clamp(12px,1.8vmin,15px);color:#fbbf24;letter-spacing:.1em;margin-bottom:1.5vh;padding:0 .4vw}
#sidebar .brand small{display:block;font-family:'Sarabun',sans-serif;font-weight:400;font-size:clamp(9px,1.4vmin,11px);color:#94a3b8;margin-top:.3vh;letter-spacing:.05em;line-height:1.3}
.sb-item{display:flex;align-items:center;gap:.6vw;padding:1.2vh .5vw;border-radius:10px;cursor:pointer;font-family:'Sarabun',sans-serif;font-size:clamp(11px,1.7vmin,14px);border:none;background:transparent;color:#cbd5e1;text-align:left;width:100%}
.sb-item:hover{background:rgba(255,255,255,.06);color:#fff}
.sb-item .num{width:24px;height:24px;border-radius:8px;display:inline-flex;align-items:center;justify-content:center;font-family:'Kanit',sans-serif;font-weight:700;font-size:clamp(10px,1.5vmin,13px);flex-shrink:0;background:rgba(255,255,255,.06);color:#e2e8f0}
.sb-item .lbl{line-height:1.2}
.sb-item.home .num{background:#3b82f6;color:#fff}
.sb-item.t1 .num{background:#2563eb;color:#fff}
.sb-item.t2 .num{background:#0d9488;color:#fff}
.sb-item.t3 .num{background:#ea580c;color:#fff}
.sb-item.t4 .num{background:#7c3aed;color:#fff}
.sb-item.active{background:rgba(255,255,255,.1);color:#fff;font-weight:700;box-shadow:inset 3px 0 0 currentColor}
.sb-item.home.active{background:rgba(59,130,246,.25);color:#fff}
.sb-item.t1.active{background:rgba(37,99,235,.25);color:#fff}
.sb-item.t2.active{background:rgba(13,148,136,.25);color:#fff}
.sb-item.t3.active{background:rgba(234,88,12,.25);color:#fff}
.sb-item.t4.active{background:rgba(124,58,237,.25);color:#fff}
#toggle{position:fixed;left:210px;top:50%;transform:translateY(-50%);background:#334155;color:#e2e8f0;border:none;border-radius:0 10px 10px 0;padding:1vh .6vw;font-size:clamp(12px,1.8vmin,15px);cursor:pointer;z-index:45;transition:left .3s ease;font-family:'Sarabun',sans-serif}
#toggle.collapsed{left:0}
#toggle:hover{background:var(--blue);color:#fff}
.slide{padding-left:calc(4vw + 210px)}
#deck.shifted .slide{padding-left:4vw}

/* ===== interactive v2 ===== */
.card.link{cursor:pointer;transition:.18s;position:relative;padding-bottom:4vh}
.card.link:hover{transform:translateY(-4px);box-shadow:0 10px 24px rgba(15,23,42,.14)}
.card.link .hint{position:absolute;bottom:1vh;right:1vw;font-size:clamp(9px,1.5vmin,12px);color:var(--muted);opacity:.75;font-weight:600}
.card.link:hover .hint{opacity:1;color:var(--accent,var(--blue))}
.sym{cursor:pointer;transition:.18s}
.sym:hover{transform:translateY(-3px);box-shadow:0 6px 18px rgba(15,23,42,.12);border-color:var(--blue)}
.sym.on{border-color:var(--blue);background:#eff6ff;box-shadow:0 6px 18px rgba(37,99,235,.2)}
.bubble{display:none;position:relative;margin-top:1.8vh;background:#fff;border:2px solid var(--blue);border-radius:14px;padding:1.4vh 1.2vw;box-shadow:0 10px 28px rgba(15,23,42,.12)}
.bubble.show{display:block;animation:fadein .28s ease}
.bubble::before{content:"";position:absolute;top:-11px;left:5%;border-left:11px solid transparent;border-right:11px solid transparent;border-bottom:11px solid var(--blue)}
.bubble h3{color:var(--blue);font-size:clamp(14px,2.4vmin,20px);margin-bottom:.5vh}
.bubble .ex{font-family:'Kanit',sans-serif;font-size:clamp(14px,2.6vmin,22px);color:var(--ink)}
.bubble .why{font-size:clamp(11px,1.8vmin,15px);color:var(--muted);margin-top:.5vh;line-height:1.4}
.mini-graph{display:none;margin-top:1vh;background:#f8fafc;border:1px solid var(--line);border-radius:12px;padding:.6vh .5vw}
.mini-graph.show{display:block;animation:fadein .28s ease}
.mini-graph svg{width:100%;height:auto;max-height:22vh;display:block}
.anscard{cursor:pointer;transition:.18s}
.anscard:hover{box-shadow:0 6px 18px rgba(15,23,42,.12);transform:translateY(-2px)}
.anscard.on{border-color:var(--green);box-shadow:0 6px 20px rgba(22,163,74,.2)}
.pie-wrap{display:none;margin-top:1vh}
.pie-wrap.show{display:block;animation:fadein .28s ease}
.pie-wrap svg{width:min(100%,170px);height:auto;display:block;margin:0 auto}
.sec-head{font-family:'Kanit',sans-serif;font-size:clamp(14px,2.4vmin,20px);font-weight:700;color:var(--orange);border-left:5px solid var(--orange);padding-left:.5vw;margin-bottom:1.2vh}
.sec-head.p{color:var(--purple);border-left-color:var(--purple)}
.qnum{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;border-radius:50%;background:var(--orange);color:#fff;font-family:'Kanit',sans-serif;font-weight:700;font-size:clamp(10px,1.6vmin,13px);margin-right:.4em;vertical-align:middle}
.qnum.p{background:var(--purple)}
</style>
</head>
<body>
<aside id="sidebar">
  <div class="brand">เศษส่วน อัตราส่วน ร้อยละ<small>Fractions · Ratio · Percentage</small></div>
  <button class="sb-item home" data-i="0"><span class="num">⌂</span><span class="lbl">หน้าหลัก<br><small style="color:#94a3b8;font-size:.85em">หน้า 1</small></span></button>
  <button class="sb-item t1" data-i="2"><span class="num">1</span><span class="lbl">ระบบจำนวน<br><small style="color:#94a3b8;font-size:.85em">หน้า 3</small></span></button>
  <button class="sb-item t2" data-i="5"><span class="num">2</span><span class="lbl">อัตราส่วน สัดส่วน<br><small style="color:#94a3b8;font-size:.85em">หน้า 6</small></span></button>
  <button class="sb-item t3" data-i="13"><span class="num">3</span><span class="lbl">ร้อยละ<br><small style="color:#94a3b8;font-size:.85em">หน้า 14</small></span></button>
  <button class="sb-item t4" data-i="17"><span class="num">4</span><span class="lbl">Quiz<br><small style="color:#94a3b8;font-size:.85em">หน้า 18</small></span></button>
</aside>
<button id="toggle" onclick="toggleSidebar()">◀</button>
<div id="deck">

<!-- ============ SLIDE 1 : TITLE ============ -->
<section class="slide title-slide">
  <div class="center">
    <div class="kicker">Mathematics · คณิตศาสตร์เบื้องต้น</div>
    <h1>เศษส่วน อัตราส่วน ร้อยละ</h1>
    <p style="font-family:'Kanit';font-size:clamp(16px,3vmin,26px);margin-top:2vh">Fractions · Ratio · Percentage</p>
  </div>
  <div class="footer-tag" style="color:#bfdbfe">กด → เพื่อไปต่อ หรือคลิกปุ่ม Next ด้านล่าง</div>
</section>

<!-- ============ SLIDE 2 : AGENDA ============ -->
<section class="slide">
  <h2>เนื้อหาการเรียนรู้วันนี้ (Lesson Overview)</h2>
  <div class="body">
    <div class="grid2" style="gap:1.4vw">
      <div class="card" style="border-top:6px solid var(--blue)">
        <span class="chip blue">หมวดที่ 1</span>
        <h3>ระบบจำนวน (Number System)</h3>
        <p class="small">แผนผังโครงสร้างของจำนวน และสัญลักษณ์เซตที่สำคัญ</p>
      </div>
      <div class="card" style="border-top:6px solid var(--teal)">
        <span class="chip teal">หมวดที่ 2</span>
        <h3>อัตราส่วน สัดส่วน อัตราส่วนต่อเนื่อง</h3>
        <p class="small">สัดส่วนตรง–ผกผัน วิธีแก้ปัญหา และอัตราส่วนต่อเนื่อง (Continued Ratio)</p>
      </div>
      <div class="card" style="border-top:6px solid var(--orange)">
        <span class="chip orange">หมวดที่ 3</span>
        <h3>ร้อยละ (Percentage)</h3>
        <p class="small">นิยามของร้อยละ และโจทย์ปัญหาร้อยละในชีวิตจริง</p>
      </div>
      <div class="card" style="border-top:6px solid var(--purple)">
        <span class="chip purple">หมวดที่ 4</span>
        <h3>แบบฝึกหัด แบบทดสอบ (Quiz)</h3>
        <p class="small">ลองทำดู — กดเลือกคำตอบแล้วดูเฉลยพร้อมวิธีทำทันที</p>
      </div>
    </div>
  </div>
  <div class="footer-tag">เศษส่วน อัตราส่วน ร้อยละ</div>
</section>

<!-- ============ SLIDE 3 : DIVIDER 1 ============ -->
<section class="slide divider d1">
  <div class="center">
    <div class="big-num">01</div>
    <h1>ระบบจำนวน</h1>
    <p style="color:#bfdbfe;font-family:'Kanit';font-size:clamp(15px,2.6vmin,24px)">Number System</p>
  </div>
</section>

<!-- ============ SLIDE 4 : NUMBER TREE ============ -->
<section class="slide">
  <h2>1. แผนผังโครงสร้างของจำนวน (Structure of Numbers)</h2>
  <div class="body" style="align-items:center;justify-content:center">
    <svg viewBox="40 0 1500 430" style="width:min(100%,1150px);height:auto;font-family:'Sarabun',sans-serif">
      <defs>
        <linearGradient id="gTop" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#3b82f6"/>
        </linearGradient>
      </defs>
      <!-- connectors -->
      <path d="M620 64 L620 88 M250 88 L990 88 M250 88 L250 112 M990 88 L990 112" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M250 168 L250 372" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M990 168 L990 182 M700 182 L1280 182 M700 182 L700 190 M990 182 L990 190 M1280 182 L1280 190" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M700 244 L700 268" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M990 244 L990 316" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M1280 244 L1280 262 M1150 262 L1410 262 M1150 262 L1150 276 M1280 262 L1280 276 M1410 262 L1410 276" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <path d="M1410 322 L1410 344" stroke="#94a3b8" stroke-width="2.5" fill="none"/>
      <!-- root -->
      <rect x="480" y="8" width="280" height="56" rx="14" fill="url(#gTop)"/>
      <text x="620" y="33" text-anchor="middle" fill="#fff" font-size="22" font-weight="700">จำนวนจริง</text>
      <text x="620" y="53" text-anchor="middle" fill="#bfdbfe" font-size="14">Real Numbers</text>
      <!-- level 1 -->
      <rect x="110" y="112" width="280" height="56" rx="12" fill="#ffedd5" stroke="#ea580c" stroke-width="2"/>
      <text x="250" y="137" text-anchor="middle" fill="#9a3412" font-size="20" font-weight="700">จำนวนอตรรกยะ</text>
      <text x="250" y="157" text-anchor="middle" fill="#ea580c" font-size="12">Irrational Numbers</text>
      <rect x="850" y="112" width="280" height="56" rx="12" fill="#ccfbf1" stroke="#0d9488" stroke-width="2"/>
      <text x="990" y="137" text-anchor="middle" fill="#134e4a" font-size="20" font-weight="700">จำนวนตรรกยะ</text>
      <text x="990" y="157" text-anchor="middle" fill="#0d9488" font-size="12">Rational Numbers</text>
      <!-- irrational children -->
      <rect x="90" y="190" width="320" height="50" rx="10" fill="#fff" stroke="#fdba74" stroke-width="2"/>
      <text x="250" y="221" text-anchor="middle" fill="#9a3412" font-size="17">ทศนิยมไม่ซ้ำ</text>
      <rect x="90" y="256" width="320" height="50" rx="10" fill="#fff" stroke="#fdba74" stroke-width="2"/>
      <text x="250" y="287" text-anchor="middle" fill="#9a3412" font-size="17">√2 , √3 , √5 …</text>
      <rect x="90" y="322" width="320" height="50" rx="10" fill="#fff" stroke="#fdba74" stroke-width="2"/>
      <text x="250" y="353" text-anchor="middle" fill="#9a3412" font-size="17">π , e</text>
      <!-- rational children -->
      <rect x="615" y="190" width="170" height="54" rx="12" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="700" y="223" text-anchor="middle" fill="#1e3a8a" font-size="18" font-weight="700">เศษส่วน</text>
      <rect x="905" y="190" width="170" height="54" rx="12" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
      <text x="990" y="223" text-anchor="middle" fill="#5b21b6" font-size="18" font-weight="700">ทศนิยม</text>
      <rect x="1195" y="190" width="170" height="54" rx="12" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
      <text x="1280" y="223" text-anchor="middle" fill="#334155" font-size="18" font-weight="700">จำนวนเต็ม</text>
      <!-- fraction sub -->
      <rect x="615" y="268" width="170" height="50" rx="10" fill="#fff" stroke="#93c5fd" stroke-width="2"/>
      <text x="686" y="294" text-anchor="middle" fill="#1e3a8a" font-size="15">a</text>
      <line x1="676" y1="298" x2="696" y2="298" stroke="#1e3a8a" stroke-width="1.6"/>
      <text x="686" y="314" text-anchor="middle" fill="#1e3a8a" font-size="15">b</text>
      <text x="712" y="300" fill="#1e3a8a" font-size="13">; b ≠ 0</text>
      <!-- decimal subs -->
      <rect x="905" y="264" width="170" height="44" rx="10" fill="#fff" stroke="#c4b5fd" stroke-width="2"/>
      <text x="990" y="292" text-anchor="middle" fill="#5b21b6" font-size="15">รู้จบ</text>
      <rect x="905" y="316" width="170" height="44" rx="10" fill="#fff" stroke="#c4b5fd" stroke-width="2"/>
      <text x="990" y="344" text-anchor="middle" fill="#5b21b6" font-size="15">ไม่รู้จบ</text>
      <!-- integer subs -->
      <rect x="1090" y="276" width="120" height="46" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="2"/>
      <text x="1150" y="304" text-anchor="middle" fill="#475569" font-size="13">จำนวนเต็มลบ</text>
      <rect x="1230" y="276" width="100" height="46" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="2"/>
      <text x="1280" y="304" text-anchor="middle" fill="#475569" font-size="15">ศูนย์</text>
      <rect x="1350" y="276" width="120" height="46" rx="10" fill="#fff" stroke="#cbd5e1" stroke-width="2"/>
      <text x="1410" y="304" text-anchor="middle" fill="#475569" font-size="13">จำนวนเต็มบวก</text>
      <!-- natural -->
      <rect x="1320" y="344" width="180" height="46" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
      <text x="1410" y="372" text-anchor="middle" fill="#14532d" font-size="15" font-weight="700">จำนวนธรรมชาติ</text>
    </svg>
  </div>
  <div class="footer-tag">หมวดที่ 1 · ระบบจำนวน (Number System)</div>
</section>

<!-- ============ SLIDE 5 : SET SYMBOLS ============ -->
<section class="slide">
  <h2>2. สัญลักษณ์เซตที่สำคัญ (Important Set Notations)</h2>
  <div class="body">
    <div class="grid4">
      <div class="sym"><div class="s">R</div><div class="d">เซตของจำนวนจริง</div></div>
      <div class="sym"><div class="s">R⁺</div><div class="d">จำนวนจริงบวก</div></div>
      <div class="sym"><div class="s">R⁻</div><div class="d">จำนวนจริงลบ</div></div>
      <div class="sym"><div class="s">Q</div><div class="d">เซตของจำนวนตรรกยะ</div></div>
      <div class="sym"><div class="s">Q′</div><div class="d">เซตของจำนวนอตรรกยะ</div></div>
      <div class="sym"><div class="s">N</div><div class="d">เซตของจำนวนนับ</div></div>
      <div class="sym"><div class="s">I</div><div class="d">เซตของจำนวนเต็ม</div></div>
      <div class="sym"><div class="s">I⁺ / I⁻</div><div class="d">จำนวนเต็มบวก / เต็มลบ</div></div>
    </div>
    <div class="card" style="margin-top:2vh;background:#eff6ff;border-left:5px solid var(--blue)">
      <p><b>จำไว้ (Remember):</b> จำนวนตรรกยะ (Q) คือจำนวนที่เขียนเป็นเศษส่วน
      <span class="frac"><span>a</span><span>b</span></span> ได้ เมื่อ a, b เป็นจำนวนเต็มและ b ≠ 0 —
      ส่วนจำนวนอตรรกยะ (Q′) คือทศนิยมไม่รู้จบไม่ซ้ำ เช่น <b>√2, π</b></p>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 1 · ระบบจำนวน (Number System)</div>
</section>

<!-- ============ SLIDE 6 : DIVIDER 2 ============ -->
<section class="slide divider d2">
  <div class="center">
    <div class="big-num">02</div>
    <h1>อัตราส่วน สัดส่วน และอัตราส่วนต่อเนื่อง</h1>
    <p style="color:#99f6e4;font-family:'Kanit';font-size:clamp(15px,2.6vmin,24px)">Ratio · Proportion · Continued Ratio</p>
  </div>
</section>

<!-- ============ SLIDE 7 : DIRECT vs INVERSE ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>ประเภทของสัดส่วน (Types of Proportion)</h2>
  <div class="body">
    <div class="grid2">
      <div class="card" style="border-top:6px solid var(--teal)">
        <span class="chip teal">1) สัดส่วนตรง</span>
        <h3 style="color:var(--teal)">Direct Proportion</h3>
        <p>เปรียบเทียบระหว่าง 2 ปริมาณ โดยมีเงื่อนไขคือ</p>
        <p style="margin-top:.8vh">✅ ถ้าปริมาณหนึ่ง<b>เพิ่มขึ้น</b> อีกปริมาณหนึ่งจะ<b>เพิ่มขึ้นตาม</b></p>
        <p>✅ ถ้าปริมาณหนึ่ง<b>ลดลง</b> อีกปริมาณหนึ่งจะ<b>ลดลงตาม</b></p>
        <p class="small" style="margin-top:1vh">ตัวอย่าง: ยิ่งซื้อบะหมี่หลายชาม ยิ่งจ่ายเงินมาก</p>
      </div>
      <div class="card" style="border-top:6px solid var(--orange)">
        <span class="chip orange">2) สัดส่วนผกผัน</span>
        <h3 style="color:var(--orange)">Inverse Proportion</h3>
        <p>เปรียบเทียบระหว่าง 2 ปริมาณ โดยมีเงื่อนไขคือ</p>
        <p style="margin-top:.8vh">🔄 ถ้าปริมาณหนึ่ง<b>เพิ่มขึ้น</b> อีกปริมาณหนึ่งจะ<b>ลดลง</b></p>
        <p>🔄 ถ้าปริมาณหนึ่ง<b>ลดลง</b> อีกปริมาณหนึ่งจะ<b>เพิ่มขึ้น</b></p>
        <p class="small" style="margin-top:1vh">ตัวอย่าง: ยิ่งมีคนงานมาก ยิ่งใช้เวลาทำงานน้อยลง</p>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · อัตราส่วน สัดส่วน และอัตราส่วนต่อเนื่อง</div>
</section>

<!-- ============ SLIDE 8 : SOLUTION METHODS ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>วิธีแก้ปัญหา (Solution Methods)</h2>
  <div class="body">
    <div class="grid2">
      <div class="card">
        <h3 style="color:var(--teal)">วิธีที่ 1 · เทียบบัญญัติไตรยางศ์</h3>
        <p>วิเคราะห์ก่อนว่าเป็น</p>
        <p>• <b>บัญญัติไตรยางศ์แบบตรง</b> — คูณตรง ๆ</p>
        <p>• <b>บัญญัติไตรยางศ์แบบผกผัน</b> — ต้อง<b>กลับอัตราส่วน</b>ก่อนคูณ</p>
        <div class="stepbox">
          <p class="small">บัญญัติไตรยางศ์: <b>รู้ 3 ปริมาณ หาปริมาณที่ 4</b><br>
          ตรง: หา = <span class="frac"><span>หลังที่รู้ × หน้าที่รู้</span><span>หน้าที่รู้ (คู่เดิม)</span></span>
          ผกผัน: กลับตัวเลขคู่ใดคู่หนึ่งก่อน</p>
        </div>
      </div>
      <div class="card">
        <h3 style="color:var(--teal)">วิธีที่ 2 · เทียบสัดส่วน</h3>
        <p>1) เอาสิ่งของ<b>ชนิดเดียวกัน</b>เข้าสัดส่วน</p>
        <p>2) สมมุติตัวแปร — โจทย์ถามสิ่งใด ให้สมมุติสิ่งนั้นเป็นตัวแปร <b>x</b></p>
        <p>3) แก้ปัญหาโดยใช้หลักสัดส่วน</p>
        <div class="stepbox">
          <p class="small">⚠️ ต้องวิเคราะห์ก่อนเสมอว่าเป็น<b>สัดส่วนตรง</b> หรือ <b>สัดส่วนผกผัน</b>
          (ถ้าผกผันจะต้องกลับอัตราส่วน)</p>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · อัตราส่วน สัดส่วน และอัตราส่วนต่อเนื่อง</div>
</section>

<!-- ============ SLIDE 9 : EXAMPLES ลองคิดดู ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>ลองคิดดูนะครับ — สัดส่วนตรงและผกผัน (Try It!)</h2>
  <div class="body">
    <div class="grid4 ex-visual">
      <div class="ex-item">
        <div class="icon">🍜</div>
        <p><b>ข้อ 1</b><br>บะหมี่ 4 ชาม ราคา 80 บาท ถ้าพินมีเงิน 360 บาท จะกินบะหมี่ได้ทั้งหมดกี่ชาม</p>
        <p class="small" style="margin-top:.6vh">💡 สัดส่วนตรง</p>
      </div>
      <div class="ex-item">
        <div class="icon">👷</div>
        <p><b>ข้อ 2</b><br>ในหนึ่งวัน ช่าง 5 คน สร้างกำแพงได้ 35 เมตร ถ้ามีช่าง 8 คน จะสร้างกำแพงได้กี่เมตร</p>
        <p class="small" style="margin-top:.6vh">💡 สัดส่วนตรง</p>
      </div>
      <div class="ex-item">
        <div class="icon">⏳</div>
        <p><b>ข้อ 3</b><br>คน 10 คน ทำงานชิ้นหนึ่งเสร็จในเวลา 50 วัน ถ้ามีคน 5 คน ทำงานชิ้นนี้ให้เสร็จ จะใช้เวลากี่วัน</p>
        <p class="small" style="margin-top:.6vh">💡 สัดส่วนผกผัน</p>
      </div>
      <div class="ex-item">
        <div class="icon">🏗️</div>
        <p><b>ข้อ 4</b><br>ช่างก่อสร้าง 8 คน ทำงานชิ้นหนึ่งเสร็จในเวลา 5 วัน ถ้ามีช่าง 4 คน ทำงาน 3 ชิ้นนี้ให้เสร็จ จะใช้เวลากี่วัน</p>
        <p class="small" style="margin-top:.6vh">💡 สัดส่วนผกผัน</p>
      </div>
    </div>
    <p class="small" style="margin-top:1.5vh; text-align:center">ลองคิดด้วยตัวเองก่อน แล้วไปดูเฉลยพร้อมวิธีทำในสไลด์ถัดไป</p>
  </div>
  <div class="footer-tag">หมวดที่ 2 · ตัวอย่างจากบทเรียน</div>
</section>

<!-- ============ SLIDE 10 : ANSWERS 1 ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>เฉลย — ลองคิดดูนะครับ (Answers &amp; How)</h2>
  <div class="body">
    <div class="grid2">
      <div class="card">
        <p><b>ข้อ 1</b> 🍜 (ตรง) <span class="frac"><span>80</span><span>4</span></span> =
        <span class="frac"><span>360</span><span>x</span></span> → x = <span class="frac"><span>360×4</span><span>80</span></span> = <span class="num">18 ชาม</span></p>
      </div>
      <div class="card">
        <p><b>ข้อ 2</b> 👷 (ตรง) <span class="frac"><span>5</span><span>35</span></span> =
        <span class="frac"><span>8</span><span>x</span></span> → x = <span class="frac"><span>35×8</span><span>5</span></span> = <span class="num">56 เมตร</span></p>
      </div>
      <div class="card">
        <p><b>ข้อ 3</b> ⏳ (ผกผัน) คนลดจาก 10 → 5 (กลับอัตราส่วน) → x = <span class="frac"><span>10×50</span><span>5</span></span> = <span class="num">100 วัน</span></p>
      </div>
      <div class="card">
        <p><b>ข้อ 4</b> 🏗️ (ผกผัน) ช่าง 8 → 4 คน และงานเพิ่มเป็น 3 ชิ้น → x = <span class="frac"><span>8×5×3</span><span>4</span></span> = <span class="num">30 วัน</span></p>
      </div>
    </div>
    <div class="stepbox" style="margin-top:1.5vh">
      <p class="small">ข้อสังเกต: ข้อ 3–4 เป็น<b>สัดส่วนผกผัน</b> จึงต้อง<b>กลับอัตราส่วน</b>ก่อนคูณ — ถ้าคิดตรง ๆ จะผิดทันที</p>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · เฉลยตัวอย่าง</div>
</section>

<!-- ============ SLIDE 11 : CONTINUED RATIO EXPLAIN ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>อัตราส่วนต่อเนื่อง (Continued Ratio)</h2>
  <div class="body">
    <div class="card" style="margin-bottom:1.5vh">
      <p><b>ความหมาย:</b> อัตราส่วนของจำนวน<b>ตั้งแต่ 3 จำนวนขึ้นไป</b>เขียนต่อเนื่องกัน เช่น a : b : c</p>
      <p><b>การเชื่อมอัตราส่วน:</b> ทำ<b>ตัวเชื่อม (ตัวแปรร่วม)</b> ให้มีค่าเท่ากันก่อน</p>
    </div>
    <div class="grid2">
      <div class="card" style="border-left:6px solid var(--teal)">
        <h3>ตัวอย่าง ✏️ ดินสอ : ปากกา : สมุด</h3>
        <p>ดินสอ : ปากกา = 3 : 5</p>
        <p>ปากกา : สมุด = 4 : 7</p>
        <div class="stepbox">
          <p class="small">ปากกาคือตัวเชื่อม → ทำให้เป็น 20 (LCM ของ 5 กับ 4)</p>
          <p class="small">ดินสอ : ปากกา = 3:5 = <b>12 : 20</b></p>
          <p class="small">ปากกา : สมุด = 4:7 = <b>20 : 35</b></p>
        </div>
        <p style="margin-top:.8vh">ตอบ: ดินสอ : ปากกา : สมุด = <span class="num">12 : 20 : 35</span></p>
      </div>
      <div class="card" style="border-left:6px solid var(--teal)">
        <h3>ตัวอย่าง 📦 กว้าง : ยาว : สูง</h3>
        <p>ความกว้าง : ความยาว = 5 : 8</p>
        <p>ความสูง : ความยาว = 4 : 6</p>
        <div class="stepbox">
          <p class="small">ยาวคือตัวเชื่อม → ทำให้เป็น 24</p>
          <p class="small">กว้าง : ยาว = 5:8 = <b>15 : 24</b></p>
          <p class="small">สูง : ยาว = 4:6 = 2:3 = <b>16 : 24</b></p>
        </div>
        <p style="margin-top:.8vh">ตอบ: กว้าง : ยาว : สูง = <span class="num">15 : 24 : 16</span></p>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · อัตราส่วนต่อเนื่อง (Continued Ratio)</div>
</section>

<!-- ============ SLIDE 12 : REAL-WORLD PROBLEMS ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>โจทย์ประยุกต์ในชีวิตจริง (Real-World Problems)</h2>
  <div class="body">
    <div class="grid2" style="gap:1vw">
      <div class="card"><p><b>📈 โจทย์เรื่องหุ้นส่วน</b><br>พีระถือหุ้น <span class="frac"><span>1</span><span>4</span></span> มานะถือ <span class="frac"><span>2</span><span>5</span></span> ของทั้งหมด อารีถือส่วนที่เหลือ ถ้ากำไรสุทธิ 2,400,000 บาท อารีจะได้รับส่วนแบ่งกำไรกี่บาท</p></div>
      <div class="card"><p><b>🪵 การบริหารวัตถุดิบเหลือใช้</b><br>โรงงานมีไม้ซุง 8.4 ตัน เดือนแรกใช้ไป <span class="frac"><span>2</span><span>7</span></span> ของทั้งหมด จะเหลือวัตถุดิบกี่กิโลกรัม (1 ตัน = 1,000 กก.)</p></div>
      <div class="card"><p><b>💹 การคำนวณต้นทุนซื้อหลักทรัพย์</b><br>ซื้อหุ้น 2,500 หุ้น ราคาหุ้นละ 25.50 บาท ค่าธรรมเนียม 0.20% ของยอดซื้อ ต้องเตรียมเงินทั้งหมดกี่บาท</p></div>
      <div class="card"><p><b>🏦 การคำนวณดอกเบี้ยเงินกู้ระยะสั้น</b><br>กู้ 1,500,000 บาท ดอกเบี้ย 6% ต่อปี ครบกำหนดเมื่อ <span class="frac"><span>2</span><span>3</span></span> ของปี ต้องจ่ายดอกเบี้ยกี่บาท</p></div>
      <div class="card" style="grid-column:1/-1"><p><b>🧾 การคำนวณราคาสุทธิหลังหักส่วนลดและรวมภาษี</b><br>เครื่องจักรราคาป้าย 80,000 บาท ให้ส่วนลด <span class="frac"><span>1</span><span>10</span></span> ของราคาป้าย แล้วบวก VAT 7% ของราคาหลังหักส่วนลด — ต้องจ่ายเงินสุทธิกี่บาท</p></div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · โจทย์ประยุกต์ (เฉลยในสไลด์ถัดไป)</div>
</section>

<!-- ============ SLIDE 13 : ANSWERS REAL-WORLD ============ -->
<section class="slide" style="--accent:var(--teal)">
  <h2>เฉลยโจทย์ประยุกต์ (Answers)</h2>
  <div class="body">
    <div class="grid2" style="gap:1vw">
      <div class="card ansline"><p><b>หุ้นส่วน:</b> พีระ+มานะ = <span class="frac"><span>1</span><span>4</span></span>+<span class="frac"><span>2</span><span>5</span></span> = <span class="frac"><span>13</span><span>20</span></span> → อารีได้ <span class="frac"><span>7</span><span>20</span></span> = 2,400,000 × <span class="frac"><span>7</span><span>20</span></span> = <span class="num">840,000 บาท</span></p></div>
      <div class="card ansline"><p><b>ไม้ซุง:</b> ใช้ไป <span class="frac"><span>2</span><span>7</span></span> เหลือ <span class="frac"><span>5</span><span>7</span></span> → 8.4 × <span class="frac"><span>5</span><span>7</span></span> = 6 ตัน = <span class="num">6,000 กิโลกรัม</span></p></div>
      <div class="card ansline"><p><b>หลักทรัพย์:</b> 2,500 × 25.50 = 63,750 บาท ค่าธรรมเนียม 63,750 × 0.20% = 127.50 → รวม <span class="num">63,877.50 บาท</span></p></div>
      <div class="card ansline"><p><b>ดอกเบี้ย:</b> 1,500,000 × 6% × <span class="frac"><span>2</span><span>3</span></span> = <span class="num">60,000 บาท</span></p></div>
      <div class="card ansline" style="grid-column:1/-1"><p><b>เครื่องจักร:</b> หักส่วนลด 80,000 × <span class="frac"><span>9</span><span>10</span></span> = 72,000 บาท แล้วบวก VAT 7% → 72,000 × 1.07 = <span class="num">77,040 บาท</span></p></div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 2 · เฉลยโจทย์ประยุกต์</div>
</section>

<!-- ============ SLIDE 14 : DIVIDER 3 ============ -->
<section class="slide divider d3">
  <div class="center">
    <div class="big-num">03</div>
    <h1>ร้อยละ</h1>
    <p style="color:#fed7aa;font-family:'Kanit';font-size:clamp(15px,2.6vmin,24px)">Percentage</p>
  </div>
</section>

<!-- ============ SLIDE 15 : PERCENTAGE DEFINITION ============ -->
<section class="slide" style="--accent:var(--orange)">
  <h2>นิยามของร้อยละ (Definition of Percentage)</h2>
  <div class="body">
    <div class="card" style="text-align:center;background:#fff7ed;border:2px solid var(--orange)">
      <p style="font-family:'Kanit';font-size:clamp(16px,3vmin,26px)">ร้อยละ หมายถึง <b>"ต่อร้อย"</b> — อัตราส่วนที่มีจำนวนหลังเป็น 100</p>
      <p style="margin-top:1vh">เช่น <span class="frac"><span>85</span><span>100</span></span> หรือ 85 : 100 หมายถึง ร้อยละ 85 หรือ <b>85%</b></p>
    </div>
    <div class="grid2" style="margin-top:2vh">
      <div class="ex-item">
        <div class="icon">🖊️</div>
        <p>ปากกาทั้งหมด 100 ด้าม เป็นสีแดง 30 ด้าม</p>
        <p>คิดเป็นปากกาสีแดงร้อยละ 30 หรือ <span class="num">30%</span></p>
      </div>
      <div class="ex-item">
        <div class="icon">📝</div>
        <p>สมชาติสอบได้ 76% หมายความว่า</p>
        <p>ถ้าคะแนนเต็ม 100 คะแนน สมชาติสอบได้ <span class="num">76 คะแนน</span></p>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 3 · ร้อยละ (Percentage)</div>
</section>

<!-- ============ SLIDE 16 : PERCENTAGE PROBLEMS ============ -->
<section class="slide" style="--accent:var(--orange)">
  <h2>โจทย์ปัญหาร้อยละ (Percentage Problems)</h2>
  <div class="body">
    <div class="grid2">
      <div class="card">
        <h3>จากบทเรียน 📚</h3>
        <ol class="qlist">
          <li>โรงเรียนมีนักเรียนชายคิดเป็น 24% ของนักเรียนทั้งหมด ถ้ามีนักเรียนทั้งหมด 1,800 คน จะเป็นนักเรียนชายกี่คน</li>
          <li>พ่อค้าซื้อกางเกงราคาตัวละ 450 บาท ขายไปได้กำไร 20% คิดเป็นกำไรกี่บาท</li>
          <li>20% ของ 150 มีค่ามากกว่า 10% ของ 190 เท่าใด</li>
        </ol>
      </div>
      <div class="card">
        <h3>ลองคิดดูนะครับ 🤔</h3>
        <ol class="qlist">
          <li>จงหาว่า 8% ของ 75 เท่ากับเท่าใด</li>
          <li>จงหาว่า 6 เป็นกี่เปอร์เซ็นต์ของ 40</li>
          <li>แม่ค้าลดราคาสินค้าจาก 50 บาท เหลือ 40 บาท ถามว่าผู้ซื้อจะประหยัดกี่เปอร์เซ็นต์</li>
          <li>โซฟาราคา 200 บาท ลดราคา 20% แล้วลดอีก 20% ผู้ซื้อจะซื้อในราคาสุทธิได้กี่บาท</li>
          <li>ซื้อสินค้า 2 ชิ้น ขายไปชิ้นละ 4,800 บาท ได้กำไรจากชิ้นแรก 20% และขาดทุนจากชิ้นที่ 2 เท่ากับ 20% — ขายทั้งสองชิ้นได้กำไรหรือขาดทุนกี่บาท</li>
        </ol>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 3 · ร้อยละ (เฉลยในสไลด์ถัดไป)</div>
</section>

<!-- ============ SLIDE 17 : PERCENTAGE ANSWERS ============ -->
<section class="slide" style="--accent:var(--orange)">
  <h2>เฉลยโจทย์ร้อยละ (Answers)</h2>
  <div class="body">
    <div class="grid2" style="gap:1vw;align-items:start">
      <div class="card">
        <div class="sec-head">จากบทเรียน 📚</div>
        <p class="small" style="margin-bottom:1.2vh"><span class="qnum">1</span><b>นักเรียนชาย 24% ของนักเรียนทั้งหมด 1,800 คน</b><br>1,800 × 24% = <span class="num">432 คน</span></p>
        <p class="small" style="margin-bottom:1.2vh"><span class="qnum">2</span><b>พ่อค้าซื้อกางเกงราคา 450 บาท ขายได้กำไร 20%</b><br>450 × 20% = <span class="num">90 บาท</span></p>
        <p class="small"><span class="qnum">3</span><b>20% ของ 150 มากกว่า 10% ของ 190 เท่าใด</b><br>(150 × 20%) − (190 × 10%) = 30 − 19 = <span class="num">มากกว่า 11</span></p>
      </div>
      <div class="card">
        <div class="sec-head p">ลองคิดดูนะครับ 🤔</div>
        <p class="small" style="margin-bottom:1vh"><span class="qnum p">1</span><b>8% ของ 75 เท่ากับเท่าใด</b><br>75 × 8% = <span class="num">6</span></p>
        <p class="small" style="margin-bottom:1vh"><span class="qnum p">2</span><b>6 เป็นกี่เปอร์เซ็นต์ของ 40</b><br>6 ÷ 40 × 100 = <span class="num">15%</span></p>
        <p class="small" style="margin-bottom:1vh"><span class="qnum p">3</span><b>ลดราคาจาก 50 บาท เหลือ 40 บาท ประหยัดกี่%</b><br>(50 − 40) ÷ 50 × 100 = <span class="num">20%</span></p>
        <p class="small" style="margin-bottom:1vh"><span class="qnum p">4</span><b>โซฟาราคา 200 บาท ลด 20% แล้วลดอีก 20%</b><br>200 × 0.8 × 0.8 = <span class="num">128 บาท</span> <span style="color:var(--red);font-weight:700">(ไม่ใช่ลด 40%)</span></p>
        <p class="small"><span class="qnum p">5</span><b>ซื้อสินค้า 2 ชิ้น ขายไปชิ้นละ 4,800 บาท</b><br>ชิ้นแรกกำไร 20% → ทุน 4,000 (กำไร 800)<br>ชิ้นที่สองขาดทุน 20% → ทุน 6,000 (ขาดทุน 1,200)<br>รวม = <span class="num" style="color:var(--red)">ขาดทุน 400 บาท</span></p>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 3 · เฉลยโจทย์ร้อยละ</div>
</section>

<!-- ============ SLIDE 18 : DIVIDER 4 ============ -->
<section class="slide divider d4">
  <div class="center">
    <div class="big-num">04</div>
    <h1>แบบฝึกหัด แบบทดสอบ</h1>
    <p style="color:#ddd6fe;font-family:'Kanit';font-size:clamp(15px,2.6vmin,24px)">Quiz — กดเลือกคำตอบ แล้วดูเฉลยพร้อมวิธีทำทันที</p>
  </div>
</section>

<!-- ============ SLIDE 19 : QUIZ 1 ============ -->
<section class="slide" style="--accent:var(--purple)">
  <h2>Quiz 1 🥚 อัตราส่วนต่อเนื่อง</h2>
  <div class="body">
    <div class="card" style="margin-bottom:1.5vh">
      <p>แม่ค้าซื้อไข่มา <b>220 ใบ</b> มีอัตราส่วนของจำนวนไข่ขนาดใบใหญ่ : ใบกลาง : ใบเล็ก เป็น <b>3 : 2 : 5</b> แล้วจงหาจำนวนไข่ขนาดใบกลาง</p>
    </div>
    <button class="opt" onclick="pick(this,false)">ก) 44 ใบ &nbsp;&nbsp;ไม่ใช่ข้อนี้ — 44 ใบคือไข่ใบเล็กครึ่งเดียว</button>
    <button class="opt" onclick="pick(this,true)">ข) 44 ใบ… อ่านดี ๆ คือ <b>ใบกลาง</b> = 220 × 2/10 = 44 ใบ</button>
    <button class="opt" onclick="pick(this,false)">ค) 66 ใบ</button>
    <div class="explain">
      <p><b>เฉลย + วิธีทำ:</b> ผลรวมอัตราส่วน = 3 + 2 + 5 = 10 ส่วน<br>
      ใบใหญ่ = 220 × 3/10 = 66 ใบ · <b>ใบกลาง = 220 × 2/10 = 44 ใบ</b> · ใบเล็ก = 220 × 5/10 = 110 ใบ</p>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 4 · แบบฝึกหัด (Quiz)</div>
</section>

<!-- ============ SLIDE 20 : QUIZ 2 ============ -->
<section class="slide" style="--accent:var(--purple)">
  <h2>Quiz 2 ✖️ อัตราส่วนกับตัวแปร</h2>
  <div class="body">
    <div class="card" style="margin-bottom:1.5vh">
      <p>ถ้า <b>3x = 2k</b> และ <b>5y = 8k</b> แล้วจงหาอัตราส่วนของ <b>x : y</b></p>
    </div>
    <button class="opt" onclick="pick(this,true)">ก) x : y = <b>5 : 12</b></button>
    <button class="opt" onclick="pick(this,false)">ข) x : y = 12 : 5</button>
    <button class="opt" onclick="pick(this,false)">ค) x : y = 3 : 5</button>
    <div class="explain">
      <p><b>เฉลย + วิธีทำ:</b> x = <span class="frac"><span>2k</span><span>3</span></span> และ y = <span class="frac"><span>8k</span><span>5</span></span><br>
      x : y = <span class="frac"><span>2k</span><span>3</span></span> : <span class="frac"><span>8k</span><span>5</span></span> = <span class="frac"><span>2</span><span>3</span></span> × <span class="frac"><span>5</span><span>8</span></span> = <span class="frac"><span>10</span><span>24</span></span> = <b>5 : 12</b></p>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 4 · แบบฝึกหัด (Quiz)</div>
</section>

<!-- ============ SLIDE 21 : QUIZ 3 ============ -->
<section class="slide" style="--accent:var(--purple)">
  <h2>Quiz 3 🔊 ร้อยละกับการลดราคา</h2>
  <div class="body">
    <div class="card" style="margin-bottom:1.5vh">
      <p>เครื่องเสียงชุดหนึ่งปิดราคา <b>4,200 บาท</b> ถ้าลดราคา <b>30%</b> จะขายกี่บาท</p>
    </div>
    <button class="opt" onclick="pick(this,false)">ก) 3,780 บาท</button>
    <button class="opt" onclick="pick(this,false)">ข) 3,360 บาท</button>
    <button class="opt" onclick="pick(this,true)">ค) <b>2,940 บาท</b></button>
    <div class="explain">
      <p><b>เฉลย + วิธีทำ:</b> ลด 30% แสดงว่าขายที่ราคา 70% ของราคาปิด<br>
      4,200 × <span class="frac"><span>70</span><span>100</span></span> = <b>2,940 บาท</b></p>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 4 · แบบฝึกหัด (Quiz)</div>
</section>

<!-- ============ SLIDE 22 : QUIZ ANSWER SUMMARY ============ -->
<section class="slide" style="--accent:var(--purple)">
  <h2>สรุปคำตอบ Quiz (Answer Summary)</h2>
  <div class="body">
    <div class="grid3">
      <div class="card" style="border-top:6px solid var(--purple);text-align:center">
        <p style="font-size:clamp(26px,5vmin,48px)">🥚</p>
        <p><b>ข้อ 1</b><br>ไข่ใบกลาง = <span class="num">44 ใบ</span><br><span class="small">(66 : 44 : 110)</span></p>
      </div>
      <div class="card" style="border-top:6px solid var(--purple);text-align:center">
        <p style="font-size:clamp(26px,5vmin,48px)">✖️</p>
        <p><b>ข้อ 2</b><br>x : y = <span class="num">5 : 12</span><br><span class="small">จาก 3x = 2k, 5y = 8k</span></p>
      </div>
      <div class="card" style="border-top:6px solid var(--purple);text-align:center">
        <p style="font-size:clamp(26px,5vmin,48px)">🔊</p>
        <p><b>ข้อ 3</b><br>ขายได้ <span class="num">2,940 บาท</span><br><span class="small">4,200 × 70%</span></p>
      </div>
    </div>
  </div>
  <div class="footer-tag">หมวดที่ 4 · แบบฝึกหัด (Quiz)</div>
</section>

<!-- ============ SLIDE 23 : END ============ -->
<section class="slide title-slide">
  <div class="center">
    <h1>จบบทเรียน 🎉</h1>
    <p class="sub" style="margin-top:2vh;font-size:clamp(15px,2.8vmin,24px)">เศษส่วน · อัตราส่วน · ร้อยละ</p>
    <p class="sub" style="margin-top:2vh">Fractions · Ratio · Percentage — พบกันใหม่ครับ</p>
  </div>
</section>

</div>

<div id="bar"></div>
<div id="nav">
  <button onclick="go(-1)">◀ ก่อนหน้า</button>
  <span id="counter"></span>
  <button onclick="go(1)">ถัดไป ▶</button>
</div>

<script>
const slides=[...document.querySelectorAll('.slide')];
let cur=0;
function show(i){
  cur=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,idx)=>s.classList.toggle('active',idx===cur));
  document.getElementById('counter').textContent=(cur+1)+' / '+slides.length;
  document.getElementById('bar').style.width=((cur+1)/slides.length*100)+'%';
  // sidebar active state
  let sec='home';
  if(cur>=2&&cur<=4)sec='t1';
  else if(cur>=5&&cur<=12)sec='t2';
  else if(cur>=13&&cur<=16)sec='t3';
  else if(cur>=17&&cur<=slides.length-1)sec='t4';
  document.querySelectorAll('.sb-item').forEach(b=>{b.classList.toggle('active',b.classList.contains(sec))});
}
function go(d){show(cur+d)}
document.querySelectorAll('.sb-item').forEach(b=>b.addEventListener('click',()=>show(parseInt(b.dataset.i,10))));
function toggleSidebar(){
  const sb=document.getElementById('sidebar');
  const tg=document.getElementById('toggle');
  const coll=document.getElementById('deck');
  sb.classList.toggle('collapsed');
  tg.classList.toggle('collapsed');
  coll.classList.toggle('shifted');
  tg.textContent=sb.classList.contains('collapsed')?'▶':'◀';
}
document.addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(1)}
  if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(-1)}
  if(e.key==='Home')show(0);
  if(e.key==='End')show(slides.length-1);
});
function pick(btn,correct){
  const box=btn.closest('.body');
  box.querySelectorAll('.opt').forEach(b=>{b.disabled=true;b.classList.remove('correct','wrong')});
  btn.classList.add(correct?'correct':'wrong');
  if(!correct){box.querySelectorAll('.opt')[[...box.querySelectorAll('.opt')].findIndex(b=>b.onclick.toString().includes('true'))]?.classList.add('correct');}
  box.querySelector('.explain').classList.add('show');
}
/* ===== interactive v2 ===== */
const SS=i=>slides[i];
function graphSVG(cfg){
  const W=440,H=225,L=46,B=34,T=28,R=18;
  const xs=cfg.pts.map(p=>p[0]), ys=cfg.pts.map(p=>p[1]);
  const xmax=Math.max.apply(null,xs)*1.3, ymax=Math.max.apply(null,ys)*1.35;
  const X=v=>L+(v/xmax)*(W-L-R), Y=v=>H-B-(v/ymax)*(H-B-T);
  const c=cfg.color||'#2563eb';
  let s='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg" style="font-family:Sarabun,sans-serif">';
  for(let i=1;i<=4;i++){
    const gx=L+(i/4)*(W-L-R), gy=H-B-(i/4)*(H-B-T);
    s+='<line x1="'+gx.toFixed(1)+'" y1="'+T+'" x2="'+gx.toFixed(1)+'" y2="'+(H-B)+'" stroke="#eef2f7"/>';
    s+='<line x1="'+L+'" y1="'+gy.toFixed(1)+'" x2="'+(W-R)+'" y2="'+gy.toFixed(1)+'" stroke="#eef2f7"/>';
  }
  s+='<line x1="'+L+'" y1="'+(H-B)+'" x2="'+(W-R)+'" y2="'+(H-B)+'" stroke="#94a3b8" stroke-width="1.6"/>';
  s+='<line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(H-B)+'" stroke="#94a3b8" stroke-width="1.6"/>';
  if(cfg.title) s+='<text x="'+L+'" y="'+(T-9)+'" font-size="13" font-weight="700" fill="#334155">'+cfg.title+'</text>';
  if(cfg.type==='inv'){
    const k=xs[0]*ys[0]; let d='';
    for(let i=0;i<=160;i++){
      const x=0.12+(xmax-0.12)*i/160, y=k/x;
      if(y>ymax){continue}
      d+=(d===''?'M':' L')+X(x).toFixed(1)+' '+Y(y).toFixed(1);
    }
    s+='<path d="'+d+'" fill="none" stroke="'+c+'" stroke-width="2.6" stroke-linecap="round"/>';
  }else{
    const k=ys[0]/xs[0];
    s+='<line x1="'+X(0).toFixed(1)+'" y1="'+Y(0).toFixed(1)+'" x2="'+X(xmax).toFixed(1)+'" y2="'+Y(k*xmax).toFixed(1)+'" stroke="'+c+'" stroke-width="2.6" stroke-linecap="round"/>';
  }
  cfg.pts.forEach((p,i)=>{
    s+='<circle cx="'+X(p[0]).toFixed(1)+'" cy="'+Y(p[1]).toFixed(1)+'" r="4.6" fill="'+c+'" stroke="#fff" stroke-width="1.7"/>';
    const lb=cfg.labels&&cfg.labels[i];
    if(lb){ const tx=Math.min(X(p[0])+9,W-150);
      s+='<text x="'+tx.toFixed(1)+'" y="'+(Y(p[1])-8).toFixed(1)+'" font-size="12" font-weight="700" fill="'+c+'">'+lb+'</text>'; }
  });
  s+='<text x="'+(W-R)+'" y="'+(H-B+20)+'" text-anchor="end" font-size="11" fill="#64748b">'+cfg.xLabel+'</text>';
  s+='<text x="'+(L-10)+'" y="'+(T+9)+'" text-anchor="end" font-size="11" fill="#64748b">'+cfg.yLabel+'</text>';
  s+='</svg>';
  return s;
}
function pieSVG(segs){
  const cx=110,cy=110,Rr=88,total=segs.reduce((a,b)=>a+b.v,0);
  let ang=-Math.PI/2;
  let s='<svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" style="font-family:Sarabun,sans-serif">';
  segs.forEach(g=>{
    const a=g.v/total*Math.PI*2;
    if(a>=Math.PI*1.999){ s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+Rr+'" fill="'+g.c+'"/>'; }
    else{
      const x1=cx+Rr*Math.cos(ang), y1=cy+Rr*Math.sin(ang), a2=ang+a;
      const x2=cx+Rr*Math.cos(a2), y2=cy+Rr*Math.sin(a2);
      const lg=a>Math.PI?1:0;
      s+='<path d="M'+cx+' '+cy+' L'+x1.toFixed(1)+' '+y1.toFixed(1)+' A'+Rr+' '+Rr+' 0 '+lg+' 1 '+x2.toFixed(1)+' '+y2.toFixed(1)+' Z" fill="'+g.c+'" stroke="#fff" stroke-width="2.5"/>';
    }
    const mid=ang+a/2, mx=cx+Rr*0.6*Math.cos(mid), my=cy+Rr*0.6*Math.sin(mid);
    s+='<text x="'+mx.toFixed(1)+'" y="'+(my+6).toFixed(1)+'" text-anchor="middle" font-size="18" font-weight="700" fill="'+(g.dark?'#475569':'#ffffff')+'">'+g.t+'</text>';
    ang+=a;
  });
  return s+'</svg>';
}
/* 1) agenda cards jump to their section */
(function(){
  const cards=[].slice.call(SS(1).querySelectorAll('.card')), tgt=[2,5,13,17];
  cards.forEach((c,i)=>{
    c.classList.add('link');
    const h=document.createElement('div'); h.className='hint'; h.textContent='กดเพื่อไปหมวดนี้ \u2192';
    c.appendChild(h);
    c.addEventListener('click',()=>show(tgt[i]));
  });
})();
/* 2) set-symbol examples */
const SYMD=[
 {n:'R \u2014 เซตของจำนวนจริง (Real Numbers)',ex:'\u22123 , 0 , \u00bd , 2.5 , \u221a2 , \u03c0 , e',w:'จำนวนจริง = จำนวนตรรกยะ (Q) รวมกับจำนวนอตรรกยะ (Q\u2032) ครอบคลุมทุกจำนวนบนเส้นจำนวน'},
 {n:'R\u207a \u2014 จำนวนจริงบวก (Positive Real Numbers)',ex:'0.5 , 1 , 2.75 , \u221a3 , \u03c0',w:'จำนวนจริงที่มีค่ามากกว่าศูนย์ (ไม่รวม 0)'},
 {n:'R\u207b \u2014 จำนวนจริงลบ (Negative Real Numbers)',ex:'\u22120.5 , \u22121 , \u22122.75 , \u2212\u221a3 , \u2212\u03c0',w:'จำนวนจริงที่มีค่าน้อยกว่าศูนย์ (ไม่รวม 0)'},
 {n:'Q \u2014 เซตของจำนวนตรรกยะ (Rational Numbers)',ex:'\u00bd , \u22123 , 0.75 , 0.333\u2026 , 22\u20447',w:'เขียนในรูปเศษส่วน a/b ได้ เมื่อ a, b เป็นจำนวนเต็ม และ b \u2260 0 (ทศนิยมรู้จบหรือซ้ำ)'},
 {n:'Q\u2032 \u2014 เซตของจำนวนอตรรกยะ (Irrational Numbers)',ex:'\u221a2 , \u221a3 , \u03c0 , e , 0.1010010001\u2026',w:'เขียนเป็นเศษส่วนไม่ได้ \u2014 ทศนิยมไม่รู้จบและไม่ซ้ำ'},
 {n:'N \u2014 เซตของจำนวนนับ (Natural Numbers)',ex:'1 , 2 , 3 , 4 , 5 , \u2026',w:'จำนวนที่ใช้นับสิ่งของ เริ่มจาก 1'},
 {n:'I \u2014 เซตของจำนวนเต็ม (Integers)',ex:'\u2026 , \u22123 , \u22122 , \u22121 , 0 , 1 , 2 , 3 , \u2026',w:'จำนวนเต็มบวก รวมศูนย์ และจำนวนเต็มลบ ไม่มีทศนิยมหรือเศษส่วน'},
 {n:'I\u207a / I\u207b \u2014 จำนวนเต็มบวก / จำนวนเต็มลบ',ex:'I\u207a = 1, 2, 3, \u2026 \u00b7 I\u207b = \u22121, \u22122, \u22123, \u2026',w:'โดย 0 ไม่นับเป็นจำนวนเต็มบวกหรือจำนวนเต็มลบ'}
];
(function(){
  const grid=SS(4).querySelector('.grid4'); if(!grid)return;
  const box=document.createElement('div'); box.className='bubble';
  grid.insertAdjacentElement('afterend',box);
  const cards=[].slice.call(grid.querySelectorAll('.sym'));
  cards.forEach((c,i)=>c.addEventListener('click',()=>{
    const d=SYMD[i];
    box.innerHTML='<h3>'+d.n+'</h3><p class="ex">ตัวอย่าง: '+d.ex+'</p><p class="why">'+d.w+'</p>';
    box.classList.add('show');
    cards.forEach((x,k)=>x.classList.toggle('on',k===i));
  }));
})();
/* 3) slide 7 : direct & inverse proportion graphs */
(function(){
  const cards=[].slice.call(SS(6).querySelectorAll('.grid2 > .card'));
  const G=[
   {type:'line',pts:[[2,40],[4,80],[6,120]],labels:['','4 ชาม = 80 บาท',''],xLabel:'จำนวนบะหมี่ (ชาม)',yLabel:'ราคา (บาท)',color:'#0d9488',title:'สัดส่วนตรง \u2014 เส้นตรงผ่านจุดกำเนิด (y = kx)'},
   {type:'inv',pts:[[2,20],[5,8],[8,5]],labels:['2 คน = 20 วัน','','8 คน = 5 วัน'],xLabel:'จำนวนคนงาน (คน)',yLabel:'เวลา (วัน)',color:'#ea580c',title:'สัดส่วนผกผัน \u2014 เส้นโค้งไฮเพอร์โบลา (y = k/x)'}
  ];
  cards.forEach((c,i)=>{ const g=document.createElement('div'); g.className='mini-graph show'; g.innerHTML=graphSVG(G[i]); c.appendChild(g); });
})();
/* 4) slide 10 : click an answer -> its own line graph */
(function(){
  const body=SS(9).querySelector('.body');
  const cards=[].slice.call(body.querySelectorAll('.grid2 > .card'));
  const note=body.querySelector('.stepbox');
  const panel=document.createElement('div'); panel.className='mini-graph';
  body.insertBefore(panel,note);
  const G=[
   {type:'line',pts:[[4,80],[18,360]],labels:['4 ชาม = 80 บาท','18 ชาม = 360 บาท'],xLabel:'จำนวนบะหมี่ (ชาม)',yLabel:'เงิน (บาท)',color:'#0d9488',title:'ข้อ 1 \u00b7 สัดส่วนตรง \u2192 18 ชาม'},
   {type:'line',pts:[[5,35],[8,56]],labels:['5 คน = 35 ม.','8 คน = 56 ม.'],xLabel:'จำนวนช่าง (คน)',yLabel:'ความยาวกำแพง (เมตร)',color:'#0d9488',title:'ข้อ 2 \u00b7 สัดส่วนตรง \u2192 56 เมตร'},
   {type:'inv',pts:[[10,50],[5,100]],labels:['10 คน = 50 วัน','5 คน = 100 วัน'],xLabel:'จำนวนคน (คน)',yLabel:'เวลา (วัน)',color:'#ea580c',title:'ข้อ 3 \u00b7 สัดส่วนผกผัน \u2192 100 วัน'},
   {type:'inv',pts:[[10,12],[4,30]],labels:['','4 คน = 30 วัน'],xLabel:'จำนวนช่าง (คน)',yLabel:'เวลา (วัน)',color:'#ea580c',title:'ข้อ 4 \u00b7 สัดส่วนผกผัน (งาน 3 ชิ้น) \u2192 30 วัน'}
  ];
  cards.forEach((c,i)=>{
    c.classList.add('anscard');
    c.addEventListener('click',()=>{
      cards.forEach(x=>x.classList.remove('on'));
      c.classList.add('on');
      panel.innerHTML=graphSVG(G[i]);
      panel.classList.add('show');
      if(note) note.style.display='none';
    });
  });
})();
/* 5) slide 15 : click an example box -> its pie chart */
(function(){
  const items=[].slice.call(SS(14).querySelectorAll('.grid2 .ex-item'));
  const P=[
   {segs:[{v:30,c:'#dc2626',t:'30%'},{v:70,c:'#e2e8f0',t:'70%',dark:1}],leg:'\U0001F58A\uFE0F แดง 30 ด้าม (30%) \u00b7 อื่น ๆ 70 ด้าม (70%)'},
   {segs:[{v:76,c:'#16a34a',t:'76%'},{v:24,c:'#e2e8f0',t:'24%',dark:1}],leg:'\U0001F4DD สอบได้ 76 คะแนน (76%) \u00b7 ที่เหลือ 24 คะแนน (24%)'}
  ];
  items.forEach((it,i)=>{
    it.style.cursor='pointer';
    const box=document.createElement('div'); box.className='pie-wrap';
    box.innerHTML=pieSVG(P[i].segs)+'<p class="small" style="margin-top:.6vh">'+P[i].leg+'</p>';
    it.appendChild(box);
    it.addEventListener('click',()=>box.classList.toggle('show'));
  });
})();

show(0);
const h=parseInt((location.hash||'#1').slice(1),10);
if(!isNaN(h)&&h>=1&&h<=slides.length)show(h-1);
window.addEventListener('hashchange',()=>{const n=parseInt((location.hash||'#1').slice(1),10);if(!isNaN(n)&&n>=1&&n<=slides.length)show(n-1);});
</script>
</body>
</html>
"""

HTML = HTML.lstrip("\n")


def write_html(path="slides.html"):
    """เขียนไฟล์ slides.html ลงดิสก์ (ใช้ตอนรันแบบ python main.py)"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"สร้างไฟล์ {path} เรียบร้อยแล้ว")


# ตรวจว่ากำลังถูกรันอยู่ภายใต้ `streamlit run main.py` หรือไม่
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    _running_in_streamlit = get_script_run_ctx() is not None
except Exception:
    _running_in_streamlit = False

if _running_in_streamlit:
    # โหมด Streamlit: ปรับแต่งให้แสดงผลเต็มความสูง Viewport และซ่อน Margin ของ Streamlit
    import streamlit as st
    import streamlit.components.v1 as components
    
    st.set_page_config(page_title="เศษส่วน อัตราส่วน ร้อยละ", layout="wide")

    # CSS ฉีดเข้าไปเพื่อลบ Padding และบังคับให้แสดงผลเต็มความสูงหน้าจอ (No Scrollbar)
    st.markdown(
        """
        <style>
            /* ซ่อน Header และ Footer ทั้งหมดของ Streamlit */
            header, footer, #MainMenu {visibility: hidden; height: 0; display: none;}
            
            /* กำหนดองค์ประกอบหลักให้เต็มความสูง 100vh และซ่อน Scrollbar */
            html, body, [data-testid="stAppViewContainer"], .stApp {
                height: 100vh !important;
                width: 100vw !important;
                overflow: hidden !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* ลบ Padding ของ Container หลักใน Streamlit */
            .block-container {
                padding: 0rem !important;
                margin: 0rem !important;
                max-width: 100% !important;
                height: 100vh !important;
            }
            
            /* ปรับแต่ง Element ของ Component iframe ให้เต็มขอบ */
            div[data-testid="stCustomComponentV1"] {
                height: 100vh !important;
                width: 100vw !important;
            }
            
            iframe {
                display: block !important;
                height: 100vh !important;
                width: 100vw !important;
                border: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # แสดงผลสไลด์ผ่าน iframe บังคับความสูงเต็มหน้าจอ
    components.html(HTML, height=0, scrolling=False)

elif __name__ == "__main__":
    # โหมดปกติ: รันด้วย python main.py เพื่อสร้างไฟล์ slides.html
    write_html()