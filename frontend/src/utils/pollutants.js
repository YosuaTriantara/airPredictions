import { POLLUTANT_UNITS } from '../data/stations.js'

const FIELD_LABELS = {
  pm25: 'PM2.5',
  pm10: 'PM10',
  no: 'NO',
  no2: 'NO2',
  nox: 'NOx',
  co: 'CO',
  so2: 'SO2',
  o3: 'O3',
}

// Urutan tampilan default (4 polutan utama, sesuai desain awal).
const DEFAULT_ORDER = ['pm25', 'pm10', 'no2', 'co']

// Ubah 1 baris measurement (dict field->angka dari backend) jadi array
// [{ name, value, unit }] siap dipakai kartu polutan di UI.
export function toPollutantList(measurement, order = DEFAULT_ORDER) {
  if (!measurement) return []
  return order
    .filter((field) => measurement[field] !== null && measurement[field] !== undefined)
    .map((field) => {
      const name = FIELD_LABELS[field] || field.toUpperCase()
      return {
        name,
        value: measurement[field],
        unit: POLLUTANT_UNITS[name] || '',
      }
    })
}
