import VueRouter from 'vue-router'
import Vue from 'vue'

const title = 'Proxy API'

Vue.use(VueRouter)
var routes = [
  {
    path: '/',
    meta: {title: '渠道', show: true, activeMenuPath: '/channels'},
    component: () => import("@/views/channels.vue"),
  },
  {
    path: '/tokens',
    meta: {title: '令牌', show: true, activeMenuPath: '/tokens'},
    component: () => import("@/views/tokens.vue"),
  },
  {
    path: '/logs',
    meta: {title: '日志', show: true, activeMenuPath: '/logs'},
    component: () => import("@/views/logs.vue"),
  },
  {
    path: '/about', component: () => import("@/views/about.vue"),
    meta: {title: '关于', show: true, activeMenuPath: '/about'},
  },
  {
    path: '/login', component: () => import("@/views/login.vue"),
    meta: {title: '用户登录', show: false, activeMenuPath: '/login'},
    children: [],
  },
  {
    path: '/404',
    meta: {title: '404', show: false, activeMenuPath: '/404'},
    component: () => import('@/views/NotFound'),
    children: [],
  },
  // 所有未定义路由，全部重定向到404页
  {
    path: '*',
    redirect: '/404',
    meta: {title: '*', show: false, activeMenuPath: '/404'},
  }

];

const router = new VueRouter({
  mode: 'history',
  scrollBehavior: () => ({y: 0}),
  routes
})

function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}

// 路由后置守卫
router.afterEach(to => {
  document.title = getPageTitle(to.meta.title)
})


export default router

