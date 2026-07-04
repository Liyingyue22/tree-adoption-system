<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>订单管理</span>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="orderId" label="订单ID" width="100" />
        <el-table-column prop="username" label="用户" />
        <el-table-column prop="treeType" label="树种" />
        <el-table-column prop="position" label="种植位置" />
        <el-table-column prop="cycleMonth" label="认养月数" />
        <el-table-column prop="createTime" label="下单时间" />
      </el-table>

      <div class="pager">
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :page-size="query.pageSize"
          :current-page="query.pageNum"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { getOrderList } from '../../api/order'

const loading = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)

const query = reactive({
  pageNum: 1,
  pageSize: 10,
})

async function loadTable() {
  loading.value = true
  try {
    const res: any = await getOrderList({
      pageNum: query.pageNum,
      pageSize: query.pageSize,
    })
    tableData.value = res.data.list || []
    total.value = res.data.total || 0
  } catch {
    tableData.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function handlePageChange(page: number) {
  query.pageNum = page
  loadTable()
}

onMounted(() => {
  loadTable()
})
</script>

<style scoped>
.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
