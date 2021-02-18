const SERVER_URL = process.env.SERVER_URL || 'http://localhost:1323'

export function post(path, body) {
    const url = `${SERVER_URL}/${path}`
    const opts = { method: 'POST',
                   headers: {'Content-Type': 'application/json'},
                   body: JSON.stringify(body) }
    return fetch(url, opts)
}

export function beacon(path, body){
  navigator.sendBeacon(`${SERVER_URL}/${path}`, body)
}
