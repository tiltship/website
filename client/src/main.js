import drawTree from './tree'
import Consent from './Consent.svelte'
import './css/custom.css'

const app = new Consent({
  target: document.querySelector('#app')
})

// Draw cool tree
drawTree(document.querySelector('#tree'))

export default app
