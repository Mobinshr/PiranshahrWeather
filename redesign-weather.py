from pathlib import Path
import re

page = Path("app/src/main/assets/weather.html")
source = page.read_text(encoding="utf-8")
scripts = re.findall(r"<script[^>]*>.*?</script>", source, flags=re.S)
if len(scripts) != 1:
    raise SystemExit("Expected exactly one application script; refusing to replace unknown logic.")
app_script = scripts[0]

css = r"""<style>
:root{color-scheme:light;--bg:#edf5fc;--ink:#18334f;--muted:#7189a2;--line:rgba(42,91,137,.12);--panel:#fff;--blue:#2e83c7;--blue2:#66b4e9;--gold:#f6bf78;--cyan:#7fc9e9;--shadow:0 12px 32px rgba(35,83,128,.08)}
*{box-sizing:border-box;margin:0;padding:0}
[hidden]{display:none!important}
html{background:var(--bg);-webkit-text-size-adjust:100%;overscroll-behavior-y:contain}
body{font-family:Tahoma,"Segoe UI",system-ui,sans-serif;background:radial-gradient(ellipse at 10% 0%,rgba(110,190,239,.18),transparent 35%),linear-gradient(180deg,#f2f8fd 0%,#eaf2f9 100%);color:var(--ink);min-height:100vh;padding:calc(12px + env(safe-area-inset-top)) 0 calc(28px + env(safe-area-inset-bottom));-webkit-font-smoothing:antialiased}
button,select{font:inherit}button{cursor:pointer}button:focus-visible,select:focus-visible{outline:3px solid #f3bd76;outline-offset:3px}
.app{width:100%;max-width:620px;margin:0 auto;display:flex;flex-direction:column;gap:14px;padding:0 14px}
header{position:sticky;top:5px;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 9px 8px 13px;border:1px solid rgba(255,255,255,.8);border-radius:20px;background:rgba(255,255,255,.82);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:0 8px 26px rgba(40,90,135,.07)}
.location{display:flex;align-items:center;gap:10px;min-width:0}.location-icon{width:40px;height:40px;flex:0 0 40px;display:grid;place-items:center;border-radius:14px;background:linear-gradient(145deg,#e2f3ff,#cce8fa);color:#2876b5}.location-icon svg{width:19px;height:19px}.location-info{min-width:0}.city-select{max-width:170px;appearance:none;border:0;background:transparent;color:#183b5d;font-size:1rem;font-weight:800;cursor:pointer}.city-select option{background:#fff;color:#183b5d}.location-info p{margin-top:3px;color:#8198af;font-size:.65rem}.actions{display:flex;align-items:center;gap:6px}.icon-btn{width:38px;height:38px;display:grid;place-items:center;border:1px solid #e1edf6;border-radius:13px;background:#f5faff;color:#477493;transition:transform .18s,background .18s}.icon-btn svg{width:17px;height:17px}.icon-btn:active{transform:scale(.93)}.icon-btn.install-btn{color:#21865c}.icon-btn.notif-btn.active{color:#c17b2b;background:#fff4e5;border-color:#f3d5aa}.icon-btn.spinning svg{animation:spin .9s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.notif-status{display:none!important}.banner{display:flex;align-items:center;gap:10px;padding:12px 14px;border:1px solid var(--line);border-radius:17px;font-size:.75rem;line-height:1.7;background:#fff;box-shadow:var(--shadow)}.banner-rain{background:#fff5eb;border-color:#f5d7bb;color:#80542e}.banner-offline{background:#edf8fd;border-color:#cce8f6;color:#356c8e}.banner-icon{font-size:1.25rem}.banner-body{display:flex;flex-direction:column;gap:2px;flex:1}.banner-body b{font-size:.8rem}.banner-body span{font-size:.7rem;color:#6d849a}.banner-close{border:0;background:transparent;color:inherit;font-size:1.35rem;padding:0 4px}
#content{display:flex;flex-direction:column;gap:14px}#content[hidden]{display:none!important}
#content>.hero{order:1}#content>.stats{order:2}#content>.section:nth-of-type(5){order:3}#content>.section:nth-of-type(6){order:4}#content>.section:nth-of-type(3){order:5}#content>.section:nth-of-type(4){order:6}#content>.sun-row{order:7}
.hero{position:relative;isolation:isolate;overflow:hidden;min-height:250px;padding:25px 24px;border:0;border-radius:27px;background:radial-gradient(circle at 82% 22%,rgba(255,255,255,.27),transparent 28%),linear-gradient(135deg,#72bce9 0%,#438fce 52%,#2c72b4 100%);box-shadow:0 17px 34px rgba(47,119,177,.2);display:grid;grid-template-columns:minmax(0,1fr) 145px;align-items:center;gap:12px;color:#fff}
.hero:before{content:"";position:absolute;z-index:-1;width:250px;height:250px;right:-110px;bottom:-160px;border:1px solid rgba(255,255,255,.2);border-radius:50%;box-shadow:0 0 0 24px rgba(255,255,255,.045),0 0 0 52px rgba(255,255,255,.035)}
.hero:after{content:"";position:absolute;z-index:-1;width:115px;height:115px;left:-48px;top:-55px;border-radius:50%;background:rgba(255,255,255,.08);filter:blur(2px)}
.hero-main{display:flex;flex-direction:column;align-items:flex-start;gap:8px;min-width:0}.hero-main:before{content:"وضعیت فعلی";display:inline-flex;padding:5px 10px;border:1px solid rgba(255,255,255,.3);border-radius:30px;background:rgba(255,255,255,.13);font-size:.67rem;font-weight:700;color:#f5fbff}
.hero-temp{font-size:clamp(4.7rem,17vw,6.4rem);font-weight:300;line-height:.98;letter-spacing:-4px;color:#fff;direction:ltr;text-shadow:0 5px 18px rgba(18,67,112,.12)}.hero-temp sup{font-size:1.15rem;vertical-align:top;letter-spacing:0;margin-left:3px;font-weight:400;color:#e7f5ff}.hero-desc{font-size:1rem;font-weight:800;color:#fff}.hero-feels{font-size:.76rem;color:rgba(255,255,255,.86)}
.hero-icon{font-size:clamp(5rem,18vw,7.2rem);line-height:1;text-align:center;filter:drop-shadow(0 12px 16px rgba(20,70,110,.18));animation:float 5s ease-in-out infinite}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.stat{min-width:0;min-height:92px;padding:13px 12px;border:1px solid rgba(255,255,255,.95);border-radius:17px;background:rgba(255,255,255,.9);box-shadow:0 7px 20px rgba(35,83,128,.055)}.stat-label{display:flex;align-items:center;gap:6px;color:#8297ac;font-size:.66rem;white-space:nowrap}.stat-label svg{width:16px;height:16px;color:#4a9bcf;flex:0 0 auto}.stat-value{margin-top:10px;font-size:1.16rem;line-height:1.2;font-weight:800;color:#244767;overflow-wrap:anywhere}.stat-value .unit{font-size:.68rem;font-weight:600;color:#8398ad}
.section{display:flex;flex-direction:column;gap:9px;min-width:0}.section-title{display:flex;align-items:center;gap:8px;padding:0 2px;color:#244867;font-size:.88rem;font-weight:800}.section-title:before{content:"";width:4px;height:17px;border-radius:8px;background:linear-gradient(180deg,#65b5e5,#f3bd77)}.section-title:after{content:"";height:1px;flex:1;background:linear-gradient(90deg,#d8e6f1,transparent)}
.chart-card{padding:13px 10px 9px;border:1px solid rgba(255,255,255,.95);border-radius:19px;background:#fff;box-shadow:var(--shadow)}.chart-wrap{position:relative;width:100%;height:178px}.chart-wrap.precip{height:132px}.chart-wrap canvas{width:100%;height:100%;display:block}.chart-tooltip{position:absolute;z-index:5;display:none;pointer-events:none;padding:7px 10px;border-radius:10px;background:#214c6f;color:#fff;font-size:.7rem;font-weight:800;box-shadow:0 7px 20px rgba(0,0,0,.13);white-space:nowrap}.chart-tooltip.blue{background:#dff4ff;color:#245a7e}
.hourly-scroll{direction:rtl;display:flex;gap:7px;overflow-x:auto;scroll-snap-type:x proximity;scroll-padding-inline:4px;overscroll-behavior-x:contain;padding:2px 1px 9px;scrollbar-width:thin;scrollbar-color:#bfd5e6 transparent}.hourly-scroll::-webkit-scrollbar{height:4px}.hourly-scroll::-webkit-scrollbar-thumb{background:#bfd5e6;border-radius:5px}.hour-card{scroll-snap-align:start;flex:0 0 70px;min-width:70px;display:flex;flex-direction:column;align-items:center;gap:8px;padding:12px 7px;border:1px solid #e4eef6;border-radius:16px;background:#fff;color:#254969;box-shadow:0 5px 14px rgba(35,83,128,.045)}.hour-card.now{background:#eaf6ff;border-color:#acd7f1;box-shadow:inset 0 0 0 1px rgba(95,172,220,.08)}.hour-card.rainy{border-bottom:2px solid #68b9df}.hour-time{font-size:.67rem;color:#8aa0b5}.hour-icon{font-size:1.55rem;line-height:1.1}.hour-temp{font-size:.95rem;font-weight:800}.hour-pop{font-size:.63rem;color:#3996c8}
.daily-list{overflow:hidden;border:1px solid rgba(255,255,255,.95);border-radius:19px;background:#fff;box-shadow:var(--shadow)}.day-row{display:grid;grid-template-columns:70px 29px minmax(45px,1fr) 66px;align-items:center;gap:7px;padding:13px 11px;border-bottom:1px solid #edf2f7}.day-row:last-child{border-bottom:0}.day-name{font-size:.74rem;font-weight:700;color:#294d6d}.day-name small{display:block;margin-top:3px;font-size:.6rem;font-weight:400;color:#92a5b8}.day-icon{text-align:center;font-size:1.35rem}.day-bar-wrap{display:flex;align-items:center;gap:6px;color:#91a5b8;font-size:.63rem;direction:ltr}.day-bar{height:6px;position:relative;flex:1;min-width:20px;border-radius:8px;background:#e9f0f6;overflow:hidden}.day-bar-fill{position:absolute;top:0;height:100%;border-radius:8px;background:linear-gradient(90deg,#75c5e8,#f2c078)}.day-temps{display:flex;align-items:center;justify-content:flex-end;gap:5px;direction:ltr;font-size:.72rem;font-weight:800}.day-temps .min{color:#9aabbb}.day-temps .max{color:#294d6d}.day-temps .sep{color:#ccd8e3}
.sun-row{display:grid;grid-template-columns:1fr 1fr;gap:9px}.sun-card{display:flex;align-items:center;gap:10px;padding:14px 12px;border:1px solid rgba(255,255,255,.95);border-radius:17px;background:#fff;box-shadow:0 7px 20px rgba(35,83,128,.05)}.sun-icon{font-size:1.65rem}.sun-info{display:flex;flex-direction:column;gap:4px}.sun-label{font-size:.67rem;color:#8aa0b5}.sun-time{font-size:.98rem;font-weight:800;color:#294d6d}
.skeleton-wrap{display:flex;flex-direction:column;gap:12px}.sk{border-radius:20px;background:linear-gradient(100deg,#e1edf6 25%,#f6fbff 40%,#e1edf6 60%);background-size:200% 100%;animation:shimmer 1.4s ease infinite}.sk.hero{height:250px}.sk.stats{height:100px}.sk.chart{height:185px}@keyframes shimmer{to{background-position:-200% 0}}
.error-card{padding:22px;border:1px solid #f1d3d0;border-radius:18px;background:#fff5f3;text-align:center;line-height:1.8;color:#9b4e49}.btn-retry{margin-top:12px;padding:10px 17px;border:0;border-radius:12px;background:#347fb8;color:#fff;font-weight:800}
.toast{position:fixed;z-index:200;bottom:calc(20px + env(safe-area-inset-bottom));left:50%;transform:translate(-50%,20px);opacity:0;max-width:calc(100vw - 32px);padding:12px 16px;border:1px solid #dce8f1;border-radius:14px;background:#fff;color:#244767;font-size:.75rem;font-weight:700;box-shadow:0 12px 32px rgba(30,73,111,.18);pointer-events:none;transition:opacity .25s,transform .25s}.toast.show{opacity:1;transform:translate(-50%,0)}
.inpage-notif-stack{position:fixed;z-index:180;top:calc(10px + env(safe-area-inset-top));left:12px;right:12px;display:flex;flex-direction:column;gap:8px;pointer-events:none}.inpage-notif{display:flex;align-items:center;gap:10px;padding:12px;border:1px solid #d9e7f2;border-radius:16px;background:rgba(255,255,255,.97);box-shadow:0 12px 32px rgba(30,73,111,.18);pointer-events:auto;animation:drop .25s ease}.inpage-notif.out{opacity:0;transform:translateY(-8px);transition:.3s}.inpage-notif-icon{font-size:1.3rem}.inpage-notif-content{flex:1;min-width:0}.inpage-notif-title{font-size:.78rem;font-weight:800;color:#244767}.inpage-notif-body{margin-top:3px;font-size:.69rem;color:#7189a2;line-height:1.6}.inpage-notif-close{border:0;background:transparent;color:#7189a2;font-size:1.2rem}
.pull-indicator{position:fixed;z-index:160;top:calc(8px + env(safe-area-inset-top));left:50%;transform:translate(-50%,-90px);display:flex;align-items:center;gap:9px;padding:10px 15px;border:1px solid #dce8f1;border-radius:25px;background:#fff;color:#7189a2;font-size:.72rem;box-shadow:0 9px 28px rgba(30,73,111,.13);transition:transform .22s;white-space:nowrap;pointer-events:none}.pull-indicator.visible{transform:translate(-50%,0)}.pull-indicator.ready,.pull-indicator.refreshing{color:#347fb8}.pull-spinner{width:15px;height:15px;border:2px solid #dce8f1;border-top-color:#347fb8;border-radius:50%}.pull-indicator.refreshing .pull-spinner{animation:spin .8s linear infinite}
footer{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 12px;padding:12px 3px 2px;border-top:1px solid #dce8f1;color:#91a4b7;font-size:.64rem;line-height:1.8}footer b{color:#56738f;font-weight:700}
@keyframes drop{from{opacity:0;transform:translateY(-7px)}to{opacity:1;transform:none}}
@media(max-width:560px){body{padding-top:calc(8px + env(safe-area-inset-top))}.app{gap:12px;padding:0 11px}header{padding:7px 8px 7px 10px;border-radius:17px}.location-icon{width:36px;height:36px;flex-basis:36px;border-radius:12px}.city-select{font-size:.94rem;max-width:130px}.location-info p{font-size:.61rem}.icon-btn{width:35px;height:35px;border-radius:12px}.hero{min-height:226px;padding:21px 17px;border-radius:23px;grid-template-columns:minmax(0,1fr) 112px}.hero-temp{font-size:clamp(4.4rem,18vw,5.5rem)}.hero-icon{font-size:5.2rem}.stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.stat{min-height:84px;padding:11px;border-radius:15px}.stat-label{font-size:.64rem}.stat-value{font-size:1.08rem;margin-top:8px}.section-title{font-size:.83rem}.chart-card{padding:10px 8px 7px;border-radius:17px}.chart-wrap{height:160px}.chart-wrap.precip{height:122px}.hour-card{flex-basis:65px;min-width:65px;padding:10px 6px}.day-row{grid-template-columns:59px 25px minmax(34px,1fr) 60px;gap:5px;padding:11px 8px}.day-name{font-size:.68rem}.day-name small{font-size:.57rem}.day-icon{font-size:1.2rem}.day-bar-wrap{gap:4px;font-size:.59rem}.day-temps{gap:3px;font-size:.66rem}.sun-card{padding:12px 10px;gap:8px}.sun-icon{font-size:1.45rem}.sun-time{font-size:.88rem}}
@media(max-width:365px){.city-select{max-width:105px;font-size:.86rem}.hero{grid-template-columns:minmax(0,1fr) 88px;padding-inline:13px}.hero-temp{font-size:3.9rem}.hero-icon{font-size:4.3rem}.day-row{grid-template-columns:52px 22px minmax(27px,1fr) 55px;gap:4px;padding-inline:6px}.day-temps{font-size:.62rem}}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#0d1b2a;--ink:#eaf3fb;--muted:#93a9bd;--line:rgba(190,215,238,.12);--panel:#172a3e;--shadow:0 12px 30px rgba(0,0,0,.16)}html{background:#0d1b2a}body{background:radial-gradient(ellipse at 10% 0%,rgba(63,126,177,.17),transparent 36%),linear-gradient(180deg,#102238,#0d1b2a);color:#eaf3fb}header{background:rgba(20,39,59,.88);border-color:rgba(190,215,238,.12)}.city-select{color:#eaf3fb}.city-select option{background:#172a3e;color:#eaf3fb}.location-info p,.stat-label,.sun-label,.hour-time,.day-name small,.day-bar-wrap,.footer{color:#91a9c0}.icon-btn{background:#20364c;border-color:#314b63;color:#c5d9e9}.stat,.chart-card,.daily-list,.sun-card,.hour-card{background:#172a3e;border-color:#294258;box-shadow:0 8px 22px rgba(0,0,0,.13)}.stat-value,.day-name,.day-temps .max,.sun-time,.hour-temp{color:#edf5fc}.stat-value .unit,.day-temps .min{color:#8fa7bd}.section-title{color:#eaf3fb}.section-title:after{background:linear-gradient(90deg,#294258,transparent)}.day-row{border-color:#263d52}.day-bar{background:#2b4359}.chart-tooltip{background:#e7f4fc;color:#183b58}.chart-tooltip.blue{background:#dff4ff;color:#245a7e}.banner{background:#172a3e;border-color:#294258;color:#eaf3fb}.banner-body span{color:#9bb1c5}.banner-rain{background:#35291e;border-color:#5a442c}.banner-offline{background:#172d3d;border-color:#294c62}.skeleton-wrap .sk{background:linear-gradient(100deg,#172a3e 25%,#233c54 40%,#172a3e 60%);background-size:200% 100%}.error-card{background:#352322;border-color:#69413e;color:#ffd9d4}.toast,.inpage-notif{background:#172a3e;border-color:#294258;color:#eaf3fb}.inpage-notif-title{color:#eaf3fb}.inpage-notif-body{color:#9bb1c5}.pull-indicator{background:#172a3e;border-color:#294258;color:#9bb1c5}.pull-spinner{border-color:#344c62;border-top-color:#75bce6}footer{border-color:#294258;color:#819ab1}footer b{color:#c2d6e8}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>"""

body = r"""<body>
<div id="pullIndicator" class="pull-indicator"><span class="pull-spinner"></span><span id="pullText">برای به‌روزرسانی بکشید</span></div>
<div class="app">
<div id="notifStatus" class="notif-status" hidden title="کلیک کنید برای ارسال آزمایشی"><span class="notif-status-icon">🔔</span><span class="notif-status-text" id="notifStatusText">—</span><span class="notif-status-hint">آزمایش اعلان</span></div>
<div id="rainAlert" class="banner banner-rain" hidden><span class="banner-icon">🌧️</span><div class="banner-body"><b>هشدار بارش</b><span id="rainMsg"></span></div><button class="banner-close" id="rainClose" aria-label="بستن">×</button></div>
<div id="offlineBanner" class="banner banner-offline" hidden><span class="banner-icon">📡</span><div class="banner-body"><b>حالت آفلاین</b><span id="offlineMsg">آخرین داده ذخیره‌شده نمایش داده می‌شود.</span></div></div>
<header>
<div class="location"><div class="location-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><div class="location-info"><select id="citySelect" class="city-select" aria-label="انتخاب شهر"><option value="piranshahr">پیرانشهر</option><option value="urmia">ارومیه</option><option value="mahabad">مهاباد</option><option value="sardasht">سردشت</option><option value="bukan">بوکان</option><option value="tabriz">تبریز</option><option value="tehran">تهران</option></select><p id="cityRegion">آب‌وهوای قندیل</p></div></div>
<div class="actions">
<button id="installBtn" class="icon-btn install-btn" aria-label="نصب اپ" title="نصب به‌عنوان اپ" hidden><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></button>
<button id="notifBtn" class="icon-btn notif-btn" aria-label="اعلان بارش" title="فعال‌سازی اعلان بارش"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg></button>
<button id="refreshBtn" class="icon-btn" aria-label="به‌روزرسانی" title="به‌روزرسانی"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
</div></header>
<div id="loading" class="skeleton-wrap"><div class="sk hero"></div><div class="sk stats"></div><div class="sk chart"></div></div>
<div id="error" class="error-card" hidden><p id="errorMsg">⚠️ دریافت اطلاعات آب و هوا ناموفق بود.</p><button class="btn-retry" onclick="location.reload()">تلاش دوباره</button></div>
<main id="content" hidden>
<section class="hero"><div class="hero-main"><div class="hero-temp" id="heroTemp">—<sup>°C</sup></div><div class="hero-desc" id="heroDesc">—</div><div class="hero-feels" id="heroFeels">—</div></div><div class="hero-icon" id="heroIcon">🌤️</div></section>
<section class="stats" id="statsGrid"></section>
<section class="section"><h2 class="section-title">روند دمای ۲۴ ساعت آینده</h2><div class="chart-card"><div class="chart-wrap"><canvas id="tempChart"></canvas><div id="chartTip" class="chart-tooltip"></div></div></div></section>
<section class="section"><h2 class="section-title">احتمال بارش در ۲۴ ساعت آینده</h2><div class="chart-card"><div class="chart-wrap precip"><canvas id="precipChart"></canvas><div id="precipTip" class="chart-tooltip blue"></div></div></div></section>
<section class="section"><h2 class="section-title">پیش‌بینی ساعتی</h2><div class="hourly-scroll" id="hourlyRow"></div></section>
<section class="section"><h2 class="section-title">پیش‌بینی ۷ روز آینده</h2><div class="daily-list" id="dailyList"></div></section>
<section class="sun-row"><div class="sun-card"><div class="sun-icon">🌅</div><div class="sun-info"><span class="sun-label">طلوع خورشید</span><span class="sun-time" id="sunrise">—</span></div></div><div class="sun-card"><div class="sun-icon">🌇</div><div class="sun-info"><span class="sun-label">غروب خورشید</span><span class="sun-time" id="sunset">—</span></div></div></section>
</main>
<footer><span>آخرین به‌روزرسانی: <b id="lastUpdate">—</b></span><span>به‌روزرسانی بعدی: <b id="countdown">—</b></span></footer>
</div>
<div id="toast" class="toast"></div><div id="notifStack" class="inpage-notif-stack" aria-live="polite"></div>
"""

ids = set(re.findall(r'\bid=["\']([^"\']+)', body))
needed = set(re.findall(r"\$\('([^']+)'\)", app_script))
missing = sorted(needed - ids)
if missing:
    raise SystemExit("Redesign omitted required DOM IDs: " + ", ".join(missing))

html = '<!DOCTYPE html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n<meta name="theme-color" content="#0b1628">\n<title>آب و هوای قندیل</title>\n' + css + '\n</head>\n' + body + '\n' + app_script + '\n</body>\n</html>\n'

# Rename the Android launcher label while preserving the application ID and signing identity.
values_dir = Path("app/src/main/res/values")
values_dir.mkdir(parents=True, exist_ok=True)
strings_file = values_dir / "strings.xml"
if strings_file.exists():
    strings = strings_file.read_text(encoding="utf-8")
    if re.search(r'<string\s+name=["\']app_name["\']', strings):
        strings = re.sub(r'(<string\s+name=["\']app_name["\'][^>]*>)[\s\S]*?(</string>)', r'\1آب و هوای قندیل\2', strings, count=1)
    else:
        strings = strings.replace("</resources>", '    <string name="app_name">آب و هوای قندیل</string>\n</resources>')
    strings_file.write_text(strings, encoding="utf-8")
manifest = Path("app/src/main/AndroidManifest.xml")
if manifest.exists():
    manifest_text = manifest.read_text(encoding="utf-8")
    if re.search(r'android:label\s*=', manifest_text):
        manifest_text = re.sub(r'android:label\s*=\s*["\'][^"\']*["\']', 'android:label="@string/app_name"', manifest_text, count=1)
    else:
        manifest_text = re.sub(r'(<application\b)', r'\1 android:label="@string/app_name"', manifest_text, count=1)
    manifest.write_text(manifest_text, encoding="utf-8")


# Install the custom Qandil winter icon for Android launchers.
icon_source = Path("../qandil_icon.jpg")
if not icon_source.is_file():
    raise SystemExit("Qandil launcher icon asset is missing")
icon_dir = Path("app/src/main/res/mipmap-nodpi")
icon_dir.mkdir(parents=True, exist_ok=True)
(icon_dir / "ic_launcher.jpg").write_bytes(icon_source.read_bytes())
manifest = Path("app/src/main/AndroidManifest.xml")
manifest_text = manifest.read_text(encoding="utf-8")
manifest_text = re.sub(r'android:icon\s*=\s*"[^"]*"', 'android:icon="@mipmap/ic_launcher"', manifest_text, count=1)
manifest_text = re.sub(r'android:roundIcon\s*=\s*"[^"]*"', 'android:roundIcon="@mipmap/ic_launcher"', manifest_text, count=1)
manifest.write_text(manifest_text, encoding="utf-8")

page.write_text(html, encoding="utf-8")
print(f"Rebuilt weather.html with {len(ids)} preserved DOM IDs and original application JavaScript.")
