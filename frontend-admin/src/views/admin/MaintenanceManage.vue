<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>养护记录管理</span>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="recordId" label="记录ID" width="100" />
        <el-table-column prop="treeId" label="树木ID" width="100" />
        <el-table-column prop="treeType" label="树种" />
        <el-table-column prop="maintainType" label="养护类型" />
        <el-table-column prop="description" label="说明" />
        <el-table-column prop="maintainTime" label="养护时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getMaintenanceList } from '../../api/maintenance'

const loading = ref(false)
const tableData = ref<any[]>([])

async function loadTable() {
  loading.value = true
  try {
    const res: any = await getMaintenanceList()
    console.log('养护记录返回：', res)

    if (Array.isArray(res.data)) {
      tableData.value = res.data
    } else if (Array.isArray(res.data?.list)) {
      tableData.value = res.data.list
    } else {
      tableData.value = []
    }
  } catch {
    tableData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTable()
})
</script>
