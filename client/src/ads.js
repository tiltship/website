function getFbc() {
  return new URL(window.location).searchParams.get('fbclid')
}

function getGclid() {
  const id = new URL(window.location).searchParams.get('gclid')
}

export function getAdIds() {
  return Promise.all([getFbc(), getGclid()]).then(([fbc, gclid ]) => {
    return { fbc, gclid }
  })
}
