import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// Global overlay instance (we'll create it from App.vue)
declare global {
  interface Window {
    dialOverlay: any | null
  }
}

window.dialOverlay = null

createApp(App).mount('#app')

