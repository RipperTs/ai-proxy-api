<template lang="html">
  <el-row>
    <el-col :span="12" :offset="6">
      <div class="login">
        <el-row slot="body" :gutter="0">
          <el-col :span="24" :xs="24" :sm="16" :md="16" :lg="16">
            <div class="login-form">
              <div class="card-block">
                <h1>用户注册</h1>
                <div class="input-group m-b-1">
                  <span class="input-group-addon"><i class="el-icon-user"></i></span>
                  <input type="text" class="form-control" placeholder="请输入用户名" v-model="form.username">
                </div>
                <div class="input-group m-b-1">
                  <span class="input-group-addon"><i class="el-icon-message"></i></span>
                  <input type="text" class="form-control" placeholder="请输入邮箱" v-model="form.email">
                </div>
                <div class="input-group m-b-2">
                  <span class="input-group-addon"><i class="el-icon-lock"></i></span>
                  <input type="password"  class="form-control" placeholder="请输入密码" v-model="form.password">
                </div>
                <div class="input-group m-b-2">
                  <span class="input-group-addon"><i class="el-icon-lock"></i></span>
                  <input type="password" class="form-control" placeholder="请再次输入密码" v-model="form.re_password">
                </div>
                <div class="row">
                  <el-row>
                    <el-col :span="12">
                      <el-button type="primary" class="btn btn-primary p-x-2" @click="login">注 册</el-button>
                    </el-col>
                  </el-row>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="24" :xs="24" :sm="8" :md="8" :lg="8">
            <div class="login-register">
              <div class="card-block">
                <h2>登录</h2>
                <p>如果您已经拥有此平台账号,且账号已经通过验证,可以直接登录!</p>
                <el-button type="danger" class="btn btn-primary active m-t-1" @click="toLogin"> 立即登录</el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-col>
  </el-row>
</template>

<script>

import {_apiPost} from "@/api/api";

export default {
  name: 'login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    login() {
      if (!this.form.email) {
        this.$message.error('请输入邮箱')
        return false
      }
      if (!this.form.password) {
        this.$message.error('请输入密码')
        return false
      }
      if (this.form.password.length < 6) {
        this.$message.error('密码长度不能小于6位')
        return false
      }
      if (!this.form.re_password) {
        this.$message.error('请再次输入密码')
        return false
      }
      if (this.form.password !== this.form.re_password) {
        this.$message.error('两次输入的密码不一致')
        return false
      }
      // 检查邮箱格式是否正确
      const reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!reg.test(this.form.email)) {
        this.$message.error('邮箱格式不正确')
        return false
      }
      _apiPost('/api/register-user', this.form).then(res => {
        this.$message.success('注册成功,请联系管理员进行验证后才可正常使用.')
        this.$router.push({path: '/login'})
      })
    },

    toLogin(){
      this.$router.push({path: '/login'})
    },

  }
}
</script>

<style>
.login {
  margin-top: 160px;
  width: 100%;
  border: 1px solid #cfd8dc;
  margin-right: auto !important;
  margin-left: auto !important;
  display: table;
  table-layout: fixed;
  background-color: #ae3036;
}

.login .el-button {
  border-radius: 0;
}

.login .el-button.forgot, .login .el-button.forgot:hover {
  border: none;
}

.login .login-form {
  background-color: #FFFFFF;
  width: 100%;
  height: 100%;
  display: block;

}

.login .login-form .card-block {
  padding: 35px;
}

.login .login-form .card-block p {
  margin: 15px 0;
}

.input-group {
  width: 100%;
  display: table;
  border-collapse: separate;
  margin-bottom: 20px !important;
}

.input-group, .input-group-btn, .input-group-btn > .btn, .navbar {
  position: relative;
}

.input-group-addon:not(:last-child) {
  border-right: 0;
}

.input-group-addon, .input-group-btn {
  min-width: 40px;
  white-space: nowrap;
  vertical-align: middle;
  width: 1%;
}

.btn-link:focus, .btn-link:hover {
  color: #ae3036;
  text-decoration: underline;
  background-color: transparent;
}

.btn-link, .btn-link:active, .btn-link:focus, .btn-link:hover {
  border-color: transparent;
}

.btn.focus, .btn:focus, .btn:hover {
  text-decoration: none;
}

.input-group-addon {
  padding: .5rem .75rem;
  margin-bottom: 0;
  font-size: 1.1rem;
  font-weight: 400;
  line-height: 1.75rem;
  color: #fff;
  text-align: center;
  background-color: #ae3036;
  border: 1px solid rgba(0, 0, 0, .15);
}

.input-group .form-control, .input-group-addon, .input-group-btn {
  display: table-cell;
}

.input-group .form-control {
  position: relative;
  z-index: 2;
  float: left;
  margin-bottom: 0;
}

.form-control {
  width: 90%;
  padding: .5rem .75rem;
  font-size: .9rem;
  line-height: 1.75rem;
  color: #607d8b;
  background: #fff none;
  background-clip: padding-box;
  border: 1px solid rgba(0, 0, 0, .15);
  font-weight: 500;
  transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
}

.login .login-form .card-block .row {
  display: block;
  margin: 15px 0;
}

.login .login-register {
  width: 100%;
  height: 100%;
  display: block;
  background-color: #ae3036;
  color: #fff;
}

.login .login-register .card-block {
  text-align: center !important;
  padding: 30px;
}

.login .login-register .card-block p {
  text-align: left !important;
  margin: 15px 0;
  height: 100px;
}
</style>
