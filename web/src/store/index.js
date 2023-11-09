import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    dataList: [],
    isBack: false,
    searchScrollTop: 0,
  },
  getters: {
    getDataList: state => () => {
      let arr = [];
      const res = arr.concat(state.dataList);
      return res;
    }

  },
  mutations: {
    setSearchScrollTop: (state, data) => {
      state.searchScrollTop = data;
    },
    setIsBack: (state, isBack) => {
      state.isBack = isBack;
    },
    addDataList: (state, data) => {
      state.dataList.push(data);
    },
    clearDataList: (state) => {
      // state.dataList.length = 0;
      state.dataList.length = 0;
      console.log(state.dataList.length);
    }
  },
  actions: {}
})
