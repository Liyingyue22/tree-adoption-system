# 后端A → 后端B 接口文档

## 后端A服务信息

- **地址**：`http://47.107.162.223:5000`
- **启动方式**：`cd backend_a && python app.py`
- **抓拍图片访问**：`http://47.107.162.223:5000/static/cap/文件名.jpg`

---

## 接口列表

### 1. 检测摄像头在线状态

```
POST /internal/camera/check
Content-Type: application/json

请求体：
{
    "device_serial": "GU0249887"
}

成功返回：
{
    "code": 0,
    "online": true,
    "msg": "设备在线",
    "device_name": "认养"
}

失败返回：
{
    "code": 1,
    "online": false,
    "msg": "设备离线"
}
```

---

### 2. 获取实时视频流地址

```
POST /internal/camera/rtsp
Content-Type: application/json

请求体：
{
    "device_serial": "GU0249887",
    "channel_no": 1,        // 可选，默认1
    "quality": 1             // 可选，0=流畅 1=高清，默认1
}

成功返回：
{
    "code": 0,
    "msg": "成功（加密设备）",
    "url": "ezopen://xxxxxxxxx@open.ys7.com/GU0249887/1.hd.live",
    "access_token": "at.xxxxxxxx"
}

前端播放方式：
将 url 和 access_token 拼成 iframe 地址：
https://openstatic.ys7.com/ezuikit_share/index.html
  ?accessToken={access_token}
  &url={url（需要URL编码）}
  &themeId=pcLive
```

---

### 3. 抓拍当前画面

```
POST /internal/camera/snapshot
Content-Type: application/json

请求体：
{
    "device_serial": "GU0249887",
    "channel_no": 1          // 可选，默认1
}

成功返回：
{
    "code": 0,
    "msg": "抓拍成功",
    "data": {
        "img_url": "/static/cap/GU0249887_20260630_205426.jpg",
        "img_path": "/home/admin/backend_a/static/cap/GU0249887_20260630_205426.jpg",
        "capture_time": "2026-06-30 20:54:26"
    }
}

注意：img_url 是相对路径，前端访问需要拼接为：
http://47.107.162.223:5000/static/cap/文件名.jpg
```

---

### 4. 批量查询摄像头状态（管理后台用）

```
POST /internal/camera/status
Content-Type: application/json

请求体：
{
    "device_serials": ["GU0249887"]
}

返回：
{
    "code": 0,
    "data": [
        {
            "camera_sn": "GU0249887",
            "online": true,
            "last_check": "2026-06-30 20:48:24",
            "device_name": "认养"
        }
    ]
}
```

---

### 5. 云台控制（转动摄像头）

```
POST /internal/camera/ptz/start

请求体：
{
    "device_serial": "GU0249887",
    "direction": "up",       // up / down / left / right
    "speed": 5               // 可选，1-10，默认5
}

POST /internal/camera/ptz/stop

请求体：
{
    "device_serial": "GU0249887"
}

返回：
{"code": 0, "msg": "控制成功"}
```

---

### 6. 健康检查

```
GET /health

返回：
{"code": 0, "msg": "后端A运行中", "time": "2026-06-30 20:48:24"}
```

---

## 统一返回格式

```json
{
    "code": 0,       // 0=成功，非0=失败
    "msg": "提示信息",
    "data": {}       // 具体数据（部分接口无此字段）
}
```

## 错误码

| code | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 设备离线 |
| 2 | 网络异常 |
| 99 | 其他错误（看msg字段） |

---

## 当前设备信息

| 项目 | 值 |
|------|-----|
| 设备序列号 | GU0249887 |
| 设备名称 | 认养 |
| 验证码 | Ss20060626 |
| 接入方式 | 萤石云开放平台 |
