const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const scriptPath = process.argv[2] || 'dist/weather-core.js';
const context = { URLSearchParams, Date, Math, Number, Array, Object, Error };
vm.runInNewContext(fs.readFileSync(scriptPath, 'utf8'), context, { filename: scriptPath });
const core = context.QandilWeatherCore;
assert.ok(core, 'compiled TypeScript namespace must be exposed to the WebView');

assert.equal(core.getCity('piranshahr').name, 'پیرانشهر');
assert.equal(core.getCity('urmia').lat, 37.552);
assert.throws(() => core.getCity('unknown-city'), /Unknown Qandil city/);
assert.equal(core.getAqiInfo(15).label, 'خوب');
assert.equal(core.getAqiInfo(50).label, 'متوسط');
assert.equal(core.getAqiInfo(null).label, 'نامشخص');
assert.equal(core.clampProbability(130), 100);
assert.equal(core.clampProbability(-5), 0);
assert.equal(core.WEATHER_DESCS[75], 'برف شدید');

const now = new Date('2026-11-15T06:00:00Z');
const hourly = {
  time: [
    '2026-11-15T05:00:00Z',
    '2026-11-15T06:00:00Z',
    '2026-11-15T07:00:00Z',
    '2026-11-15T08:00:00Z',
    '2026-11-15T09:00:00Z'
  ],
  precipitation_probability: [90, 25, 75, 40, 99]
};
const rain = core.summarizeRain(hourly, { precipitation_probability_max: [82] }, now, 3);
assert.deepEqual(JSON.parse(JSON.stringify(rain)), {
  maxProb: 75,
  peakIdx: 2,
  peakTime: '2026-11-15T07:00:00Z',
  todayProb: 82,
  startIdx: 1
});

assert.deepEqual(JSON.parse(JSON.stringify(core.getHourlyWindow(hourly.time, now, 2))), { start: 1, end: 3 });
assert.deepEqual(JSON.parse(JSON.stringify(core.getTemperatureExtent([12, 18], [-3, 4]))), {
  gMax: 18,
  gMin: -3,
  range: 21
});
assert.match(core.buildForecastUrl('piranshahr'), /latitude=36\.701/);
assert.match(core.buildAirQualityUrl('tehran'), /longitude=51\.389/);
assert.throws(() => core.buildForecastUrl('not-a-city'));

const validPayload = {
  current: { temperature_2m: 10, apparent_temperature: 8, weather_code: 3, relative_humidity_2m: 70 },
  hourly: { time: ['2026-11-15T06:00'], temperature_2m: [10], weather_code: [3] },
  daily: { time: ['2026-11-15'], temperature_2m_max: [12], temperature_2m_min: [5], weather_code: [3] }
};
assert.equal(core.isValidWeatherPayload(validPayload), true);
assert.equal(core.isValidWeatherPayload({ current: {}, hourly: {}, daily: {} }), false);

console.log('Qandil TypeScript core tests passed.');
