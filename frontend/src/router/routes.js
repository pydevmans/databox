import HomeView from '../pages/HomeView.vue'
import FeatureView from '../pages/FeatureView.vue'
import LogInView from '../pages/LogInView.vue'
import DashboardView from '../pages/DashboardView.vue'
import SignUpView from '../pages/SignUpView.vue'

const routes = [
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
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
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
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView
  },
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
  // Always leave this as last one,
  // but you can also remove it
  // {
  //   path: '/:catchAll(.*)*',
  //   component: () => import('pages/ErrorNotFound.vue')
  // }
]

export default routes
