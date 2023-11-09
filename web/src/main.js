import Vue from "vue";
import App from "./App.vue";
import Vant from "./vant.js";
import router from './router';
import store from './store/index'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/icons' // icon
import {updateElementTheme} from "@/common/update-element-theme";
import Storage from 'vue-ls'
import Base from "@/utils/base";

Vue.config.productionTip = false;


// vue-ls 的配置
const storageOptions = {
  namespace: 'aiapi_',   // key 键的前缀（随便起）
  name: 'ls',          // 变量名称（随便起） 使用方式：Vue.变量名称 或 this.$变量名称
  storage: 'local'     // 作用范围：local、session、memory
}

Vue.use(Storage, storageOptions)
Vue.use(Vant);
Vue.use(ElementUI, {size: 'small'});
Vue.use(Base);

// 正式环境清除所有console.log
if (process.env.NODE_ENV === 'production') {
  if (window) {
    window.console.log = function () {
    };
  }
}


const initApp = async () => {
  try {
    await updateElementTheme({
      oldTheme: '#409EFF',
      primaryColor: '#ae3036',
      cssUrl: '/theme-chalk/index.css'
    })

    new Vue({
      router,
      store,
      render: (h) => h(App),
    }).$mount('#app');
  } catch (error) {
    new Vue({
      router,
      store,
      render: (h) => h(App),
    }).$mount('#app');
    console.error('主题更新失败', error)
  }
}

initApp()

