<template>
  <div class="container">
    <div class="table-box">
      <div class="btn-box">
        <el-button size="mini" @click="dialogFormVisible=true">添加令牌</el-button>
      </div>
      <el-table
        :data="tableData"
        height="700"
        stripe
        border
        v-loading="isLoading"
        :header-cell-style="{background: '#f3f3f3',fontWeight: 'bold',fontSize: '14px'}"
        style="width: 100%">
        <el-table-column
          prop="name"
          label="名称">
        </el-table-column>
        <el-table-column
          width="100"
          align="center"
          label="状态">
          <template slot-scope="scope">
            <el-tag type="success" class="cursor" @click="setStatus(scope.row,2)" v-if="scope.row.status === 1">已启用</el-tag>
            <el-tag type="danger" class="cursor" @click="setStatus(scope.row,1)" v-else>已禁用</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_time"
          align="center"
          label="创建时间">
        </el-table-column>
        <el-table-column
          prop="expired_time"
          align="center"
          label="到期时间">
        </el-table-column>
        <el-table-column
          label="操作">
          <template slot-scope="scope">
            <el-button type="success" @click="copyKey(scope.row)" size="mini">复制</el-button>
            <el-button type="primary" size="mini" disabled>编辑</el-button>
            <el-button type="danger" @click="delToken(scope.row)" size="mini">删除</el-button>
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
          :total="100">
        </el-pagination>
      </div>
    </div>

    <el-dialog title="添加令牌" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="令牌名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" class="input-width"></el-input>
        </el-form-item>
        <el-form-item label="过期时间" :label-width="formLabelWidth">
          <el-date-picker
            v-model="form.expired_time"
            type="datetime"
            placeholder="选择日期时间"
            default-value="2050-01-01 12:00:00"
            value-format="yyyy-MM-dd HH:mm:ss"
            default-time="12:00:00">
          </el-date-picker>
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
      tableData: [],
      page: 1,
      limit: 30,
      isLoading: true,
      dialogFormVisible: false,
      form: {
        name: '',
        expired_time: '',
      },
      formLabelWidth: '100px',
    }
  },
  created() {
    this.getTokenList()
  },
  mounted() {
  },
  methods: {

    setStatus(row, status) {
      this.isLoading = true
      _apiGet(`/api/token/${row.id}/status`, {status: status}).then(res => {
        this.getTokenList()
      })
    },

    currentChange(e){
      this.page = e
      this.getTokenList()
    },

    copyKey(row){
      this.$copyText(row.key)
        .then(() => {
          this.$message.success('秘钥已成功复制到剪贴板')
        })
        .catch(() => {
          this.$message.error('复制失败')
        });
    },

    getTokenList() {
      _apiGet('/api/token-list', {page: this.page, limit: this.limit}).then(res => {
        this.tableData = res.data
        this.isLoading = false
      }).catch(() => {
        this.isLoading = false
      })
    },

    delToken(row) {
      this.$confirm('此操作将永久删除该令牌, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        _apiPost(`/api/${row.id}/del-token`).then(res => {
          this.getTokenList()
        })
      })
    },

    onSubmit() {
      _apiPost('/api/add-token', this.form).then(res => {
        this.getTokenList()
        this.dialogFormVisible = false
      })
    },

  },
}
</script>
<style lang="scss" scoped>
.table-box {
  margin-top: 30px;
  min-height: 700px;
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
