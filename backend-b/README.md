# 农业树木认养系统 - 后端 B

Python + Flask + SQLite 轻量版，提供全部 REST API 给前端 A/B 联调。

## 目录结构

```
backend-b/
├── app.py              # 主程序（启动这个）
├── requirements.txt    # Python 依赖
├── API测试.http        # 接口测试文件（VS Code REST Client）
├── 后端B任务指南.md     # 详细说明
├── data/               # SQLite 数据库（自动创建）
├── static/             # 占位图片
├── sql/                # SQL Server 建表脚本（DBA 用，Python 版不需要手动执行）
└── docs/               # 接口文档、后端 A 对接文档
```

## 快速启动

```bash
cd d:\hym\backend-b
pip install -r requirements.txt
python app.py
```

接口地址：`http://localhost:8080/api`

## 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 普通用户 | test01 | 123456 |
| 管理员 | admin01 | 123456 |

## 摄像头模式

- 默认 mock 演示模式，不接硬件也能跑
- 真实模式：`$env:HARDWARE_MOCK="false"; python app.py`

## 文档

- 对外 API 规范：`docs/农业树木认养系统.docx`
- 后端 A 对接：`docs/后端A接口文档.md`
- 后端 A 测试页：`docs/接口测试页面.html`（浏览器打开）
- **后端 B 测试页：`docs/后端B接口测试页面.html`（浏览器打开，模拟前端联调）**

## 给前端联调

基础地址 `http://localhost:8080/api`，登录后请求头带 `token`，详见 `后端B任务指南.md`。
