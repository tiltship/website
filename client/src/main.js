import drawTree from './tree'
import Consent from './Consent.svelte'
import { getAdIds } from './ads'
import { post } from './api'
import './css/custom.css'

const app = new Consent({
  target: document.querySelector('#app')
})

// Draw cool tree
drawTree(document.querySelector('#tree'))

// Make page_visit event
getAdIds()
  .then(tracking_data => post('events', {subtype: 'page_visit', tracking_data }))
  .catch(e => console.error(`Error sending page_visit: ${e}`))

export default app
