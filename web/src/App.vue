<template>
  <div id="app">
    <Header :user_info="user_info" v-if="isShowGlobalModule"></Header>
    <router-view />
  </div>
</template>
<script>
import Header from "@/components/Header";

export default {
  components: {
    Header
  },
  data() {
    return {
      user_info: {
        username: '',
        card: '0',
        avatar: '',
      },
    }
  },
  computed: {
    isShowGlobalModule() {
      return this.$route.meta.title !== '404' && this.$route.meta.title !== '用户登录' && this.$route.meta.title !== '用户注册'
    }
  },
}
</script>


