<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>树木管理</span>
          <el-button type="primary">新增树木</el-button>
        </div>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="treeId" label="树木ID" width="100" />
        <el-table-column prop="treeType" label="树种" />
        <el-table-column prop="position" label="位置" />
        <el-table-column prop="price" label="价格" />
        <el-table-column label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'danger' : 'success'">
              {{ row.status === 1 ? '已认养' : '可认养' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="companyName" label="所属公司" />
        <el-table-column prop="cameraSn" label="设备SN" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" type="primary">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.treeId)">
              删除
            </el-button>
          </template>
        </el-table-column>
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTreeList, removeTree } from '../../api/tree'

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
    const res: any = await getTreeList({
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

async function handleDelete(treeId: number) {
  try {
    await ElMessageBox.confirm('确认删除这棵树吗？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
  } catch {
    return
  }

  try {
    await removeTree(treeId)
    ElMessage.success('删除成功')
    loadTable()
  } catch {
    // 错误提示已经在 request.ts 里处理
  }
}

onMounted(() => {
  loadTable()
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
