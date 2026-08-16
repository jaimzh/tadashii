import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ResultView from '@/views/ResultView.vue'
import WatchLaterView from '@/views/WatchLaterView.vue'
import HelpView from '@/views/HelpView.vue'
import NotFoundView from '@/views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Tadashii — AI Anime Recommendations for Your Mood',
        description:
          'Describe what you feel like watching and get focused AI-assisted anime recommendations matched to your mood, preferred story, and exclusions.',
        canonical: '/',
      },
    },
    {
      path: '/results',
      name: 'results',
      component: ResultView,
      meta: {
        title: 'Your Anime Recommendations | Tadashii',
        description: 'Your personalized Tadashii anime recommendation results.',
        noindex: true,
      },
    },
    {
      path: '/watch-later',
      name: 'watch-later',
      component: WatchLaterView,
      meta: {
        title: 'Watch Later | Tadashii',
        description: 'Your locally saved Tadashii Watch Later list.',
        noindex: true,
      },
    },
    {
      path: '/help',
      name: 'help',
      component: HelpView,
      meta: {
        title: 'Help & Information | Tadashii',
        description:
          'Learn how to describe what you want to watch, understand Tadashii recommendations, and manage your Watch Later list.',
        canonical: '/help',
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
      meta: {
        title: 'Page Not Found | Tadashii',
        description: 'The requested Tadashii page could not be found.',
        noindex: true,
      },
    },
  ],
})

export default router
