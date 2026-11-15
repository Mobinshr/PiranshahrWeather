from pathlib import Path
import re
import shutil

ASSETS = Path("app/src/main/assets")
HTML = ASSETS / "weather.html"
COMPILED_CORE = Path("../dist/weather-core.js")


def replace_once(source: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Could not integrate TypeScript core: expected one {label}, found {count}")
    return updated


def main() -> None:
    if not HTML.is_file():
        raise SystemExit(f"Weather HTML is missing: {HTML}")
    if not COMPILED_CORE.is_file():
        raise SystemExit(f"Compiled TypeScript core is missing: {COMPILED_CORE}")

    source = HTML.read_text(encoding="utf-8")
    core_target = ASSETS / "weather-core.js"
    shutil.copy2(COMPILED_CORE, core_target)

    if 'src="weather-core.js"' not in source:
        source = replace_once(
            source,
            r"<script(?![^>]*\bsrc=)[^>]*>",
            '<script src="weather-core.js"></script>\n    <script>',
            "main script tag",
        )

    replacements = [
        (r"const CITIES = \{.*?\n        \};", "const CITIES = QandilWeatherCore.CITIES;", "city registry"),
        (r"const WEATHER_ICONS = \{[^\n]*?\};", "const WEATHER_ICONS = QandilWeatherCore.WEATHER_ICONS;", "weather icon registry"),
        (r"const WEATHER_DESCS = \{[^\n]*?\};", "const WEATHER_DESCS = QandilWeatherCore.WEATHER_DESCS;", "weather description registry"),
        (r"const aqiInfo = aqi => \{.*?\n        \};", "const aqiInfo = QandilWeatherCore.getAqiInfo;", "air quality classifier"),
    ]
    for pattern, replacement, label in replacements:
        if replacement not in source:
            source = replace_once(source, pattern, replacement, label)
    rain_function = "function computeNotifStatus(hourly, daily) {\n            return QandilWeatherCore.summarizeRain(hourly, daily);\n        }"
    if rain_function not in source:
        source = replace_once(
            source,
            r"function computeNotifStatus\(hourly, daily\) \{.*?\n        \}",
            rain_function,
            "rain probability calculation",
        )
    source = replace_once(
        source,
        r"const \{ lat, lon \} = CITIES\[currentCity\];.*?const airUrl = .*?;",
        "const weatherUrl = QandilWeatherCore.buildForecastUrl(currentCity, TZ);\n"
        "            const airUrl = QandilWeatherCore.buildAirQualityUrl(currentCity, TZ);",
        "weather API URL builder",
    )
    source = replace_once(
        source,
        r"const weather = await wRes\.json\(\);",
        "const weather = await wRes.json();\n"
        "            if (!QandilWeatherCore.isValidWeatherPayload(weather)) {\n"
        "                throw new Error('دادهٔ دریافتی هواشناسی معتبر نیست.');\n"
        "            }",
        "weather response validation",
    )
    source = replace_once(
        source,
        r"let start = hourly\.time\.findIndex\(t => new Date\(t\) >= ref\);\s*"
        r"if \(start < 0\) start = 0;\s*"
        r"const end = Math\.min\(start \+ 24, hourly\.time\.length\);",
        "const { start, end } = QandilWeatherCore.getHourlyWindow(hourly.time, ref, 24);",
        "hourly forecast window",
    )
    source = replace_once(
        source,
        r"const gMax = Math\.max\(\.\.\.maxArr\), gMin = Math\.min\(\.\.\.minArr\), range = \(gMax-gMin\)\|\|1;",
        "const { gMax, gMin, range } = QandilWeatherCore.getTemperatureExtent(maxArr, minArr);",
        "daily temperature range",
    )

    if source.count('src="weather-core.js"') != 1:
        raise SystemExit("The compiled TypeScript core must be loaded exactly once")
    if "QandilWeatherCore.buildForecastUrl" not in source or "QandilWeatherCore.summarizeRain" not in source:
        raise SystemExit("TypeScript core integration did not reach the application runtime")

    HTML.write_text(source, encoding="utf-8")

    strings_file = Path("app/src/main/res/values/strings.xml")
    if strings_file.is_file():
        strings = strings_file.read_text(encoding="utf-8")
        strings = re.sub(
            r'(<string\s+name="app_name"[^>]*>).*?(</string>)',
            r'\1آب‌وهوای قندیل\2',
            strings,
            count=1,
            flags=re.S,
        )
        strings_file.write_text(strings, encoding="utf-8")

    main_activity = Path("app/src/main/java/com/example/weather/MainActivity.kt")
    if main_activity.is_file():
        kotlin = main_activity.read_text(encoding="utf-8")
        kotlin = kotlin.replace("آب و هوای پیرانشهر", "آب‌وهوای قندیل")
        main_activity.write_text(kotlin, encoding="utf-8")

    notification_helper = Path("app/src/main/java/com/example/weather/NotificationHelper.kt")
    if notification_helper.is_file():
        kotlin = notification_helper.read_text(encoding="utf-8")
        kotlin = kotlin.replace(
            "اعلان‌های هشدار بارش و تغییرات وضعیت جوی پیرانشهر",
            "اعلان هشدار بارش و تغییرات وضعیت جوی",
        )
        notification_helper.write_text(kotlin, encoding="utf-8")

    print("Integrated TypeScript core into the Android WebView assets and aligned native app labels.")


if __name__ == "__main__":
    main()
