/**
 * Qandil Weather domain core.
 * This file is compiled to a browser-compatible classic script for Android WebView.
 */
namespace QandilWeatherCore {
  export interface City {
    readonly name: string;
    readonly region: string;
    readonly lat: number;
    readonly lon: number;
  }

  export interface HourlyForecast {
    readonly time: readonly string[];
    readonly precipitation_probability?: readonly (number | null | undefined)[];
  }

  export interface DailyForecast {
    readonly precipitation_probability_max?: readonly (number | null | undefined)[];
  }

  export interface RainSummary {
    maxProb: number;
    peakIdx: number;
    peakTime: string | null;
    todayProb: number;
    startIdx: number;
  }

  export interface TemperatureExtent {
    gMax: number;
    gMin: number;
    range: number;
  }

  export const CITIES: Readonly<Record<string, City>> = Object.freeze({
    piranshahr: { name: 'پیرانشهر', region: 'آذربایجان غربی', lat: 36.701, lon: 45.141 },
    urmia: { name: 'ارومیه', region: 'آذربایجان غربی', lat: 37.552, lon: 45.076 },
    mahabad: { name: 'مهاباد', region: 'آذربایجان غربی', lat: 36.763, lon: 45.722 },
    sardasht: { name: 'سردشت', region: 'آذربایجان غربی', lat: 36.155, lon: 45.481 },
    bukan: { name: 'بوکان', region: 'آذربایجان غربی', lat: 36.521, lon: 46.211 },
    tabriz: { name: 'تبریز', region: 'آذربایجان شرقی', lat: 38.080, lon: 46.291 },
    tehran: { name: 'تهران', region: 'تهران', lat: 35.689, lon: 51.389 }
  });

  export const WEATHER_ICONS: Readonly<Record<number, string>> = Object.freeze({
    0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 48: '🌫️',
    51: '🌦️', 53: '🌦️', 55: '🌧️', 61: '🌧️', 63: '🌧️', 65: '🌧️',
    71: '🌨️', 73: '🌨️', 75: '❄️', 80: '🌦️', 81: '🌧️', 82: '⛈️',
    95: '⛈️', 96: '⛈️', 99: '⛈️'
  });

  export const WEATHER_DESCS: Readonly<Record<number, string>> = Object.freeze({
    0: 'آسمان صاف', 1: 'عمدتاً صاف', 2: 'نیمه ابری', 3: 'ابری',
    45: 'مه', 48: 'مه یخ‌زده', 51: 'نم‌نم باران سبک', 53: 'نم‌نم باران',
    55: 'نم‌نم شدید', 61: 'باران سبک', 63: 'باران', 65: 'باران شدید',
    71: 'برف سبک', 73: 'برف', 75: 'برف شدید', 80: 'رگبار سبک',
    81: 'رگبار', 82: 'رگبار شدید', 95: 'رعد و برق', 96: 'رعد و تگرگ',
    99: 'رعد شدید'
  });

  export function getCity(cityKey: string): City {
    const city = CITIES[cityKey];
    if (!city) throw new Error(`Unknown Qandil city: ${cityKey}`);
    return city;
  }

  export function buildForecastUrl(cityKey: string, timezone = 'Asia/Tehran'): string {
    const city = getCity(cityKey);
    const query = new URLSearchParams({
      latitude: String(city.lat),
      longitude: String(city.lon),
      current: 'temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,pressure_msl',
      hourly: 'temperature_2m,precipitation_probability,weather_code',
      daily: 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max',
      timezone,
      forecast_days: '7'
    });
    return `https://api.open-meteo.com/v1/forecast?${query.toString()}`;
  }

  export function buildAirQualityUrl(cityKey: string, timezone = 'Asia/Tehran'): string {
    const city = getCity(cityKey);
    const query = new URLSearchParams({
      latitude: String(city.lat),
      longitude: String(city.lon),
      current: 'european_aqi',
      timezone
    });
    return `https://air-quality-api.open-meteo.com/v1/air-quality?${query.toString()}`;
  }

  export function getAqiInfo(aqi: number | null | undefined): { cls: string; label: string } {
    if (aqi == null || !Number.isFinite(aqi)) return { cls: '', label: 'نامشخص' };
    if (aqi <= 20) return { cls: 'aqi-good', label: 'خوب' };
    if (aqi <= 40) return { cls: 'aqi-fair', label: 'قابل قبول' };
    if (aqi <= 60) return { cls: 'aqi-moder', label: 'متوسط' };
    if (aqi <= 80) return { cls: 'aqi-poor', label: 'ناسالم' };
    return { cls: 'aqi-vpoor', label: 'بسیار ناسالم' };
  }

  export function clampProbability(value: number | null | undefined): number {
    if (value == null || !Number.isFinite(value)) return 0;
    return Math.min(100, Math.max(0, value));
  }

  export function summarizeRain(
    hourly: HourlyForecast,
    daily: DailyForecast,
    now: Date = new Date(),
    windowHours = 3
  ): RainSummary {
    const times = Array.isArray(hourly?.time) ? hourly.time : [];
    const probabilities = hourly?.precipitation_probability ?? [];
    let startIdx = times.findIndex((time) => new Date(time).getTime() >= now.getTime());
    if (startIdx < 0) startIdx = 0;

    const endIdx = Math.min(startIdx + Math.max(0, Math.floor(windowHours)), times.length);
    let maxProb = 0;
    let peakIdx = -1;
    for (let i = startIdx; i < endIdx; i += 1) {
      const probability = clampProbability(probabilities[i]);
      if (probability > maxProb) {
        maxProb = probability;
        peakIdx = i;
      }
    }

    const todayProb = clampProbability(daily?.precipitation_probability_max?.[0]);
    return {
      maxProb,
      peakIdx,
      peakTime: peakIdx >= 0 ? times[peakIdx] : null,
      todayProb,
      startIdx
    };
  }

  export function getHourlyWindow(
    times: readonly string[],
    referenceTime: Date | string = new Date(),
    count = 24
  ): { start: number; end: number } {
    const reference = referenceTime instanceof Date ? referenceTime : new Date(referenceTime);
    let start = times.findIndex((time) => new Date(time).getTime() >= reference.getTime());
    if (start < 0) start = 0;
    const safeCount = Math.max(0, Math.floor(count));
    return { start, end: Math.min(start + safeCount, times.length) };
  }

  export function getTemperatureExtent(
    maxTemps: readonly number[],
    minTemps: readonly number[]
  ): TemperatureExtent {
    const values = [...maxTemps, ...minTemps].filter(Number.isFinite);
    if (values.length === 0) return { gMax: 0, gMin: 0, range: 1 };
    const gMax = Math.max(...values);
    const gMin = Math.min(...values);
    return { gMax, gMin, range: gMax - gMin || 1 };
  }

  export function isValidWeatherPayload(payload: unknown): boolean {
    if (typeof payload !== 'object' || payload === null) return false;
    const value = payload as Record<string, unknown>;
    const current = value.current as Record<string, unknown> | undefined;
    const hourly = value.hourly as Record<string, unknown> | undefined;
    const daily = value.daily as Record<string, unknown> | undefined;
    if (!current || !hourly || !daily) return false;

    const finite = (candidate: unknown): candidate is number =>
      typeof candidate === 'number' && Number.isFinite(candidate);
    const hasArray = (record: Record<string, unknown>, key: string): boolean =>
      Array.isArray(record[key]) && (record[key] as unknown[]).length > 0;

    if (!finite(current.temperature_2m) || !finite(current.apparent_temperature) ||
        !finite(current.weather_code) || !finite(current.relative_humidity_2m)) return false;

    if (!hasArray(hourly, 'time') || !hasArray(hourly, 'temperature_2m') ||
        !hasArray(hourly, 'weather_code')) return false;
    if (!hasArray(daily, 'time') || !hasArray(daily, 'temperature_2m_max') ||
        !hasArray(daily, 'temperature_2m_min') || !hasArray(daily, 'weather_code')) return false;

    const hourlyTimes = hourly.time as unknown[];
    const hourlyTemps = hourly.temperature_2m as unknown[];
    const dailyTimes = daily.time as unknown[];
    const dailyMax = daily.temperature_2m_max as unknown[];
    const dailyMin = daily.temperature_2m_min as unknown[];
    return hourlyTimes.length === hourlyTemps.length &&
      dailyTimes.length === dailyMax.length && dailyTimes.length === dailyMin.length &&
      hourlyTimes.every((time) => typeof time === 'string') &&
      dailyTimes.every((time) => typeof time === 'string') &&
      hourlyTemps.every(finite) && dailyMax.every(finite) && dailyMin.every(finite);
  }
}
