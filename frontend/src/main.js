import '@fontsource/inter/latin-400.css'
import '@fontsource/inter/latin-500.css'
import '@fontsource/inter/latin-600.css'
import '@fontsource/inter/latin-700.css'
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

createApp(App).use(router).mount('#app')
