<template lang="html">
  <el-row>
    <el-col :span="12" :offset="6">
      <div class="login">
        <el-row slot="body" :gutter="0">
          <el-col :span="24" :xs="24" :sm="16" :md="16" :lg="16">
            <div class="login-form">
              <div class="card-block">
                <h1>AI-Proxy-API</h1>
                <p class="text-muted">邮箱/密码登录</p>
                <div class="input-group m-b-1">
                  <span class="input-group-addon"><i class="el-icon-user"></i></span>
                  <input type="text" class="form-control" placeholder="请输入邮箱" v-model="form.email">
                </div>
                <div class="input-group m-b-2">
                  <span class="input-group-addon"><i class="el-icon-lock"></i></span>
                  <input type="password" class="form-control" placeholder="请输入密码" v-model="form.password"
                         @keyup.enter="login">
                </div>
                <div class="row">
                  <el-row>
                    <el-col :span="12">
                      <el-button type="primary" class="btn btn-primary p-x-2" @click="login">登 录</el-button>
                    </el-col>
                    <el-col :span="12">
                      <el-button type="text" disabled class="btn btn-link forgot" style="float:right;">忘记密码?
                      </el-button>
                    </el-col>
                  </el-row>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="24" :xs="24" :sm="8" :md="8" :lg="8">
            <div class="login-register">
              <div class="card-block">
                <h2>注册</h2>
                <p>平台注册后无法自动登录,需联系管理员.</p>
                <el-button type="danger" class="btn btn-primary active m-t-1"> 马上注册</el-button>
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
      _apiPost('/api/login-user', this.form).then(res => {
        this.$ls.set('user_info', res.data)
        this.$router.push({path: '/'})
      })
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
