<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>公司管理</span>
          <el-button type="primary" @click="openAddDialog">新增公司</el-button>
        </div>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="companyId" label="公司ID" width="100" />
        <el-table-column label="公司名称">
          <template #default="{ row }">
            {{ row.companyName || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="地址">
          <template #default="{ row }">
            {{ row.address || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="联系电话">
          <template #default="{ row }">
            {{ row.contactPhone || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="简介">
          <template #default="{ row }">
            {{ row.description || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.companyId)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑公司' : '新增公司'"
      width="520px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="公司名称">
          <el-input v-model="form.companyName" placeholder="请输入公司名称" />
        </el-form-item>

        <el-form-item label="地址">
          <el-input v-model="form.address" placeholder="请输入地址" />
        </el-form-item>

        <el-form-item label="联系电话">
          <el-input v-model="form.contactPhone" placeholder="请输入联系电话" />
        </el-form-item>

        <el-form-item label="简介">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入公司简介"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '确认新增' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCompanyList, addCompany, updateCompany, removeCompany } from '../../api/company'

const loading = ref(false)
const submitLoading = ref(false)
const tableData = ref<any[]>([])

const dialogVisible = ref(false)
const isEdit = ref(false)

const form = reactive<any>({
  companyId: undefined,
  companyName: '',
  address: '',
  contactPhone: '',
  description: '',
})

function resetForm() {
  form.companyId = undefined
  form.companyName = ''
  form.address = ''
  form.contactPhone = ''
  form.description = ''
}

async function loadTable() {
  loading.value = true
  try {
    const res: any = await getCompanyList()
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
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: any) {
  isEdit.value = true
  form.companyId = row.companyId
  form.companyName = row.companyName || ''
  form.address = row.address || ''
  form.contactPhone = row.contactPhone || ''
  form.description = row.description || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.companyName) {
    ElMessage.warning('请填写公司名称')
    return
  }

  submitLoading.value = true
  try {
    const payload = { ...form }

    if (isEdit.value) {
      await updateCompany(payload)
      ElMessage.success('修改成功')
    } else {
      await addCompany(payload)
      ElMessage.success('新增成功')
    }

    dialogVisible.value = false
    loadTable()
  } catch {
    // 错误提示由拦截器处理
  } finally {
    submitLoading.value = false
  }
}

async function handleDelete(companyId: number) {
  try {
    await ElMessageBox.confirm('确认删除这家公司吗？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
  } catch {
    return
  }

  try {
    await removeCompany(companyId)
    ElMessage.success('删除成功')
    loadTable()
  } catch {
    // 错误提示由拦截器处理
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
