import drawTree from './tree'
import Consent from './Consent.svelte'
import { spent } from './events'
import './css/custom.css'

const app = new Consent({
  target: document.querySelector('#app')
})


drawTree(document.querySelector('#tree'))
spent(30, 'dwelled')

export default app
