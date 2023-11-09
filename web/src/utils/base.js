/*
*
*常用工具函数
*
*/

'use strict';
const UA = window.navigator.userAgent.toLowerCase()
const isFF = UA && UA.match(/firefox\/(\d+)/)

export default {
  /**
   * 每个插件都有的install方法，用于安装插件
   * @param {Object} Vue - Vue类
   * @param {Object} [pluginOptions] - 插件安装配置
   */
  install: function (Vue, option) {

    Vue.prototype.$scale = function () {
      let bl = 1.25 / window.devicePixelRatio
      let fl = (isFF ? screen.width / bl : screen.width) / 2048
      return bl * fl;
    }


    Vue.prototype.$getQueryString = function (name) {
      var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
      var r = window.location.search.substr(1).match(reg);
      if (r != null) {
        return decodeURI(r[2]);
      }
      return null;
    }

    //随机生成十六进制颜色
    Vue.prototype.$randomHexColor = function () {
      return '#' + ('00000' + (Math.random() * 0x1000000 << 0).toString(16)).substr(-6);
    }

    /**
     * 改变地址栏参数
     * @param key
     * @param value
     */
    Vue.prototype.$historyPushState = function (key, value) {
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.set(key, value);
      window.history.pushState(null, null, newUrl);
    }
  }
}
