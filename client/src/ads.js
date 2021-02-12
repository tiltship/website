function getFbc() {
  const fbclid = new URL(window.location).searchParams.get('fbclid')
  if (!fbclid) return
  const now = Date.now()
  return `fb.1.${now}.${fbclid}`
}

function getGclid() {
  const id = new URL(window.location).searchParams.get('gclid')
  if (id) return id
}

export function getAdIds() {
  return Promise.all([getFbc(), getGclid()]).then(([fbc, gclid ]) => {
    return { fbc, gclid }
  })
}
