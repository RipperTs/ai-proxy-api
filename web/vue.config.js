// test
const path = require('path')


function resolve(dir) {
  return path.join(__dirname, './', dir)
}

module.exports = {
  // 根路径 默认使用/ vue cli 3.3+ 弃用 baseUrl
  publicPath: '/', // 此处改为 './' 即可
  productionSourceMap: false,
  // 关闭eslint
  lintOnSave: false,
  devServer: {
    port: 8081,
    // If you want to turn on the proxy, please remove the mockjs /src/main.jsL11
    proxy: {
      '/ai-proxy': {
        target: 'http://127.0.0.1:3000/', // target host
        ws: true, // proxy websockets
        changeOrigin: true, // needed for virtual hosted sites
        pathRewrite: {
          '^/ai-proxy': '' // rewrite path
        }
      }
    }
  },
  css: {
    loaderOptions: {
      sass: {
        // 依次导入的公用的scss变量，公用的scss混入，共用的默认样式
        prependData: `
                    @import "./src/assets/css/global.scss";
                `
      },
    }
  },
  chainWebpack: config => {
    config.module
      .rule('svg')
      .exclude.add(resolve('src/assets/icons'))
      .end();

    config.module
      .rule('icons')
      .test(/\.svg$/)
      .include.add(resolve('src/assets/icons'))
      .end()
      .use('svg-sprite-loader')
      .loader('svg-sprite-loader')
      .options({
        symbolId: 'myicon-[name]'
      });
  },

}
