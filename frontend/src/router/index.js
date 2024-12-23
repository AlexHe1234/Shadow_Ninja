// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [

  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),

    beforeEnter: (to, from, next) => {
      const isLoggedIn = localStorage.getItem('is_login') === 'true';
      if (!isLoggedIn) {
        next({ name: 'Login' });
      } else {
        next();
      }
    },

  },

  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
