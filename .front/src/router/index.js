import Vue from 'vue'
import VueRouter from 'vue-router'
import Terminal from '../views/Terminal.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/terminal',
    name: 'Terminal',
    component: Terminal
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
