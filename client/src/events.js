export function spent(seconds, tag) {
  setTimeout(() => {
    gtag('event', tag, {})
    fbq('trackCustom', tag)
  }, seconds * 1000)
}
