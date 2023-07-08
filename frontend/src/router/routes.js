import HomeView from '../pages/HomeView.vue'
import FeatureView from '../pages/FeatureView.vue'
import LogInView from '../pages/LogInView.vue'
import LogOutView from '../pages/LogOutView.vue'
import DashboardView from '../pages/DashboardView.vue'
import SignUpView from '../pages/SignUpView.vue'
import DatabaseView from '../pages/DatabaseView.vue'
import ErrorNotFound from '../pages/ErrorNotFound.vue'
import TestView from '../pages/TestView.vue'


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
    path: '/logout',
    name: 'logout',
    component: LogOutView,
    meta: {
      requiresAuth: true
    }
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
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/databases/:databaseName(\\S+)',
    name: 'database',
    component: DatabaseView,
    // meta: {
    //   requiresAuth: true
    // },
  },
    {
      path: '/test',
      name: 'test',
      component: TestView,
      meta: {
        requiresAuth: true
      }
    },
  // {
  //   path: '/databases/:database/query?',
  //   name: 'home',
  //   component: RecordsView,
  //   meta: {
  //     requiresAuth: true
  //   }
  // },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    name: 'error404',
    component: ErrorNotFound
  }
]

export default routes
