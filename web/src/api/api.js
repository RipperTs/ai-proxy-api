import axios from 'axios'
import {Message} from 'element-ui';
import Vue from "vue";

const vm = new Vue()

/**
 * 封装get方法
 * @param url
 * @param params
 * @returns {Promise<unknown>}
 * @private
 */
export function _apiGet(url, params) {
  return new Promise((resolve, reject) => {
    url = '/web/ai-proxy' + url
    axios.get(url, {
      params: params,
      headers: {
        'ai-proxy-token': vm.$ls.get('user_info')?.access_token || null
      }
    }).then(res => {
      if (res.status !== 200) {
        Message.error(res.data.msg);
        return;
      }
      if (res.data.code !== 0) {
        Message.error(res.data.msg);
        reject(res.data)
        return;
      }
      resolve(res.data)
    }).catch(err => {
      const response = err.response
      Message.error(response.data.msg);
      if (response.status === 401){
        window.location.href  = '/login'
      }
      reject(response.data)
    })
  })
}

/**
 * 获取post请求
 * @param url
 * @param data
 * @returns {Promise<unknown>}
 * @private
 */
export function _apiPost(url, data) {
  return new Promise((resolve, reject) => {
    url = '/web/ai-proxy' + url
    axios.post(url, data,{
      headers: {
        'ai-proxy-token': vm.$ls.get('user_info')?.access_token || null
      }
    }).then(res => {
      if (res.status !== 200) {
        Message.error(res.data.msg);
        return;
      }
      if (res.data.code !== 0) {
        Message.error(res.data.msg);
        reject(res.data)
        return;
      }
      resolve(res.data)
    }).catch(err => {
      const response = err.response
      Message.error(response.data.msg);
      if (response.status === 401){
        window.location.href  = '/login'
      }
      reject(response.data)
    })
  })
}
