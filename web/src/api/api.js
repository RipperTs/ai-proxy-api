import axios from 'axios'
import {Message} from 'element-ui';

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
      params: params
    }).then(res => {
      if (res.status !== 200) {
        console.error('接口请求失败: ', res)
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
      Message.error(err.data);
      reject(err.data)
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
    axios.post(url, data).then(res => {
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
      Message.error(err.data);
      reject(err.data)
    })
  })
}
