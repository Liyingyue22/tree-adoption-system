<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>摄像头状态</span>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="treeId" label="树木ID" width="100" />
        <el-table-column prop="treeType" label="树种" />
        <el-table-column prop="cameraSn" label="设备SN" />
        <el-table-column label="在线状态">
          <template #default="{ row }">
            <el-tag :type="row.online ? 'success' : 'danger'">
              {{ row.online ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="最后检测时间">
  <template #default="{ row }">
    {{ row.lastCheck || '—' }}
  </template>
</el-table-column>

        <el-table-column label="设备名称">
  <template #default="{ row }">
    {{ row.deviceName || '—' }}
  </template>
</el-table-column>

      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getCameraStatusList } from '../../api/camera'

const loading = ref(false)
const tableData = ref<any[]>([])

async function loadTable() {
  loading.value = true
  try {
    const res: any = await getCameraStatusList()
    console.log('摄像头状态接口返回：', res)

    if (Array.isArray(res.data)) {
      tableData.value = res.data
    } else if (Array.isArray(res.data?.list)) {
      tableData.value = res.data.list
    } else {
      tableData.value = []
      console.log('摄像头状态数据不是数组：', res.data)
    }
  } catch (error) {
    console.log('摄像头状态报错：', error)
    tableData.value = []
  } finally {
    loading.value = false
  }
  console.log('第一条摄像头数据：', res.data?.[0])

}


onMounted(() => {
  loadTable()
})
</script>
