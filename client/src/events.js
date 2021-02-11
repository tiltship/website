export function spent(seconds, tag) {
  setTimeout(() => {
    console.log('spent event')
    gtag('event', tag, {
      event_category: 'engagement',
      event_callback: () => {
        console.log('Sent spent event to Google')
      }
    })
    fbq('trackCustom', tag)
  }, seconds * 1000)
}
