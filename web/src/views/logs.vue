<template>
  <div class="container">
    <div class="table-box">
      <el-table
        :data="tableData"
        height="78vh"
        stripe
        ref="table"
        border
        v-loading="isLoading"
        :header-cell-style="{background: '#f3f3f3',fontWeight: 'bold',fontSize: '14px'}"
        style="width: 100%">
        <el-table-column
          label="令牌">
          <template slot-scope="scope">
            <el-tag>{{ scope.row.token_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="渠道名称">
          <template slot-scope="scope">
            <el-tag effect="plain" type="warning">{{ scope.row.channel_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="模型名称">
          <template slot-scope="scope">
            <el-tag effect="plain" type="success">{{ scope.row.model_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="request_tokens"
          width="200"
          label="请求token">
        </el-table-column>
        <el-table-column
          prop="created_time"
          align="center"
          width="200"
          label="创建时间">
        </el-table-column>
        <el-table-column
          prop="content"
          label="备注">
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
  </div>
</template>

<script>
import {_apiGet} from "@/api/api";

export default {
  components: {},
  data() {
    return {
      tableData: [],
      page: 1,
      limit: 60,
      total: 0,
      isLoading: true
    }
  },
  created() {
    this.getLogs()
  },
  methods: {

    getLogs() {
      _apiGet('/api/v1/log/log-list', {page: this.page, limit: this.limit}).then(res => {
        this.tableData = res.data.list
        this.total = res.data.total_count
        this.isLoading = false
      }).catch(() => {
        this.isLoading = false
      })
    },

    currentChange(e) {
      this.page = e
      this.isLoading = true
      this.getLogs()
      this.$nextTick(() => {
        this.$refs.table.bodyWrapper.scrollTop = 0
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.table-box {
  margin-top: 30px;
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


.input-width {
  width: 450px;
}
</style>
