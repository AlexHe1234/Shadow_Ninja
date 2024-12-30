// Composables
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true },
    redirect: '/search',
    children: [
      {
        path: '/browse',
        name: 'Browse',
        component: () => import('../views/Browse.vue'),
      },
      {
        path: '/search',
        name: 'Search',
        component: () => import('../views/Search.vue'),
      },
    ],
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
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('is_login') === 'true';
  if (to.meta.requiresAuth && !isLoggedIn) {
    console.log('illegal access blocked')
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
