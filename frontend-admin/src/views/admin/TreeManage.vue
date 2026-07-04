<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>树木管理</span>
          <el-button type="primary" @click="openAddDialog">新增树木</el-button>
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
        <el-table-column label="所属公司">
          <template #default="{ row }">
            {{ row.companyName || '—' }}
          </template>
        </el-table-column>
        <el-table-column prop="cameraSn" label="设备SN" />
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="openEditDialog(row)">编辑</el-button>
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

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑树木' : '新增树木'"
      width="520px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="所属公司">
          <el-select v-model="form.companyId" placeholder="请选择所属公司" style="width: 100%;">
            <el-option
              v-for="item in companyOptions"
              :key="item.companyId"
              :label="item.companyName"
              :value="item.companyId"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="树种">
          <el-input v-model="form.treeType" placeholder="请输入树种" />
        </el-form-item>

        <el-form-item label="位置">
          <el-input v-model="form.position" placeholder="请输入位置" />
        </el-form-item>

        <el-form-item label="价格">
          <el-input v-model="form.price" placeholder="请输入价格" />
        </el-form-item>

        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%;">
            <el-option label="可认养" :value="0" />
            <el-option label="已认养" :value="1" />
          </el-select>
        </el-form-item>

        <el-form-item label="封面图">
          <el-input v-model="form.coverImg" placeholder="/static/tree/demo.svg" />
        </el-form-item>

        <el-form-item label="设备SN">
          <el-input v-model="form.cameraSn" placeholder="请输入设备SN" />
        </el-form-item>

        <el-form-item label="设备IP">
          <el-input v-model="form.cameraIp" placeholder="请输入设备IP" />
        </el-form-item>

        <el-form-item label="设备账号">
          <el-input v-model="form.camUser" placeholder="请输入设备账号" />
        </el-form-item>

        <el-form-item label="设备密码">
          <el-input v-model="form.camPwd" placeholder="请输入设备密码" />
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
import { getTreeList, removeTree, addTree, updateTree } from '../../api/tree'
import { getCompanyList } from '../../api/company'

const loading = ref(false)
const submitLoading = ref(false)
const tableData = ref<any[]>([])
const total = ref(0)
const companyOptions = ref<any[]>([])

const dialogVisible = ref(false)
const isEdit = ref(false)

const query = reactive({
  pageNum: 1,
  pageSize: 10,
})

const form = reactive<any>({
  treeId: undefined,
  companyId: undefined,
  treeType: '',
  position: '',
  price: '',
  status: 0,
  coverImg: '/static/tree/demo.svg',
  cameraSn: '',
  cameraIp: '',
  camUser: 'admin',
  camPwd: '123456',
})

function resetForm() {
  form.treeId = undefined
  form.companyId = undefined
  form.treeType = ''
  form.position = ''
  form.price = ''
  form.status = 0
  form.coverImg = '/static/tree/demo.svg'
  form.cameraSn = ''
  form.cameraIp = ''
  form.camUser = 'admin'
  form.camPwd = '123456'
}

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

async function loadCompanyOptions() {
  try {
    const res: any = await getCompanyList()
    if (Array.isArray(res.data)) {
      companyOptions.value = res.data
    } else if (Array.isArray(res.data?.list)) {
      companyOptions.value = res.data.list
    } else {
      companyOptions.value = []
    }
  } catch {
    companyOptions.value = []
  }
}

function handlePageChange(page: number) {
  query.pageNum = page
  loadTable()
}

function openAddDialog() {
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(row: any) {
  isEdit.value = true
  form.treeId = row.treeId
  form.companyId = row.companyId
  form.treeType = row.treeType || ''
  form.position = row.position || ''
  form.price = row.price || ''
  form.status = row.status ?? 0
  form.coverImg = row.coverImg || '/static/tree/demo.svg'
  form.cameraSn = row.cameraSn || ''
  form.cameraIp = row.cameraIp || ''
  form.camUser = row.camUser || 'admin'
  form.camPwd = row.camPwd || '123456'
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.companyId || !form.treeType || !form.position || !form.price) {
    ElMessage.warning('请填写所属公司、树种、位置和价格')
    return
  }

  submitLoading.value = true
  try {
    const payload = {
      ...form,
      price: Number(form.price),
      status: Number(form.status),
      companyId: Number(form.companyId),
    }

    if (isEdit.value) {
      await updateTree(payload)
      ElMessage.success('修改成功')
    } else {
      await addTree(payload)
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
  loadCompanyOptions()
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
