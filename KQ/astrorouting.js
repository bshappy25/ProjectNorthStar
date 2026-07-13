/**
 * chartWeights.js
 *
 * Converts a raw astrology chart (planet -> sign + degree) into a
 * weighted score per zodiac sign, summing to 100.
 *
 * This does NOT interpret or analyze the chart. It's a pure
 * codification step: turning chart placements into numeric weights
 * for use downstream (e.g. as input to another system/model).
 */

const SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
];

// Planets that get an explicit, fixed weight.
const CORE_WEIGHTS = {
  Sun: 50,
  Moon: 25,
  Jupiter: 100 / 12, // ≈ 8.3333
};

// Everything left over after Sun/Moon/Jupiter is split evenly across
// 4 buckets: Mars/Venus (as one bucket, then split in half), Saturn,
// Mercury, and "Others" (outer planets + points).
const CORE_TOTAL = CORE_WEIGHTS.Sun + CORE_WEIGHTS.Moon + CORE_WEIGHTS.Jupiter;
const REMAINING_TOTAL = 100 - CORE_TOTAL; // ≈ 16.6667
const REMAINING_BUCKETS = 4; // Mars/Venus, Saturn, Mercury, Others
const BUCKET_WEIGHT = REMAINING_TOTAL / REMAINING_BUCKETS; // ≈ 4.1667

// Planets/points that fall under the fixed named buckets.
const NAMED_BUCKET_PLANETS = new Set([
  "Sun", "Moon", "Jupiter", "Mars", "Venus", "Saturn", "Mercury",
]);

/**
 * Given the full list of planet keys present in the chart, figure out
 * which ones belong in the "Others" bucket (anything not named above:
 * Uranus, Neptune, Pluto, Chiron, North Node, South Node, etc.)
 */
function getOtherPlanets(planetKeys) {
  return planetKeys.filter((p) => !NAMED_BUCKET_PLANETS.has(p));
}

/**
 * Builds a weight-per-planet map based on which planets are actually
 * present in the chart. "Others" weight is split evenly among however
 * many "other" bodies are included.
 *
 * @param {string[]} planetKeys - all planet/point keys present in the chart
 * @returns {Object<string, number>} planet -> weight (sums to 100)
 */
function buildPlanetWeights(planetKeys) {
  const weights = {};

  // Core named weights
  weights.Sun = CORE_WEIGHTS.Sun;
  weights.Moon = CORE_WEIGHTS.Moon;
  weights.Jupiter = CORE_WEIGHTS.Jupiter;

  // Mars/Venus bucket, split in half
  weights.Mars = BUCKET_WEIGHT / 2;
  weights.Venus = BUCKET_WEIGHT / 2;

  // Saturn and Mercury each get a full bucket
  weights.Saturn = BUCKET_WEIGHT;
  weights.Mercury = BUCKET_WEIGHT;

  // Others: split BUCKET_WEIGHT evenly among whatever "other" planets
  // are actually present in this chart
  const others = getOtherPlanets(planetKeys);
  if (others.length > 0) {
    const perOther = BUCKET_WEIGHT / others.length;
    others.forEach((p) => {
      weights[p] = perOther;
    });
  }

  return weights;
}

/**
 * Codifies a chart into a per-sign weighted score, normalized to sum to 100.
 *
 * @param {Object} chart - e.g. { Sun: { sign: "Leo", degree: 15.4 }, Moon: {...}, ... }
 * @returns {Object} {
 *   bySign: { Aries: 0, ..., Leo: 50, ... }  // sums to 100
 *   byPlanet: { Sun: { sign, degree, weight }, ... }
 * }
 */
function codifyChart(chart) {
  const planetKeys = Object.keys(chart);

  if (planetKeys.length === 0) {
    throw new Error("Chart is empty — no planets provided.");
  }

  // Validate signs
  planetKeys.forEach((p) => {
    const entry = chart[p];
    if (!entry || !SIGNS.includes(entry.sign)) {
      throw new Error(`Invalid or missing sign for ${p}: ${entry && entry.sign}`);
    }
  });

  const planetWeights = buildPlanetWeights(planetKeys);

  // Initialize sign totals
  const bySign = {};
  SIGNS.forEach((s) => (bySign[s] = 0));

  const byPlanet = {};

  planetKeys.forEach((p) => {
    const { sign, degree } = chart[p];
    const weight = planetWeights[p] ?? 0;

    bySign[sign] += weight;
    byPlanet[p] = { sign, degree, weight };
  });

  // Normalize so the total is exactly 100 (guards against float drift
  // and against charts that omit some named planets like Mars/Venus).
  const rawTotal = Object.values(bySign).reduce((a, b) => a + b, 0);
  if (rawTotal > 0) {
    SIGNS.forEach((s) => {
      bySign[s] = (bySign[s] / rawTotal) * 100;
    });
  }

  return { bySign, byPlanet };
}

// ---------------------------------------------------------------------
// PLACEHOLDER SECTIONS
// These are not calculated from the chart — they're stubs to fill in
// with real data (manually, from an API, scraped, whatever). They get
// merged into the final output by buildFullOutput() below.
// ---------------------------------------------------------------------

// 1. AOL horoscope placeholder
const PLACEHOLDER_HOROSCOPE = {
  source: "AOL Horoscope", // TODO: confirm source/attribution
  sign: null,               // TODO: e.g. "Leo"
  date: null,                // TODO: e.g. "2026-07-13"
  text: "",                  // TODO: paste the actual horoscope text
};

// 2. Current actual weather placeholder
const PLACEHOLDER_WEATHER = {
  location: "",     // TODO: e.g. "Bronx, NY"
  date: null,         // TODO: e.g. "2026-07-13"
  tempF: null,        // TODO
  tempC: null,        // TODO
  conditions: "",   // TODO: e.g. "Partly Cloudy"
  humidity: null,     // TODO: %
  windSpeed: null,    // TODO: mph
};

// 3. Mood meter placeholder (1-10, based on complexity + emotion)
const PLACEHOLDER_MOOD_METER = {
  score: null,        // TODO: 1-10 overall mood score
  complexity: null,   // TODO: 1-10, how complex the day/moment feels
  emotion: "",       // TODO: e.g. "anxious", "content", "wired"
  notes: "",          // TODO: free text
};

/**
 * Merges chart weights with the placeholder sections into one payload.
 * Pass overrides for any section to fill in real data; anything you
 * omit stays as the placeholder default.
 *
 * @param {Object} chart - see codifyChart()
 * @param {Object} [overrides]
 * @param {Object} [overrides.horoscope]
 * @param {Object} [overrides.weather]
 * @param {Object} [overrides.moodMeter]
 */
function buildFullOutput(chart, overrides = {}) {
  const { bySign, byPlanet } = codifyChart(chart);

  return {
    bySign,
    byPlanet,
    horoscope: { ...PLACEHOLDER_HOROSCOPE, ...(overrides.horoscope || {}) },
    weather: { ...PLACEHOLDER_WEATHER, ...(overrides.weather || {}) },
    moodMeter: { ...PLACEHOLDER_MOOD_METER, ...(overrides.moodMeter || {}) },
  };
}

module.exports = {
  codifyChart,
  buildPlanetWeights,
  buildFullOutput,
  SIGNS,
  PLACEHOLDER_HOROSCOPE,
  PLACEHOLDER_WEATHER,
  PLACEHOLDER_MOOD_METER,
};

// ---------------------------------------------------------------------
// Example usage (remove or comment out if importing this as a module)
// ---------------------------------------------------------------------
if (require.main === module) {
  const exampleChart = {
    Sun: { sign: "Leo", degree: 15.4 },
    Moon: { sign: "Cancer", degree: 3.2 },
    Jupiter: { sign: "Sagittarius", degree: 22.1 },
    Mars: { sign: "Aries", degree: 8.9 },
    Venus: { sign: "Libra", degree: 19.0 },
    Saturn: { sign: "Capricorn", degree: 27.5 },
    Mercury: { sign: "Virgo", degree: 11.3 },
    Uranus: { sign: "Aquarius", degree: 5.0 },
    Neptune: { sign: "Pisces", degree: 29.8 },
    Pluto: { sign: "Scorpio", degree: 1.1 },
    Chiron: { sign: "Gemini", degree: 14.4 },
    NorthNode: { sign: "Taurus", degree: 6.6 },
  };

  const result = buildFullOutput(exampleChart, {
    horoscope: { sign: "Leo", date: "2026-07-13" },
    weather: { location: "Bronx, NY", date: "2026-07-13" },
    moodMeter: { complexity: 6, emotion: "focused" },
  });

  console.log("By sign (sums to 100):");
  console.log(result.bySign);
  console.log("\nBy planet:");
  console.log(result.byPlanet);
  console.log("\nHoroscope (placeholder):");
  console.log(result.horoscope);
  console.log("\nWeather (placeholder):");
  console.log(result.weather);
  console.log("\nMood meter (placeholder):");
  console.log(result.moodMeter);
}
