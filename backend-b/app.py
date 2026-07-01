# -*- coding: utf-8 -*-
"""
农业树木认养系统 - 后端 B 轻量版
Python + Flask + SQLite，无需 JDK / Maven / SQL Server

启动：
  pip install -r requirements.txt
  python app.py
"""
import base64
import hashlib
import hmac
import json
import os
import sqlite3
import time
from datetime import datetime
from functools import wraps
from urllib.parse import quote

import requests
from flask import Flask, g, jsonify, request

# ---------- 配置 ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "tree_adoption.db")
TOKEN_SECRET = "TreeAdoptionBackendSecretChangeMe"
TOKEN_EXPIRE_HOURS = 24
HARDWARE_BASE_URL = os.getenv("HARDWARE_BASE_URL", "http://47.107.162.223:5000")
# 默认 mock：不依赖后端 A 也能跑通；要接真实摄像头设 HARDWARE_MOCK=false
HARDWARE_MOCK = os.getenv("HARDWARE_MOCK", "true").lower() == "true"

app = Flask(__name__, static_folder="static", static_url_path="")


# ---------- 工具 ----------
def ok(data=None, msg="成功"):
    return jsonify({"code": 0, "msg": msg, "data": data})


def fail(code, msg):
    return jsonify({"code": code, "msg": msg, "data": None})


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def rows_to_list(rows):
    return [dict(r) for r in rows]


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn:
        conn.close()


def create_token(user_id, role):
    expire_at = int(time.time()) + TOKEN_EXPIRE_HOURS * 3600
    payload = f"{user_id}|{role}|{expire_at}"
    payload_b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    sig = hmac.new(TOKEN_SECRET.encode(), payload_b64.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return f"{payload_b64}.{sig_b64}"


def parse_token(token):
    if not token or "." not in token:
        raise ValueError("empty")
    payload_b64, sig_b64 = token.split(".", 1)
    expected = base64.urlsafe_b64encode(
        hmac.new(TOKEN_SECRET.encode(), payload_b64.encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    actual = sig_b64.rstrip("=")
    if not hmac.compare_digest(expected, actual):
        raise ValueError("bad sig")
    payload_pad = payload_b64 + "=" * (-len(payload_b64) % 4)
    payload = base64.urlsafe_b64decode(payload_pad).decode()
    user_id, role, expire_at = payload.split("|")
    if int(time.time()) > int(expire_at):
        raise ValueError("expired")
    return int(user_id), role


def get_token_from_request():
    token = request.headers.get("token") or request.headers.get("Token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    return token


def login_required(admin=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == "OPTIONS":
                return "", 204
            token = get_token_from_request()
            try:
                user_id, role = parse_token(token)
            except Exception:
                return fail(1003, "未登录或 Token 失效"), 401
            if admin and role != "admin":
                return fail(1004, "无管理员权限"), 403
            g.user_id = user_id
            g.role = role
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def public_route(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.method == "OPTIONS":
            return "", 204
        token = get_token_from_request()
        if token:
            try:
                g.user_id, g.role = parse_token(token)
            except Exception:
                return fail(1003, "未登录或 Token 失效"), 401
        return fn(*args, **kwargs)
    return wrapper


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,token,Authorization"
    return resp


# ---------- 数据库初始化 ----------
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS company (
        companyId INTEGER PRIMARY KEY AUTOINCREMENT,
        companyName TEXT NOT NULL,
        address TEXT,
        contactPhone TEXT,
        description TEXT
    );
    CREATE TABLE IF NOT EXISTS user (
        userId INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        phone TEXT,
        role TEXT DEFAULT 'user'
    );
    CREATE TABLE IF NOT EXISTS tree (
        treeId INTEGER PRIMARY KEY AUTOINCREMENT,
        companyId INTEGER,
        treeType TEXT NOT NULL,
        position TEXT,
        price REAL,
        status INTEGER DEFAULT 0,
        coverImg TEXT,
        cameraSn TEXT,
        cameraIp TEXT,
        camUser TEXT,
        camPwd TEXT,
        FOREIGN KEY (companyId) REFERENCES company(companyId)
    );
    CREATE TABLE IF NOT EXISTS tree_order (
        orderId INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER NOT NULL,
        treeId INTEGER NOT NULL,
        cycleMonth INTEGER,
        createTime TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (userId) REFERENCES user(userId),
        FOREIGN KEY (treeId) REFERENCES tree(treeId)
    );
    CREATE TABLE IF NOT EXISTS maintenance_record (
        recordId INTEGER PRIMARY KEY AUTOINCREMENT,
        treeId INTEGER NOT NULL,
        workerId INTEGER NOT NULL,
        maintainType TEXT,
        description TEXT,
        photoUrl TEXT,
        maintainTime TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (treeId) REFERENCES tree(treeId),
        FOREIGN KEY (workerId) REFERENCES user(userId)
    );
    """)
    count = cur.execute("SELECT COUNT(1) FROM user").fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO company(companyName,address,contactPhone,description) VALUES(?,?,?,?)",
            [
                ("阳光生态农场", "一号农田 A 区", "0571-88886666", "提供果树与景观树认养服务"),
                ("青禾农业公司", "二号农田 B 区", "0571-66668888", "负责农田养护和摄像头监控"),
                ("绿源果园基地", "三号果园 C 区", "0571-99990000", "提供果树长期认养服务"),
            ],
        )
        cur.executemany(
            "INSERT INTO user(username,password,phone,role) VALUES(?,?,?,?)",
            [
                ("admin01", "123456", "13900000001", "admin"),
                ("test01", "123456", "13800138001", "user"),
                ("test02", "123456", "13800138002", "user"),
            ],
        )
        trees = [
            (1, "香樟树", "一号农田 A 区 001", 200, 1, "/static/tree/demo.svg", "GU0249887", "192.168.1.101", "admin", "123456"),
            (1, "桂花树", "一号农田 A 区 002", 180, 0, "/static/tree/demo.svg", "CAM-A002", "192.168.1.102", "admin", "123456"),
            (1, "银杏树", "一号农田 A 区 003", 260, 0, "/static/tree/demo.svg", "CAM-A003", "192.168.1.103", "admin", "123456"),
            (2, "桃树", "二号农田 B 区 001", 300, 1, "/static/tree/demo.svg", "CAM-B001", "192.168.1.111", "admin", "123456"),
            (2, "梨树", "二号农田 B 区 002", 280, 0, "/static/tree/demo.svg", "CAM-B002", "192.168.1.112", "admin", "123456"),
            (3, "苹果树", "三号果园 C 区 001", 320, 0, "/static/tree/demo.svg", "CAM-C001", "192.168.1.121", "admin", "123456"),
            (3, "柿子树", "三号果园 C 区 002", 220, 0, "/static/tree/demo.svg", "CAM-C002", "192.168.1.122", "admin", "123456"),
        ]
        cur.executemany(
            "INSERT INTO tree(companyId,treeType,position,price,status,coverImg,cameraSn,cameraIp,camUser,camPwd) VALUES(?,?,?,?,?,?,?,?,?,?)",
            trees,
        )
        cur.executemany(
            "INSERT INTO tree_order(userId,treeId,cycleMonth) VALUES(?,?,?)",
            [(2, 1, 12), (3, 4, 6)],
        )
        cur.executemany(
            "INSERT INTO maintenance_record(treeId,workerId,maintainType,description,photoUrl) VALUES(?,?,?,?,?)",
            [
                (1, 1, "浇水", "完成本周浇水，树木状态良好", "/static/cap/demo.svg"),
                (1, 1, "施肥", "完成有机肥补充", "/static/cap/demo.svg"),
                (4, 1, "修剪", "修剪枯枝，保持树形", "/static/cap/demo.svg"),
            ],
        )
    db.commit()
    db.close()


def tree_select_sql(where=""):
    return f"""
        SELECT t.treeId, t.companyId, c.companyName, t.treeType, t.position, t.price, t.status,
               t.coverImg, t.cameraSn, t.cameraIp, t.camUser, t.camPwd
        FROM tree t LEFT JOIN company c ON t.companyId = c.companyId
        {where}
    """


# ---------- 硬件摄像头（转发后端 A 或 mock） ----------
def hw_post(path, body):
    try:
        r = requests.post(f"{HARDWARE_BASE_URL}{path}", json=body, timeout=10)
        return r.json()
    except Exception as e:
        raise RuntimeError(f"无法连接后端A: {e}")


def camera_online(camera_sn):
    if HARDWARE_MOCK:
        return bool(camera_sn)
    resp = hw_post("/internal/camera/check", {"device_serial": camera_sn})
    return resp.get("code") == 0 and resp.get("online") is True


def camera_snapshot(camera_sn):
    if HARDWARE_MOCK:
        return f"http://127.0.0.1:8080/static/cap/demo.svg", now_str()
    resp = hw_post("/internal/camera/snapshot", {"device_serial": camera_sn, "channel_no": 1})
    if resp.get("code") != 0:
        raise RuntimeError(resp.get("msg", "抓拍失败"))
    data = resp.get("data") or {}
    img = data.get("img_url", "")
    if img.startswith("/"):
        img = HARDWARE_BASE_URL + img
    return img, data.get("capture_time") or now_str()


def camera_rtsp(camera_sn):
    if HARDWARE_MOCK:
        return "rtsp://demo/stream", None, None
    resp = hw_post("/internal/camera/rtsp", {"device_serial": camera_sn, "channel_no": 1, "quality": 1})
    if resp.get("code") != 0:
        raise RuntimeError(resp.get("msg", "获取视频流失败"))
    url = resp.get("url")
    token = resp.get("access_token")
    play = None
    if url and token:
        play = (
            "https://openstatic.ys7.com/ezuikit_share/index.html"
            f"?accessToken={quote(token)}&url={quote(url)}&themeId=pcLive"
        )
    return url, token, play


def camera_batch_status(serials):
    if not serials:
        return {}
    if HARDWARE_MOCK:
        return {s: {"online": True, "last_check": now_str(), "device_name": "演示设备"} for s in serials}
    resp = hw_post("/internal/camera/status", {"device_serials": serials})
    if resp.get("code") != 0:
        return {}
    result = {}
    for item in resp.get("data") or []:
        result[item.get("camera_sn")] = item
    return result


def get_tree_or_404(tree_id):
    db = get_db()
    row = db.execute(tree_select_sql("WHERE t.treeId = ?"), (tree_id,)).fetchone()
    if not row:
        return None
    return row_to_dict(row)


# ---------- 用户接口 ----------
@app.post("/api/user/register")
def user_register():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    phone = body.get("phone", "")
    if not username or not password:
        return fail(4001, "用户名和密码不能为空")
    db = get_db()
    if db.execute("SELECT 1 FROM user WHERE username=?", (username,)).fetchone():
        return fail(4001, "用户名已存在")
    cur = db.execute(
        "INSERT INTO user(username,password,phone,role) VALUES(?,?,?,?)",
        (username, password, phone, "user"),
    )
    db.commit()
    return ok({"userId": cur.lastrowid, "username": username, "role": "user"}, "注册成功")


@app.post("/api/user/login")
def user_login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    db = get_db()
    row = db.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()
    if not row:
        return fail(1001, "账号不存在")
    if row["password"] != password:
        return fail(1002, "密码错误")
    data = {
        "token": create_token(row["userId"], row["role"]),
        "userId": row["userId"],
        "username": row["username"],
        "role": row["role"],
    }
    return ok(data, "登录成功")


@app.get("/api/user/info")
@login_required()
def user_info():
    db = get_db()
    row = db.execute("SELECT userId,username,phone,role FROM user WHERE userId=?", (g.user_id,)).fetchone()
    if not row:
        return fail(1001, "账号不存在")
    return ok(dict(row))


# ---------- 树木接口 ----------
@app.get("/api/tree/list")
@login_required()
def tree_list():
    page_num = max(int(request.args.get("pageNum", 1)), 1)
    page_size = min(max(int(request.args.get("pageSize", 10)), 1), 100)
    offset = (page_num - 1) * page_size
    db = get_db()
    total = db.execute("SELECT COUNT(1) FROM tree").fetchone()[0]
    rows = db.execute(
        tree_select_sql("ORDER BY t.treeId DESC LIMIT ? OFFSET ?"),
        (page_size, offset),
    ).fetchall()
    return ok({"pageNum": page_num, "pageSize": page_size, "total": total, "list": rows_to_list(rows)})


@app.get("/api/tree/detail")
@login_required()
def tree_detail():
    tree_id = request.args.get("treeId", type=int)
    if not tree_id:
        return fail(4001, "treeId 不能为空")
    tree = get_tree_or_404(tree_id)
    if not tree:
        return fail(4001, "树木不存在")
    return ok(tree)


@app.post("/api/tree/add")
@login_required(admin=True)
def tree_add():
    body = request.get_json(silent=True) or {}
    db = get_db()
    cur = db.execute(
        """INSERT INTO tree(companyId,treeType,position,price,status,coverImg,cameraSn,cameraIp,camUser,camPwd)
           VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (
            body.get("companyId"), body.get("treeType"), body.get("position"), body.get("price"),
            body.get("status", 0), body.get("coverImg"), body.get("cameraSn"),
            body.get("cameraIp"), body.get("camUser"), body.get("camPwd"),
        ),
    )
    db.commit()
    return ok({"treeId": cur.lastrowid}, "新增成功")


@app.put("/api/tree/update")
@login_required(admin=True)
def tree_update():
    body = request.get_json(silent=True) or {}
    tree_id = body.get("treeId")
    if not tree_id:
        return fail(4001, "treeId 不能为空")
    db = get_db()
    db.execute(
        """UPDATE tree SET companyId=?,treeType=?,position=?,price=?,status=?,coverImg=?,
           cameraSn=?,cameraIp=?,camUser=?,camPwd=? WHERE treeId=?""",
        (
            body.get("companyId"), body.get("treeType"), body.get("position"), body.get("price"),
            body.get("status", 0), body.get("coverImg"), body.get("cameraSn"),
            body.get("cameraIp"), body.get("camUser"), body.get("camPwd"), tree_id,
        ),
    )
    db.commit()
    return ok({"treeId": tree_id}, "修改成功")


@app.delete("/api/tree/remove")
@login_required(admin=True)
def tree_remove():
    tree_id = request.args.get("treeId", type=int)
    if not tree_id:
        return fail(4001, "treeId 不能为空")
    db = get_db()
    db.execute("DELETE FROM tree WHERE treeId=?", (tree_id,))
    db.commit()
    return ok({"treeId": tree_id}, "删除成功")


# ---------- 订单接口 ----------
@app.post("/api/order/create")
@login_required()
def order_create():
    body = request.get_json(silent=True) or {}
    tree_id = body.get("treeId")
    cycle_month = body.get("cycleMonth")
    if not tree_id:
        return fail(4001, "treeId 不能为空")
    db = get_db()
    try:
        db.execute("BEGIN IMMEDIATE")
        tree = db.execute("SELECT * FROM tree WHERE treeId=?", (tree_id,)).fetchone()
        if not tree:
            db.execute("ROLLBACK")
            return fail(4001, "树木不存在")
        if tree["status"] == 1:
            db.execute("ROLLBACK")
            return fail(2001, "树木已被认养")
        cur = db.execute(
            "INSERT INTO tree_order(userId,treeId,cycleMonth) VALUES(?,?,?)",
            (g.user_id, tree_id, cycle_month),
        )
        db.execute("UPDATE tree SET status=1 WHERE treeId=?", (tree_id,))
        db.commit()
        return ok(
            {"orderId": cur.lastrowid, "userId": g.user_id, "treeId": tree_id, "cycleMonth": cycle_month},
            "认养成功",
        )
    except Exception:
        db.execute("ROLLBACK")
        raise


@app.get("/api/order/myTree")
@login_required()
def order_my_tree():
    db = get_db()
    rows = db.execute(
        """SELECT o.orderId,o.userId,u.username,o.treeId,t.treeType,t.position,o.cycleMonth,o.createTime
           FROM tree_order o
           JOIN user u ON o.userId=u.userId
           JOIN tree t ON o.treeId=t.treeId
           WHERE o.userId=? ORDER BY o.createTime DESC""",
        (g.user_id,),
    ).fetchall()
    return ok({"list": rows_to_list(rows)})


@app.get("/api/order/all")
@login_required(admin=True)
def order_all():
    page_num = max(int(request.args.get("pageNum", 1)), 1)
    page_size = min(max(int(request.args.get("pageSize", 10)), 1), 100)
    offset = (page_num - 1) * page_size
    db = get_db()
    total = db.execute("SELECT COUNT(1) FROM tree_order").fetchone()[0]
    rows = db.execute(
        """SELECT o.orderId,o.userId,u.username,o.treeId,t.treeType,t.position,o.cycleMonth,o.createTime
           FROM tree_order o
           JOIN user u ON o.userId=u.userId
           JOIN tree t ON o.treeId=t.treeId
           ORDER BY o.createTime DESC LIMIT ? OFFSET ?""",
        (page_size, offset),
    ).fetchall()
    return ok({"pageNum": page_num, "pageSize": page_size, "total": total, "list": rows_to_list(rows)})


def do_snapshot(tree_id):
    tree = get_tree_or_404(tree_id)
    if not tree:
        return fail(4001, "树木不存在")
    if not tree.get("cameraSn"):
        return fail(4001, "该树木未绑定摄像头")
    if not camera_online(tree["cameraSn"]):
        return fail(3001, "摄像头离线")
    try:
        img_url, capture_time = camera_snapshot(tree["cameraSn"])
    except RuntimeError as e:
        return fail(3001, str(e))
    return ok({"imgUrl": img_url, "captureTime": capture_time})


# ---------- 摄像头接口 ----------
@app.get("/api/camera/snapshot")
@login_required()
def camera_snap():
    tree_id = request.args.get("treeId", type=int)
    return do_snapshot(tree_id)


@app.get("/api/camera/rtsp")
@login_required()
def camera_rtsp_api():
    tree_id = request.args.get("treeId", type=int)
    tree = get_tree_or_404(tree_id)
    if not tree:
        return fail(4001, "树木不存在")
    if not tree.get("cameraSn"):
        return fail(4001, "该树木未绑定摄像头")
    if not camera_online(tree["cameraSn"]):
        return fail(3001, "摄像头离线")
    try:
        url, access_token, play_url = camera_rtsp(tree["cameraSn"])
    except RuntimeError as e:
        return fail(3001, str(e))
    return ok({"rtspUrl": url, "url": url, "accessToken": access_token, "playUrl": play_url})


@app.get("/api/camera/status/list")
@login_required(admin=True)
def camera_status_list():
    db = get_db()
    trees = rows_to_list(db.execute(tree_select_sql("ORDER BY t.treeId DESC")).fetchall())
    serials = list({t["cameraSn"] for t in trees if t.get("cameraSn")})
    status_map = camera_batch_status(serials)
    result = []
    for t in trees:
        item = {
            "treeId": t["treeId"],
            "treeType": t["treeType"],
            "position": t["position"],
            "cameraSn": t["cameraSn"],
            "cameraIp": t["cameraIp"],
        }
        st = status_map.get(t.get("cameraSn"))
        if st:
            item["online"] = st.get("online", False)
            item["deviceName"] = st.get("device_name")
            item["checkTime"] = st.get("last_check") or now_str()
        else:
            item["online"] = False
            item["checkTime"] = now_str()
        result.append(item)
    return ok({"list": result})


@app.post("/api/camera/manualCap")
@login_required(admin=True)
def camera_manual_cap():
    body = request.get_json(silent=True) or {}
    tree_id = body.get("treeId")
    resp = do_snapshot(tree_id)
    data = resp.get_json()
    if data["code"] != 0:
        return jsonify(data)
    return ok(data["data"], "抓拍成功")


# ---------- 公司 / 养护（ER 图补充） ----------
@app.get("/api/company/list")
@login_required(admin=True)
def company_list():
    db = get_db()
    rows = db.execute("SELECT * FROM company ORDER BY companyId DESC").fetchall()
    return ok({"list": rows_to_list(rows)})


@app.post("/api/company/add")
@login_required(admin=True)
def company_add():
    body = request.get_json(silent=True) or {}
    db = get_db()
    cur = db.execute(
        "INSERT INTO company(companyName,address,contactPhone,description) VALUES(?,?,?,?)",
        (body.get("companyName"), body.get("address"), body.get("contactPhone"), body.get("description")),
    )
    db.commit()
    return ok({"companyId": cur.lastrowid}, "新增成功")


@app.put("/api/company/update")
@login_required(admin=True)
def company_update():
    body = request.get_json(silent=True) or {}
    cid = body.get("companyId")
    if not cid:
        return fail(4001, "companyId 不能为空")
    db = get_db()
    db.execute(
        "UPDATE company SET companyName=?,address=?,contactPhone=?,description=? WHERE companyId=?",
        (body.get("companyName"), body.get("address"), body.get("contactPhone"), body.get("description"), cid),
    )
    db.commit()
    return ok({"companyId": cid}, "修改成功")


@app.delete("/api/company/remove")
@login_required(admin=True)
def company_remove():
    cid = request.args.get("companyId", type=int)
    db = get_db()
    db.execute("DELETE FROM company WHERE companyId=?", (cid,))
    db.commit()
    return ok({"companyId": cid}, "删除成功")


@app.get("/api/maintenance/list")
@login_required()
def maintenance_list():
    tree_id = request.args.get("treeId", type=int)
    db = get_db()
    if tree_id:
        rows = db.execute(
            "SELECT * FROM maintenance_record WHERE treeId=? ORDER BY maintainTime DESC", (tree_id,)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM maintenance_record ORDER BY maintainTime DESC").fetchall()
    return ok({"list": rows_to_list(rows)})


@app.post("/api/maintenance/add")
@login_required(admin=True)
def maintenance_add():
    body = request.get_json(silent=True) or {}
    db = get_db()
    cur = db.execute(
        """INSERT INTO maintenance_record(treeId,workerId,maintainType,description,photoUrl)
           VALUES(?,?,?,?,?)""",
        (body.get("treeId"), g.user_id, body.get("maintainType"), body.get("description"), body.get("photoUrl")),
    )
    db.commit()
    return ok({"recordId": cur.lastrowid}, "新增成功")


@app.get("/health")
def health():
    return ok({"msg": "后端B轻量版运行中", "time": now_str(), "mock": HARDWARE_MOCK})


# ---------- 静态资源占位 ----------
@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE_DIR, "static", "tree"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "static", "cap"), exist_ok=True)
    # 复制 demo 占位图（若 Java 版 static 存在）
    for sub in ("tree", "cap"):
        src = os.path.join(BASE_DIR, "src", "main", "resources", "static", sub, "demo.svg")
        dst = os.path.join(BASE_DIR, "static", sub, "demo.svg")
        if os.path.exists(src) and not os.path.exists(dst):
            import shutil
            shutil.copy(src, dst)
    init_db()
    print("=" * 50)
    print("后端 B 轻量版已启动  http://localhost:8080/api")
    print("测试账号: test01/123456  管理员: admin01/123456")
    print(f"摄像头模式: {'演示(mock)' if HARDWARE_MOCK else '真实(后端A)'}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8080, debug=False)
