<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>公司管理</span>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="companyId" label="公司ID" width="100" />
        <el-table-column prop="companyName" label="公司名称" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="contactPhone" label="联系电话" />
        <el-table-column prop="description" label="简介" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getCompanyList } from '../../api/company'

const loading = ref(false)
const tableData = ref<any[]>([])

async function loadTable() {
  loading.value = true
  try {
    const res: any = await getCompanyList()
    console.log('公司列表返回：', res)

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
