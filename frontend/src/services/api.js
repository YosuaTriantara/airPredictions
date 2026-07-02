const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request(path, options = {}) {
  let res
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch (err) {
    throw new ApiError(
      'Tidak dapat menghubungi server. Pastikan backend berjalan dan dapat diakses.',
      0
    )
  }

  let body = null
  try {
    body = await res.json()
  } catch {
    // respons tanpa body (mis. 204) — biarkan body null
  }

  if (!res.ok || body?.success === false) {
    const message = body?.message || `Request gagal (HTTP ${res.status})`
    throw new ApiError(message, res.status)
  }

  return body?.data
}

function get(path) {
  return request(path, { method: 'GET' })
}

function post(path, payload) {
  return request(path, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// ---- Endpoint-endpoint spesifik (sesuai src/api/routes/*.py) ----

export const api = {
  health: () => get('/health'),

  // Station
  getStations: () => get('/station/'),
  getStation: (stationId) => get(`/station/${stationId}`),

  // Measurement
  getLatestMeasurement: (stationId) => get(`/measurement/latest/${stationId}`),
  getMeasurementHistory: (stationId, limit = 24) =>
    get(`/measurement/history/${stationId}?limit=${limit}`),

  // Prediction
  predict: (stationId) => post('/prediction/', { station_id: stationId }),
}

export { ApiError }
