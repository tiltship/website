import Cookies from 'js-cookie';
import FingerprintJS from '@fingerprintjs/fingerprintjs';

function getFbp() {
  return Cookies.get('_fbp')
}

function getFbc() {
  const fbc = new URL(window.location).searchParams.get('fbclid')
  if (fbc) {
    return fbc
  }

  const cookie = Cookies.get('_fbc')
  if (cookie) {
    return cookie.value.split('.')[3]
  }
}

function getGclid() {
  const id = new URL(window.location).searchParams.get('gclid')
  return id || Cookies.get('gclid')
}

function setCookies(ids) {
  // Quick hack to keep gclid to use in Conversions API
  // You'd think you could do this with the _ga cookie...

  Cookies.set('gclid', ids.google.gclid, {sameSite: 'Lax', secure: true, expires: 31})
}

function getGID() {
  return Cookies.get('_ga')
}

function getFingerprint() {
  return FingerprintJS
    .load()
    .then(fp => fp.get())
    .then(res => {
      // this is massive and ugly and i dunno what to do with
      // it anyways...
      delete res.components.canvas
      return res
    })
}

export function getAdIds() {
  return Promise.all([getFbc(), getFbp(), getGclid(), getGID(), getFingerprint()]).then(([fbc, fbp, gclid, ga, fingerprint]) => {

    const data = { facebook: {fbc, fbp}, google: {gclid, ga}, fingerprint }
    return { data, setCookies: setCookies.bind(null, data)}
  })
}
