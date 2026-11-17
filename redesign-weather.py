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

/* Selectable Qandil themes */
:root[data-theme="qandil"]{color-scheme:dark;background:#0b1628;--ink:#fff;--muted:rgba(255,255,255,.7);--line:rgba(255,255,255,.18);--shadow:0 12px 34px rgba(0,0,0,.18)}
:root[data-theme="qandil"] body{background:radial-gradient(ellipse at 78% 4%,rgba(95,168,232,.34),transparent 36%),radial-gradient(ellipse at 8% 28%,rgba(75,112,190,.18),transparent 34%),linear-gradient(165deg,#081326,#142b4c 48%,#0b1529);color:#fff}
:root[data-theme="qandil"] body:before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.28;background-image:radial-gradient(2px 2px at 18% 22%,#fff 40%,transparent 100%),radial-gradient(1px 1px at 73% 31%,#fff 40%,transparent 100%),radial-gradient(1.5px 1.5px at 42% 68%,#fff 40%,transparent 100%);background-size:260px 220px;animation:qandilSky 36s linear infinite}
@keyframes qandilSky{to{background-position:260px 220px}}
:root[data-theme="qandil"] header{background:rgba(8,18,39,.34);border-color:rgba(255,255,255,.14);box-shadow:0 10px 30px rgba(0,0,0,.12)}
:root[data-theme="qandil"] .location-icon{background:rgba(255,255,255,.12);color:#d8edff}
:root[data-theme="qandil"] .city-select{color:#fff}:root[data-theme="qandil"] .city-select option{background:#16233f;color:#fff}
:root[data-theme="qandil"] .location-info p,:root[data-theme="qandil"] .section-title{color:rgba(255,255,255,.72)}
:root[data-theme="qandil"] .icon-btn{background:rgba(12,22,48,.32);border-color:rgba(255,255,255,.2);color:#fff}
:root[data-theme="qandil"] .hero{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:0;padding:20px 8px 14px;border:0;border-radius:0;background:transparent;box-shadow:none;color:#fff}
:root[data-theme="qandil"] .hero-main{display:contents}:root[data-theme="qandil"] .hero-main:before{display:none}
:root[data-theme="qandil"] .hero-icon{order:1;font-size:3.5rem;line-height:1;filter:drop-shadow(0 8px 18px rgba(0,0,0,.3))}
:root[data-theme="qandil"] .hero-temp{order:2;font-size:clamp(6rem,30vw,8.4rem);font-weight:100;line-height:.95;letter-spacing:-6px;color:#fff;text-shadow:0 4px 30px rgba(0,0,0,.18)}
:root[data-theme="qandil"] .hero-temp sup{font-size:1.35rem;font-weight:300;color:rgba(255,255,255,.85)}
:root[data-theme="qandil"] .hero-desc{order:3;font-size:1.25rem;color:#fff}:root[data-theme="qandil"] .hero-feels{order:4;color:rgba(255,255,255,.7)}
:root[data-theme="qandil"] .stat,:root[data-theme="qandil"] .chart-card,:root[data-theme="qandil"] .hourly-scroll,:root[data-theme="qandil"] .daily-list,:root[data-theme="qandil"] .sun-card{background:rgba(12,22,48,.34);border-color:rgba(255,255,255,.16);box-shadow:0 10px 28px rgba(0,0,0,.12);backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px)}
:root[data-theme="qandil"] .stat-label,:root[data-theme="qandil"] .stat-value .unit,:root[data-theme="qandil"] .hour-time,:root[data-theme="qandil"] .day-name small,:root[data-theme="qandil"] .day-bar-wrap,:root[data-theme="qandil"] .sun-label{color:rgba(255,255,255,.65)}
:root[data-theme="qandil"] .stat-label svg{color:#8ecbfa}:root[data-theme="qandil"] .stat-value,:root[data-theme="qandil"] .hour-temp,:root[data-theme="qandil"] .day-name,:root[data-theme="qandil"] .day-temps .max,:root[data-theme="qandil"] .sun-time{color:#fff}
:root[data-theme="qandil"] .hour-card{background:transparent;color:#fff;box-shadow:none;border-color:rgba(255,255,255,.13)}:root[data-theme="qandil"] .hour-card.now{background:rgba(255,255,255,.14)}
:root[data-theme="qandil"] .day-row{border-color:rgba(255,255,255,.1)}:root[data-theme="qandil"] .day-bar{background:rgba(255,255,255,.14)}:root[data-theme="qandil"] .day-temps .min{color:rgba(255,255,255,.55)}
:root[data-theme="qandil"] .section-title:after{background:linear-gradient(90deg,rgba(255,255,255,.2),transparent)}
:root[data-theme="qandil"] footer{border-color:rgba(255,255,255,.14);color:rgba(255,255,255,.55)}:root[data-theme="qandil"] footer b{color:rgba(255,255,255,.85)}
:root[data-theme="qandil"] .banner,:root[data-theme="qandil"] .toast,:root[data-theme="qandil"] .inpage-notif{background:rgba(10,20,42,.94);border-color:rgba(255,255,255,.18);color:#fff}
:root[data-theme="qandil"] .banner-body span,:root[data-theme="qandil"] .inpage-notif-body{color:rgba(255,255,255,.7)}
:root[data-theme="qandil"] .pull-indicator{background:rgba(10,20,42,.94);border-color:rgba(255,255,255,.18);color:#fff}:root[data-theme="qandil"] .pull-spinner{border-color:rgba(255,255,255,.2);border-top-color:#fff}
:root[data-theme="night"]{color-scheme:dark;background:#07111f}:root[data-theme="night"] body{background:linear-gradient(160deg,#07111f,#101f35 58%,#080f1b);color:#edf5ff}
:root[data-theme="night"] header{background:rgba(17,31,51,.92);border-color:#2a4058}:root[data-theme="night"] .city-select{color:#edf5ff}
:root[data-theme="night"] .location-info p,:root[data-theme="night"] .section-title{color:#a8bdd1}
:root[data-theme="night"] .location-icon,:root[data-theme="night"] .icon-btn{background:#1b3048;border-color:#334b64;color:#eaf4ff}
:root[data-theme="night"] .hero{background:linear-gradient(135deg,#214b70,#172d4c 70%,#14233a);box-shadow:0 16px 34px rgba(0,0,0,.25)}
:root[data-theme="night"] .stat,:root[data-theme="night"] .chart-card,:root[data-theme="night"] .hourly-scroll,:root[data-theme="night"] .daily-list,:root[data-theme="night"] .sun-card{background:#172a40;border-color:#2b425b;box-shadow:0 8px 24px rgba(0,0,0,.18)}
:root[data-theme="night"] .stat-label,:root[data-theme="night"] .stat-value .unit,:root[data-theme="night"] .hour-time,:root[data-theme="night"] .day-name small,:root[data-theme="night"] .day-bar-wrap,:root[data-theme="night"] .sun-label{color:#9bb1c7}
:root[data-theme="night"] .stat-value,:root[data-theme="night"] .day-name,:root[data-theme="night"] .day-temps .max,:root[data-theme="night"] .sun-time,:root[data-theme="night"] .hour-temp{color:#f2f7fd}
:root[data-theme="night"] .day-row{border-color:#2a4058}:root[data-theme="night"] .day-bar{background:#2a4058}
:root[data-theme="night"] footer{border-color:#2a4058;color:#8ea5bc}:root[data-theme="night"] footer b{color:#d9e8f6}
:root[data-theme="classic"]{color-scheme:light;background:#edf5fc}
:root[data-theme="classic"] body{background:radial-gradient(ellipse at 10% 0%,rgba(110,190,239,.18),transparent 35%),linear-gradient(180deg,#f2f8fd,#eaf2f9);color:#18334f}
:root[data-theme="classic"] header{background:rgba(255,255,255,.88);border-color:rgba(255,255,255,.8)}
:root[data-theme="classic"] .city-select{color:#183b5d}
:root[data-theme="classic"] .location-info p,:root[data-theme="classic"] .section-title{color:#7189a2}
:root[data-theme="classic"] .icon-btn{background:#f5faff;border-color:#e1edf6;color:#477493}
:root[data-theme="classic"] .stat,:root[data-theme="classic"] .chart-card,:root[data-theme="classic"] .hourly-scroll,:root[data-theme="classic"] .daily-list,:root[data-theme="classic"] .sun-card{background:#fff;border-color:#e4eef6;box-shadow:0 7px 20px rgba(35,83,128,.06)}
:root[data-theme="classic"] .stat-label,:root[data-theme="classic"] .stat-value .unit,:root[data-theme="classic"] .hour-time,:root[data-theme="classic"] .day-name small,:root[data-theme="classic"] .day-bar-wrap,:root[data-theme="classic"] .sun-label{color:#8297ac}
:root[data-theme="classic"] .stat-value,:root[data-theme="classic"] .day-name,:root[data-theme="classic"] .day-temps .max,:root[data-theme="classic"] .sun-time,:root[data-theme="classic"] .hour-temp{color:#244767}
:root[data-theme="classic"] .day-row{border-color:#edf2f7}:root[data-theme="classic"] .day-bar{background:#e9f0f6}
:root[data-theme="classic"] footer{border-color:#dce8f1;color:#91a4b7}:root[data-theme="classic"] footer b{color:#56738f}
.settings-overlay{position:fixed;inset:0;z-index:9999;width:100%;height:100%;height:100dvh;min-height:100vh;display:flex;align-items:center;justify-content:center;overflow-y:auto;overscroll-behavior:contain;padding:max(16px,env(safe-area-inset-top)) 14px max(16px,env(safe-area-inset-bottom));background:rgba(3,10,22,.72);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);isolation:isolate}
.settings-overlay[hidden]{display:none!important}
.settings-sheet{position:relative;flex:0 0 auto;width:100%;max-width:560px;max-height:calc(100vh - 32px);overflow-y:auto;overscroll-behavior:contain;margin:auto;padding:22px 18px 20px;border:1px solid rgba(255,255,255,.85);border-radius:25px;background:#f8fbff;color:#18334f;box-shadow:0 22px 70px rgba(0,0,0,.34);animation:settingsIn .22s ease-out}
@keyframes settingsIn{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.settings-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:7px}.settings-head h2{font-size:1.08rem;font-weight:900}.settings-head p{font-size:.68rem;color:#8297ac;margin-bottom:4px}.settings-close{width:34px;height:34px;border:0;border-radius:12px;background:rgba(80,120,155,.1);color:inherit;font-size:1.4rem}
.settings-note{margin:0 0 14px;color:#7890a7;font-size:.72rem;line-height:1.8}.theme-options{display:grid;gap:9px}
.theme-choice{display:flex;align-items:center;gap:11px;width:100%;padding:10px 12px;border:1px solid #dce8f1;border-radius:16px;background:#fff;color:#244767;text-align:right;transition:border-color .18s,transform .18s}
.theme-choice:active{transform:scale(.99)}.theme-choice[aria-pressed="true"]{border-color:#398bc4;box-shadow:0 0 0 2px rgba(57,139,196,.13);background:#f2f9ff}
.theme-preview{width:48px;height:42px;flex:0 0 48px;border-radius:12px;border:1px solid rgba(0,0,0,.08);background:linear-gradient(145deg,#081326,#438fce);position:relative;overflow:hidden}
.theme-preview:after{content:"";position:absolute;left:8px;right:8px;bottom:7px;height:9px;border-radius:7px;background:rgba(255,255,255,.72)}
.preview-ios{background:linear-gradient(145deg,#2a6fd6,#79b8f5)}.preview-classic{background:linear-gradient(145deg,#f2f8fd,#c9e4f7)}.preview-night{background:linear-gradient(145deg,#07111f,#274969)}.preview-auto{background:linear-gradient(110deg,#edf5fc 0 50%,#14243a 50%)}
.theme-choice-copy{display:flex;flex:1;flex-direction:column;gap:3px}.theme-choice-copy b{font-size:.79rem}.theme-choice-copy small{font-size:.65rem;color:#8297ac;line-height:1.5}.theme-check{width:22px;height:22px;display:grid;place-items:center;border-radius:50%;background:#e7f2fa;color:transparent;font-size:.75rem;font-weight:900}
.theme-choice[aria-pressed="true"] .theme-check{background:#2e83c7;color:#fff}
:root[data-theme="qandil"] .settings-sheet,:root[data-theme="night"] .settings-sheet{background:#14263d;border-color:#2c4560;color:#f1f7fd}
:root[data-theme="qandil"] .settings-note,:root[data-theme="night"] .settings-note,:root[data-theme="qandil"] .theme-choice-copy small,:root[data-theme="night"] .theme-choice-copy small{color:#9bb1c7}
:root[data-theme="qandil"] .theme-choice,:root[data-theme="night"] .theme-choice{background:#1b3048;border-color:#334b64;color:#edf5fc}
:root[data-theme="qandil"] .theme-choice[aria-pressed="true"],:root[data-theme="night"] .theme-choice[aria-pressed="true"]{background:#203d59;border-color:#71b8e5}
:root[data-theme="qandil"] .theme-check,:root[data-theme="night"] .theme-check{background:#2c4560}

:root[data-theme="ios"]{color-scheme:light;background:#2a6fd6;--ink:#fff;--muted:rgba(255,255,255,.78);--line:rgba(255,255,255,.2);--shadow:0 10px 28px rgba(12,42,90,.12)}
:root[data-theme="ios"] body{background:linear-gradient(180deg,#2a6fd6 0%,#79b8f5 100%);background-attachment:fixed;color:#fff}
:root[data-theme="ios"] header{background:rgba(255,255,255,.17);border-color:rgba(255,255,255,.22);box-shadow:none;backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px)}
:root[data-theme="ios"] .location-icon,:root[data-theme="ios"] .icon-btn{background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.2);color:#fff}
:root[data-theme="ios"] .city-select,:root[data-theme="ios"] .location-info p,:root[data-theme="ios"] .section-title{color:#fff}
:root[data-theme="ios"] .hero{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:7px;min-height:0;padding:28px 8px 22px;border:0;border-radius:0;background:transparent;box-shadow:none;color:#fff}
:root[data-theme="ios"] .hero-main{display:contents}
:root[data-theme="ios"] .hero-main:before{display:none}
:root[data-theme="ios"] .hero-icon{order:1;font-size:3.7rem;line-height:1;filter:drop-shadow(0 8px 18px rgba(0,0,0,.2))}
:root[data-theme="ios"] .hero-temp{order:2;font-size:clamp(5.8rem,29vw,7.4rem);font-weight:200;line-height:1.02;letter-spacing:-5px;color:#fff;text-shadow:0 3px 18px rgba(0,0,0,.1)}
:root[data-theme="ios"] .hero-desc{order:3;font-size:1.15rem;color:#fff}
:root[data-theme="ios"] .hero-feels{order:4;color:rgba(255,255,255,.88)}
:root[data-theme="ios"] .stat,:root[data-theme="ios"] .chart-card,:root[data-theme="ios"] .hourly-scroll,:root[data-theme="ios"] .daily-list,:root[data-theme="ios"] .sun-card{background:rgba(255,255,255,.17);border-color:rgba(255,255,255,.2);box-shadow:none;backdrop-filter:blur(22px) saturate(1.25);-webkit-backdrop-filter:blur(22px) saturate(1.25)}
:root[data-theme="ios"] .stat-label,:root[data-theme="ios"] .stat-value .unit,:root[data-theme="ios"] .hour-time,:root[data-theme="ios"] .day-name small,:root[data-theme="ios"] .day-bar-wrap,:root[data-theme="ios"] .sun-label{color:rgba(255,255,255,.78)}
:root[data-theme="ios"] .stat-value,:root[data-theme="ios"] .hour-temp,:root[data-theme="ios"] .day-name,:root[data-theme="ios"] .day-temps .max,:root[data-theme="ios"] .sun-time{color:#fff}
:root[data-theme="ios"] .hour-card{background:transparent;border-color:rgba(255,255,255,.2);color:#fff;box-shadow:none}
:root[data-theme="ios"] .hour-card.now{background:rgba(255,255,255,.16)}
:root[data-theme="ios"] .day-row{border-color:rgba(255,255,255,.2)}
:root[data-theme="ios"] .day-bar{background:rgba(0,0,0,.18)}
:root[data-theme="ios"] .day-temps .min{color:rgba(255,255,255,.65)}
:root[data-theme="ios"] .section-title:after{background:linear-gradient(90deg,rgba(255,255,255,.28),transparent)}
:root[data-theme="ios"] footer{border-color:rgba(255,255,255,.2);color:rgba(255,255,255,.7)}
:root[data-theme="ios"] footer b{color:#fff}
:root[data-theme="ios"] .settings-sheet{background:rgba(18,49,91,.97);border-color:rgba(255,255,255,.24);color:#fff}
:root[data-theme="ios"] .settings-note,:root[data-theme="ios"] .theme-choice-copy small{color:rgba(255,255,255,.72)}
:root[data-theme="ios"] .theme-choice{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.18);color:#fff}
:root[data-theme="ios"] .theme-choice[aria-pressed="true"]{background:rgba(255,255,255,.2);border-color:#a9d8ff}
:root[data-theme="ios"] .theme-check{background:rgba(255,255,255,.14)}

@media(prefers-color-scheme:dark){:root[data-theme="auto"]{color-scheme:dark;background:#07111f}:root[data-theme="auto"] body{background:linear-gradient(160deg,#07111f,#10233b 60%,#0a1422);color:#edf5ff}:root[data-theme="auto"] header{background:rgba(17,31,51,.92);border-color:#2a4058}:root[data-theme="auto"] .city-select{color:#edf5ff}:root[data-theme="auto"] .location-info p,:root[data-theme="auto"] .section-title{color:#a8bdd1}:root[data-theme="auto"] .location-icon,:root[data-theme="auto"] .icon-btn{background:#1b3048;border-color:#334b64;color:#eaf4ff}:root[data-theme="auto"] .hero{background:linear-gradient(135deg,#214b70,#172d4c 70%,#14233a)}:root[data-theme="auto"] .stat,:root[data-theme="auto"] .chart-card,:root[data-theme="auto"] .hourly-scroll,:root[data-theme="auto"] .daily-list,:root[data-theme="auto"] .sun-card{background:#172a40;border-color:#2b425b}:root[data-theme="auto"] .stat-label,:root[data-theme="auto"] .stat-value .unit,:root[data-theme="auto"] .hour-time,:root[data-theme="auto"] .day-name small,:root[data-theme="auto"] .day-bar-wrap,:root[data-theme="auto"] .sun-label{color:#9bb1c7}:root[data-theme="auto"] .stat-value,:root[data-theme="auto"] .day-name,:root[data-theme="auto"] .day-temps .max,:root[data-theme="auto"] .sun-time,:root[data-theme="auto"] .hour-temp{color:#f2f7fd}:root[data-theme="auto"] .day-row{border-color:#2a4058}:root[data-theme="auto"] .day-bar{background:#2a4058}:root[data-theme="auto"] footer{border-color:#2a4058;color:#8ea5bc}}
@media(max-width:560px){:root[data-theme="qandil"] .hero{padding:18px 4px 12px}:root[data-theme="qandil"] .hero-temp{font-size:clamp(5.8rem,29vw,7.4rem)}}
@media(prefers-reduced-motion:reduce){:root[data-theme="qandil"] body:before{animation:none}}

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
<button id="settingsBtn" class="icon-btn" aria-label="تنظیمات ظاهر" title="تنظیمات ظاهر"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.88l.06.06-1.7 1.7-.06-.06a1.7 1.7 0 0 0-1.88-.34 1.7 1.7 0 0 0-1.03 1.56V20h-2.4v-.2a1.7 1.7 0 0 0-1.03-1.56 1.7 1.7 0 0 0-1.88.34l-.06.06-1.7-1.7.06-.06A1.7 1.7 0 0 0 8.4 15a1.7 1.7 0 0 0-1.56-1.03H6v-2.4h.84A1.7 1.7 0 0 0 8.4 10a1.7 1.7 0 0 0-.34-1.88L8 8.06l1.7-1.7.06.06a1.7 1.7 0 0 0 1.88.34A1.7 1.7 0 0 0 12.67 5.2V5h2.4v.2a1.7 1.7 0 0 0 1.03 1.56 1.7 1.7 0 0 0 1.88-.34l.06-.06 1.7 1.7-.06.06a1.7 1.7 0 0 0-.34 1.88 1.7 1.7 0 0 0 1.56 1.03H21v2.4h-.1A1.7 1.7 0 0 0 19.4 15z"/></svg></button>
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
<div id="settingsOverlay" class="settings-overlay" hidden>
<section class="settings-sheet" role="dialog" aria-modal="true" aria-labelledby="settingsTitle">
<div class="settings-head"><div><p>شخصی‌سازی قندیل</p><h2 id="settingsTitle">انتخاب ظاهر برنامه</h2></div><button id="settingsClose" class="settings-close" aria-label="بستن تنظیمات">×</button></div>
<p class="settings-note">هر زمان خواستی می‌توانی پوسته را عوض کنی. انتخابت ذخیره می‌شود و اطلاعات آب‌وهوا دوباره بارگیری نمی‌شوند.</p>
<div class="theme-options">
<button class="theme-choice" type="button" data-theme-choice="ios" aria-pressed="false"><span class="theme-preview preview-ios"></span><span class="theme-choice-copy"><b>آسمان آبی</b><small>طراحی شیشه‌ای آبی بر پایهٔ فایل جدید</small></span><span class="theme-check">✓</span></button>
<button class="theme-choice" type="button" data-theme-choice="qandil" aria-pressed="false"><span class="theme-preview"></span><span class="theme-choice-copy"><b>قندیل پویا</b><small>طراحی جدید با پس‌زمینهٔ آسمانی و کارت‌های شیشه‌ای</small></span><span class="theme-check">✓</span></button>
<button class="theme-choice" type="button" data-theme-choice="classic" aria-pressed="false"><span class="theme-preview preview-classic"></span><span class="theme-choice-copy"><b>آسمانی روشن</b><small>ظاهر روشن و مرتب نسخهٔ قبلی</small></span><span class="theme-check">✓</span></button>
<button class="theme-choice" type="button" data-theme-choice="night" aria-pressed="false"><span class="theme-preview preview-night"></span><span class="theme-choice-copy"><b>شب قندیل</b><small>حالت تیره با کارت‌های ساده و خوانا</small></span><span class="theme-check">✓</span></button>
<button class="theme-choice" type="button" data-theme-choice="auto" aria-pressed="false"><span class="theme-preview preview-auto"></span><span class="theme-choice-copy"><b>هماهنگ با دستگاه</b><small>تغییر روشنایی بر اساس تنظیمات گوشی</small></span><span class="theme-check">✓</span></button>
</div>
</section>
</div>
"""

theme_script = r"""<script>
(function(){
  var KEY='qandil-weather-theme-v1',allowed=['ios','qandil','classic','night','auto'];
  var root=document.documentElement,overlay=document.getElementById('settingsOverlay');
  var openBtn=document.getElementById('settingsBtn'),closeBtn=document.getElementById('settingsClose');
  var choices=Array.prototype.slice.call(document.querySelectorAll('[data-theme-choice]'));
  function apply(theme,save){
    if(allowed.indexOf(theme)<0)theme='ios';
    root.setAttribute('data-theme',theme);
    if(save){try{localStorage.setItem(KEY,theme);}catch(e){}}
    choices.forEach(function(btn){btn.setAttribute('aria-pressed',btn.getAttribute('data-theme-choice')===theme?'true':'false');});
    var meta=document.querySelector('meta[name="theme-color"]');
    if(meta)meta.content=theme==='ios'?'#2a6fd6':theme==='qandil'?'#0b1628':theme==='night'?'#07111f':theme==='auto'?'#102238':'#edf5fc';
  }
  function open(){overlay.hidden=false;document.body.style.overflow='hidden';}
  function close(){overlay.hidden=true;document.body.style.overflow='';}
  openBtn.addEventListener('click',open);closeBtn.addEventListener('click',close);
  overlay.addEventListener('click',function(e){if(e.target===overlay)close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!overlay.hidden)close();});
  choices.forEach(function(btn){btn.addEventListener('click',function(){apply(btn.getAttribute('data-theme-choice'),true);});});
  var saved='ios';try{saved=localStorage.getItem(KEY)||'ios';}catch(e){}
  apply(saved,false);
})();
</script>"""

ids = set(re.findall(r'\bid=["\']([^"\']+)', body))
needed = set(re.findall(r"\$\('([^']+)'\)", app_script))
missing = sorted(needed - ids)
if missing:
    raise SystemExit("Redesign omitted required DOM IDs: " + ", ".join(missing))

html = '<!DOCTYPE html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n<meta name="theme-color" content="#0b1628">\n<title>آب و هوای قندیل</title>\n' + css + '\n</head>\n' + body + '\n' + app_script + '\n' + theme_script + '\n</body>\n</html>\n'

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
