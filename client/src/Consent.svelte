<script>
  import src from './img/loading.svg'
  import { getAdIds } from ('./ads')

  let state = 'empty'
  let email = null
  let ads = null

  const handleCancel = e => {
    if (e.target === e.currentTarget) {
      e.preventDefault()
      state = 'empty'
    }
  }

  const SERVER_URL = process.env.SERVER_URL || 'http://localhost:1323'

  const sendData = (email, td) => {
    const body = { email: email, tracking_data: td }
    const url = `${SERVER_URL}/signups`
    const opts = { method: 'POST',
                   headers: {'Content-Type': 'application/json'},
                   body: JSON.stringify(body) }
    return fetch(url, opts)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    state = 'loading'

    const typeform = import('@typeform/embed')

    // send to server
    getAdIds()
      .then(data => sendData(email, data))
      .then(async res => {
        const r = await res.json();
        if (!res.ok) {
          throw new Error(r.message);
        }
        return r
      })
      .then(() => typeform)
      .then(({makePopup}) => {
        const formUrl = 'https://form.typeform.com/to/bEzLeP8A'
        const qs = `email=${email}`
        const typeform = makePopup(`${formUrl}?${qs}`, {
          mode: 'drawer_right',
          onSubmit: (event) => {

            typeform.close()
            state = 'finished'
          },
          onClose: () => {
            state = 'finished'
          }
        })

        typeform.open()
      })
      .catch(err => {
        alert(err)
        state = 'empty'
      })
  }

</script>

<h2> Join us </h2>

{#if state === 'empty'}
  <div id="empty-form" class="form-area">
    <p> Sign up to our email list by providing an email address below and we'll send you news and updates about the project. </p>

    <p>You can unsubscribe at any time by going to <a href="/unsubscribe">tiltship.com/unsubscribe</a> or by a link provided in the emails. Your email will be kept safe and stored along with ad tracking data that records how you got here and basic information about your device. We did not place any cookies in your browser. You can request this personal data or request to have it deleted at any time via <a href="mailto:privacy@tiltship.com">privacy@tiltship.com. </a></p>
    <form id="email-form" on:submit={handleSubmit} action="">
      <input bind:value={email} type="email" required="true" placeholder="Email" name="email" />
      <button>Submit</button>
    </form>
  </div>
{/if}

{#if state === 'loading'}
  <div id="loading-form" class="form-area">
    <img alt="loading" src={src}>
  </div>
{/if}

{#if state === 'finished'}
  <div id="finished-form" class="form-area">
    <p> Thank you for signing up! We will be in touch soon. </p>
  </div>
{/if}
