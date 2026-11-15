from pathlib import Path
import re

ROOT = Path.cwd()
required_files = [
    ROOT / "app/src/main/AndroidManifest.xml",
    ROOT / "app/src/main/java/com/example/weather/MainActivity.kt",
    ROOT / "app/src/main/java/com/example/weather/AndroidBridge.kt",
    ROOT / "app/src/main/java/com/example/weather/NotificationHelper.kt",
    ROOT / "app/src/main/assets/weather.html",
    ROOT / "app/src/main/assets/weather-core.js",
    ROOT / "app/build.gradle.kts",
]
missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
if missing:
    raise SystemExit("Required project files are missing: " + ", ".join(missing))

html = (ROOT / "app/src/main/assets/weather.html").read_text(encoding="utf-8")
core = (ROOT / "app/src/main/assets/weather-core.js").read_text(encoding="utf-8")
manifest = (ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
gradle = (ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")

checks = {
    "compiled TypeScript is loaded once": html.count('src="weather-core.js"') == 1,
    "typed core is used by the app": "QandilWeatherCore.buildForecastUrl" in html and "QandilWeatherCore.summarizeRain" in html,
    "API payload validation is active": "QandilWeatherCore.isValidWeatherPayload" in html,
    "city configuration exists in compiled core": "piranshahr" in core and "urmia" in core,
    "Android internet permission is retained": "android.permission.INTERNET" in manifest,
    "existing app identity is retained": 'applicationId = "com.example.weather"' in gradle,
    "version code is 12": bool(re.search(r"versionCode\s*=\s*12", gradle)),
    "version name is 1.7.0": bool(re.search(r'versionName\s*=\s*"1\.7\.0"', gradle)),
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {name}")
if failed:
    raise SystemExit("Project validation failed: " + "; ".join(failed))
print("Qandil project validation passed.")
