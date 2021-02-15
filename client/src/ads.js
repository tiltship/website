function getFbc() {
  const fbclid = new URL(window.location).searchParams.get('fbclid')
  if (!fbclid) return
  const now = Date.now()
  return `fb.1.${now}.${fbclid}`
}

export function getTrackingParams() {
  const obj = {}
  const url = new URL(window.location)
  url.searchParams.forEach((v, k) => {
    obj[k] = v
  })

  window.history.replaceState({}, document.title, url.pathname)
  const fbc = getFbc()
  return {...obj, fbc }
}
