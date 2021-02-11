export function spent(seconds, tag) {
  setTimeout(() => {
    gtag('event', tag, {
      event_category: 'engagement'
    })
    fbq('trackCustom', tag)
  }, seconds * 1000)
}
