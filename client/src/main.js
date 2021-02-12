import drawTree from './tree'
import Consent from './Consent.svelte'
import './css/custom.css'

const app = new Consent({
  target: document.querySelector('#app')
})


drawTree(document.querySelector('#tree'))
export default app
