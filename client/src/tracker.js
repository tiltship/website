import { beacon } from './api';

export function visit(data) {
  let start = Date.now()
  const events = []

  document.addEventListener("visibilitychange", function() {
    if (document.visibilityState === 'visible') {
      start = Date.now()
      events.length = 0
      return
    }

    const duration = Date.now() - start
    const json = JSON.stringify({subtype: 'page_visit',
                                 tracking_data: {...data, session: {duration, events} }})

    beacon('events', json)
  });

  return events
}
