import { createApp, vaporInteropPlugin } from 'vue'
// import { createVaporApp } from 'vue'

import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './utils/ws'

const pinia = createPinia()

const app = createApp(App)
// const app = createVaporApp(App)

app.use(vaporInteropPlugin)
app.use(pinia)
app.use(router)

app.mount('#app')
