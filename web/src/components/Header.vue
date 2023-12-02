<template>
  <div>
    <div class="top-navbar">
      <div class="nav-left">
        <div class="system-box">
          <div class="logo-img">
            <img class="logo-icon"
                 src="data:image/png;base64,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"
                 alt="">
          </div>
          <div class="title-content" @click.stop="goHome()">{{ title }}</div>
        </div>
        <div class="ribbon-main">
          <el-menu text-color="#333" active-text-color="#ae3036"
                   :default-active="$route.meta.activeMenuPath" router
                   class="el-menu-box" mode="horizontal">
            <el-menu-item :index="item.path" class="menu-item-class"
                          v-for="(item,index) in router" :key="index"
                          v-if="item.meta.show === true"
            >{{ item.meta.title }}
            </el-menu-item>
          </el-menu>
        </div>
      </div>
      <div class="nav-right">
        <div class="about-box">{{ user_info?.username }}</div>
        <div class="about-box">
          <el-dropdown :hide-on-click="false" @command="command">
            <el-avatar style="width: 30px;height: 30px"
                       :src="'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'">
              <template #default>user</template>
            </el-avatar>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-unlock" command="updatePwd">更改密码
              </el-dropdown-item>
              <el-dropdown-item icon="el-icon-switch-button" command="signOut">退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
    </div>

    <el-dialog title="更改密码" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="新密码" :label-width="formLabelWidth">
          <el-input v-model="form.password" show-password style="width:300px" type="password"
                    autocomplete="on"></el-input>
        </el-form-item>
        <el-form-item label="再次确认" :label-width="formLabelWidth">
          <el-input v-model="form.re_password" type="password" show-password style="width:300px"
                    autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="onSubmit()">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import router from "@/router";
import {_apiPost} from "@/api/api";

export default {
  name: "Header",
  props: {
    title: {
      type: String,
      default: "Proxy API"
    }
  },
  data() {
    return {
      router: router.options.routes,
      menuName: '/',
      dialogFormVisible: false,
      form: {
        password: '',
        new_password: '',
      },
      formLabelWidth: '100px'
    }
  },
  computed: {
    eventHandler() {
      return {
        signOut: () => {
          this.signOut();
        },
        updatePwd: () => {
          this.dialogFormVisible = true
        },
      };
    },
    user_info() {
      return this.$ls.get('user_info')
    },
  },
  methods: {

    onSubmit() {
      if (this.form.password.trim() === '') {
        this.$message.error('请输入新密码')
        return false
      }
      if (this.form.password.trim().length < 6) {
        this.$message.error('密码长度不能小于6位')
        return false
      }
      if (this.form.re_password.trim() === '') {
        this.$message.error('请再次输入新密码')
        return false
      }
      if (this.form.password !== this.form.re_password) {
        this.$message.error('两次输入的密码不一致')
        return false
      }
      _apiPost('/api/v1/user/update-password', this.form).then(res => {
        this.$message.success('密码修改成功,请重新登录')
        this.dialogFormVisible = false
        this.$ls.set('user_info', '')
        this.$router.push({path: '/login'})
      })
    },

    command(e) {
      this.eventHandler[e]();
    },

    signOut(e) {
      this.$confirm('确定退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$ls.set('user_info', '')
        this.$router.push({path: '/login'})
      })
    },


    goHome() {
      // 本页跳转
      window.location.href = '/';
    },
  }
}
</script>

<style lang="scss" scoped>
.top-navbar {
  display: flex;
  background-color: #fff;
  align-items: center;
  min-height: 55px;
  height: 55px;
  max-height: 55px;
  width: 100%;
  justify-content: space-between;
  box-shadow: 0 0 12px rgb(0 0 0 / 11%);
  z-index: 99;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;

  .nav-left {
    width: 50%;
    display: flex;
    background-color: #fff;
    align-items: center;
    justify-content: left;
    height: 100%;

    .system-box {
      display: flex;
      align-items: center;
      height: 100%;

      .logo-img {
        width: 20px;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: 20px;

        .logo-icon {
          width: 28px;
          border-radius: 4px;

          img {
            width: 100%;
          }
        }
      }

      .title-content {
        display: flex;
        align-items: center;
        margin-left: 10px;
        font-weight: 500;
        font-size: 17px;
        color: #333;
        cursor: pointer;
        height: 100%;
        white-space: nowrap;
      }
    }

    .search-box {
      margin-left: 30px;
      //z-index: 99999;
    }
  }


}

::v-deep .el-input__inner {
  border-radius: 0 40px 40px 0;
}

::v-deep .el-input .el-input-group__prepend {
  background-color: #fff;
  border-radius: 40px 0 0 40px;
}

.ribbon-main {
  margin-left: 30px;

  .menu-item-class {
    font-weight: 500;
  }
}

.el-menu-box {
  height: 55px;
  border: none;
}

::v-deep .el-menu--horizontal > .el-menu-item {
  height: 51px !important;
}

::v-deep .el-avatar > img {
  width: 100%;
}

.nav-right {
  width: 40%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: right;

  .about-box {
    margin-right: 20px;
    color: #555;
    cursor: pointer;
    border: 1px transparent;
    border-radius: 4px;
    font-size: 16px;
    margin-top: 5px;

    &:first-child {
      margin-right: 20px;
    }
  }

  .options {
    margin-right: 20px;
  }
}
</style>
