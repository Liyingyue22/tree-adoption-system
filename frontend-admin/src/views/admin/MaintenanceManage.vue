<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>养护记录管理</span>
          <el-button type="primary" @click="openAddDialog">新增养护记录</el-button>
        </div>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="recordId" label="记录ID" width="100" />
        <el-table-column prop="treeId" label="树木ID" width="100" />
        <el-table-column label="树种">
          <template #default="{ row }">
            {{ row.treeType || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="养护类型">
          <template #default="{ row }">
            {{ row.maintainType || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="说明">
          <template #default="{ row }">
            {{ row.description || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="养护时间">
          <template #default="{ row }">
            {{ row.maintainTime || '—' }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      title="新增养护记录"
      width="520px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="树木ID">
          <el-input v-model="form.treeId" placeholder="请输入树木ID" />
        </el-form-item>

        <el-form-item label="养护类型">
          <el-select v-model="form.maintainType" placeholder="请选择养护类型" style="width: 100%;">
            <el-option label="浇水" value="浇水" />
            <el-option label="施肥" value="施肥" />
            <el-option label="修剪" value="修剪" />
            <el-option label="除草" value="除草" />
            <el-option label="病虫害处理" value="病虫害处理" />
          </el-select>
        </el-form-item>

        <el-form-item label="说明">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入养护说明"
          />
        </el-form-item>

        <el-form-item label="照片地址">
          <el-input v-model="form.photoUrl" placeholder="/cap/demo.svg" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确认新增
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getMaintenanceList, addMaintenance } from '../../api/maintenance'

const loading = ref(false)
const submitLoading = ref(false)
const tableData = ref<any[]>([])

const dialogVisible = ref(false)

const form = reactive<any>({
  treeId: '',
  maintainType: '',
  description: '',
  photoUrl: '/cap/demo.svg',
})

function resetForm() {
  form.treeId = ''
  form.maintainType = ''
  form.description = ''
  form.photoUrl = '/cap/demo.svg'
}

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

function openAddDialog() {
  resetForm()
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.treeId || !form.maintainType) {
    ElMessage.warning('请填写树木ID和养护类型')
    return
  }

  submitLoading.value = true
  try {
    await addMaintenance({
      treeId: Number(form.treeId),
      maintainType: form.maintainType,
      description: form.description,
      photoUrl: form.photoUrl,
    })
    ElMessage.success('新增成功')
    dialogVisible.value = false
    loadTable()
  } catch {
    // 错误提示由拦截器处理
  } finally {
    submitLoading.value = false
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
</style>
