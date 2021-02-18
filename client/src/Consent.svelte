<script>
  import src from './img/loading.svg'
  import { post } from './api'
  import { visit } from './tracker'
  import { getTrackingParams } from './ads'

  // state variables
  let state = 'empty'
  let email = null
  let start = Date.now()

  // tracking data
  const data = getTrackingParams()

  // track visit (sends via beacon one page hidden)
  // use session: session.push(event) to record events
  const session = visit(data)

  const sendData = (email, td) => {
    const body = { email: email, tracking_data: td }
    return post('signups', body)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    state = 'loading'

    const typeform = import('@typeform/embed')

    // send to server
    sendData(email, data)
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
          onSubmit: () => {

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

    <p>You can unsubscribe at any time by going to <a href="/unsubscribe">tiltship.com/unsubscribe</a> or by a link provided in the emails. Your email will be kept safe and stored along with ad tracking data that records how you got here. We did not place any cookies in your browser. You can request this personal data or request to have it deleted at any time via <a href="mailto:privacy@tiltship.com">privacy@tiltship.com. </a></p>
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
