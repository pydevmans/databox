import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FeatureView from '../views/FeatureView.vue'
import LogInView from '../views/LogInView.vue'
// import { HomeView, LogInView, SignUpView, FeatureView } from '../views/HomeView.vue'
// import { ProfileView, DashboardView, DatabaseView, QueryView } from "../views/LoggedUserView.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // {
    //   path: '/login',
    //   name: 'login',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    // {
    //   path: '/signup',
    //   name: 'signup',
    //   component: SignUpView
    // },
    {
      path: '/features',
      name: 'features',
      component: FeatureView
    },
    // {
    //   path: '/profile',
    //   name: 'profile',
    //   component: ProfileView
    // },
    // {
    //   path: '/dashboard',
    //   name: 'dashboard',
    //   component: DashboardView
    // },
    // {
    //   path: '/dashboard/<database>',
    //   name: 'database',
    //   component: DatabaseView
    // },
    // {
    //   path: '/dashboard/<database>/query?',
    //   name: 'home',
    //   component: QueryView
    // },
  ]
})

export default router
