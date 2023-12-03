<template>
  <div class="container">
    <div class="table-box">
      <div class="btn-box">
        <el-button size="mini" @click="dialogFormVisible=true">添加渠道</el-button>
      </div>
      <el-table
        :data="channelList"
        height="75vh"
        stripe
        ref="table"
        border
        v-loading="isLoading"
        :header-cell-style="{background: '#f3f3f3',fontWeight: 'bold',fontSize: '14px'}"
        style="width: 100%">
        <el-table-column
          prop="name"
          width="160"
          label="名称">
        </el-table-column>
        <el-table-column
          prop="type"
          label="类型"
          align="center"
          width="120">
          <template slot-scope="scope">
            <el-tag effect="plain" type="success" v-if="scope.row.type === 1">OpenAI</el-tag>
            <el-tag effect="plain" type="warning" v-if="scope.row.type === 2">OhMyGPT</el-tag>
            <el-tag effect="plain" type="danger" v-if="scope.row.type === 3">OneAPI</el-tag>
            <el-tag effect="plain" type="primary" v-if="scope.row.type === 4">OpenSB</el-tag>
            <el-tag effect="plain" type="success" v-if="scope.row.type === 5">灵石Qwen</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          width="100"
          align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag type="success" class="cursor" @click="setStatus(scope.row,2)"
                    v-if="scope.row.status === 1">已启用
            </el-tag>
            <el-tag type="danger" class="cursor" @click="setStatus(scope.row,1)" v-else>已禁用
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="余额"
          align="center"
          width="80">
          <template slot-scope="scope">
            <span>{{ scope.row.balance / 100 }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_time"
          width="180"
          align="center"
          label="创建时间">
        </el-table-column>
        <el-table-column
          width="150"
          align="center"
          label="请求耗时">
          <template slot-scope="scope">
            <el-tag type="info" v-if="scope.row.response_time === 0">未测试</el-tag>
            <el-tag type="success" v-else>{{ scope.row.response_time }} ms</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作">
          <template slot-scope="scope">
            <el-button type="success" @click="testChannel(scope.row)"
                       :disabled="scope.row.type === 5" size="mini">测试
            </el-button>
            <el-button type="warning" @click="updateBalance(scope.row)"
                       :disabled="scope.row.type === 5" size="mini">更新余额
            </el-button>
            <el-button type="primary" size="mini" @click="doEdit(scope.row.id)">编辑</el-button>
            <el-button type="danger" @click="delChannel(scope.row)" size="mini">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          background
          @current-change="currentChange"
          :page-size.sync="limit"
          :current-page.sync="page"
          layout="prev, pager, next"
          :total="total">
        </el-pagination>
      </div>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogFormVisible" @close="closeDialog">
      <el-form :model="form">
        <el-form-item label="渠道名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" class="input-width"></el-input>
        </el-form-item>
        <el-form-item label="渠道类型" :label-width="formLabelWidth">
          <el-select v-model="form.type" placeholder="请选择渠道类型">
            <el-option :value="1" label="OpenAI"></el-option>
            <el-option :value="2" label="OhMyGPT"></el-option>
            <el-option :value="3" label="OneAPI"></el-option>
            <el-option :value="4" label="OpenSB"></el-option>
            <el-option :value="5" label="灵石Qwen"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="包含模型" :label-width="formLabelWidth">
          <el-input v-model="form.models" :rows="6" style="width: 560px;" type="textarea"
                    class="input-width"></el-input>
        </el-form-item>
        <el-form-item label="鉴权秘钥" :label-width="formLabelWidth">
          <el-input v-model="form.key" class="input-width"></el-input>
        </el-form-item>
        <el-form-item label="请求地址" :label-width="formLabelWidth">
          <el-input v-model="form.base_url" :disabled="form.type === 5"
                    class="input-width"></el-input>
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
import {_apiGet, _apiPost} from "@/api/api";

export default {
  components: {},
  data() {
    return {
      channelList: [],
      page: 1,
      limit: 30,
      total: 0,
      isLoading: true,
      dialogFormVisible: false,
      form: {
        name: '',
        type: 1,
        models: 'gpt-3.5-turbo,gpt-3.5-turbo-0301,gpt-3.5-turbo-0613,gpt-3.5-turbo-16k,gpt-3.5-turbo-16k-0613,gpt-3.5-turbo-instruct,text-embedding-ada-002,text-davinci-003,text-davinci-002,gpt-3.5-turbo-1106',
      },
      formLabelWidth: '100px',
      is_edit: false,
      dialogTitle: '添加渠道',
      edit_channel_id: 0,
    }
  },
  created() {
    this.getChannelsList()
  },
  mounted() {
  },
  methods: {

    closeDialog() {
      this.is_edit = false
      this.dialogTitle = '添加渠道'
      this.form = {
        name: '',
        type: 1,
        models: 'gpt-3.5-turbo,gpt-3.5-turbo-0301,gpt-3.5-turbo-0613,gpt-3.5-turbo-16k,gpt-3.5-turbo-16k-0613,gpt-3.5-turbo-instruct,text-embedding-ada-002,text-davinci-003,text-davinci-002,gpt-3.5-turbo-1106',
      }
      this.edit_channel_id = 0
    },

    doEdit(id) {
      this.dialogTitle = '编辑渠道'
      this.is_edit = true
      this.edit_channel_id = id
      _apiGet(`/api/v1/channel/channel-info`, {
        channel_id: id
      }).then(res => {
        this.form = res.data
        this.dialogFormVisible = true
      })
    },

    setStatus(row, status) {
      this.isLoading = true
      _apiGet(`/api/v1/channel/${row.id}/status`, {status: status}).then(res => {
        this.getChannelsList()
      })
    },

    currentChange(e) {
      this.page = e
      this.isLoading = true
      this.getChannelsList()
      this.$nextTick(() => {
        this.$refs.table.bodyWrapper.scrollTop = 0
      })
    },

    getChannelsList() {
      _apiGet('/api/v1/channel/channel-list', {page: this.page, limit: this.limit}).then(res => {
        this.channelList = res.data.list
        this.total = res.data.total_count
        this.isLoading = false
      }).catch(() => {
        this.isLoading = false
      })
    },

    testChannel(row) {
      _apiGet('/api/v1/channel/check-channel', {channel_id: row.id}).then(res => {
        this.getChannelsList()
      })
    },

    updateBalance(row) {
      _apiGet('/api/v1/channel/balance', {channel_id: row.id}).then(res => {
        this.getChannelsList()
      })
    },

    delChannel(row) {
      this.$confirm('此操作将永久删除该渠道, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        _apiPost(`/api/v1/channel/${row.id}/del-channel`).then(res => {
          this.getChannelsList()
        })
      })
    },

    onSubmit() {
      if (this.is_edit) {
        _apiPost(`/api/v1/channel/${this.edit_channel_id}/update-channel`, this.form).then(res => {
          this.getChannelsList()
          this.dialogFormVisible = false
          this.closeDialog()
        })
        return false;
      }
      _apiPost('/api/v1/channel/add-channel', this.form).then(res => {
        this.getChannelsList()
        this.dialogFormVisible = false
        this.closeDialog()
      })
    },

  },
}
</script>
<style lang="scss" scoped>
.table-box {
  margin-top: 30px;
  max-height: 80vh;
  border-radius: 5px;
}

.cursor {
  cursor: pointer;
}

.pagination {
  margin-top: 10px;
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 0 10px #eee;
}

.el-table {
  border-radius: 4px;
  border: none;
  box-shadow: 0 0 10px #eee;
}

.btn-box {
  margin-bottom: 10px;
}

.input-width {
  width: 450px;
}
</style>
