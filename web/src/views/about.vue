<template>
  <div class="container">
    <Header menu-name="/about"></Header>
    <h1>/about</h1>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
export default {
  components: {
    Header
  },
  data() {
    return {

    }
  },
  computed: { },
  watch: { },
  created() {

  },
  mounted() {
    let _this = this;

  },
  methods: {

  },

  //切记页面销毁需要销毁
  destroyed() {
    let _this = this
  },
}
</script>
<style lang="scss" scoped>

</style>