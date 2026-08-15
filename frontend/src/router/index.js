import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ResultView from '@/views/ResultView.vue'
import WatchLaterView from '@/views/WatchLaterView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/results', name: 'results', component: ResultView },
    { path: '/watch-later', name: 'watch-later', component: WatchLaterView },
  ],
})

export default router
