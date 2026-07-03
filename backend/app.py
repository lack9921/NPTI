"""
NPFJ 后端 API — Flask 实现

启动方式：
    cd backend
    pip install flask flask-cors
    python app.py

API 端点：
    GET     /api/pool/<pool_id>       → 获取题池题目
    POST    /api/session/create       → 创建新会话
    POST    /api/pool/<pool_id>/submit → 提交一组答案
    POST    /api/result                → 最终结算

前端 Vite 代理：/api → localhost:8080
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from engine import NPFJEngine
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 用密钥签名 session cookie
app.secret_key = "npfj-secret-key-2026"

# 全局引擎实例
engine = NPFJEngine()

# 内存会话存储（生产环境应该用 Redis/数据库）
# key = session_id, value = session data
_sessions = {}


def _get_or_create_session():
    """获取当前会话 ID，没有则创建"""
    sid = session.get("session_id")
    if not sid or sid not in _sessions:
        sid = str(uuid.uuid4())[:8]
        session["session_id"] = sid
        _sessions[sid] = engine.create_session()
    return sid, _sessions[sid]


# ============================================================
#  API 端点
# ============================================================

@app.route("/api/health")
def health():
    """健康检查"""
    meta = engine.get_meta()
    pool_count = len(engine.pools)
    return jsonify({
        "status": "ok",
        "total_pools": pool_count,
        "dimensions": meta.get("dimensions", []),
        "weight_dims": meta.get("weight_dims", []),
    })


@app.route("/api/pool/<int:pool_id>")
def get_pool(pool_id):
    """
    获取指定题池的题目（前端可见信息，不含权重和路由标签）

    返回：
    {
        "id": 0,
        "stage": 0,
        "name": "基准校准",
        "description": "...",
        "questions": [
            { "id": 1, "text": "...", "options": [
                { "key": "A", "text": "..." },
                { "key": "B", "text": "..." }
            ]}
        ]
    }
    """
    questions = engine.get_pool_questions(pool_id)
    if questions is None:
        return jsonify({"error": "题池不存在"}), 404

    info = engine.get_pool_info(pool_id)
    return jsonify({
        "id": pool_id,
        "stage": info["stage"],
        "name": info["name"],
        "description": info["description"],
        "questions": questions,
    })


@app.route("/api/session/create", methods=["POST"])
def create_session():
    """
    创建新测试会话

    返回：
    {
        "session_id": "abc12345",
        "first_pool": 0,
        "pool_info": { ... }
    }
    """
    sid, sess = _get_or_create_session()
    pool_info = engine.get_pool_info(0)
    return jsonify({
        "session_id": sid,
        "first_pool": 0,
        "pool_info": pool_info,
    })


@app.route("/api/pool/<int:pool_id>/submit", methods=["POST"])
def submit_pool(pool_id):
    """
    提交当前题池的答案，触发路由

    请求体：
    { "answers": ["A", "B", "A", "A", "B"] }

    返回（未完成）：
    {
        "next_pool": 2,
        "stage": 1,
        "is_final": false,
        "route_result": "L",
        "next_pool_info": { ... }
    }

    返回（已完成）：
    {
        "next_pool": null,
        "stage": 4,
        "is_final": true,
        "route_result": "L",
        "result_ready": true
    }
    """
    sid, sess = _get_or_create_session()
    data = request.get_json()

    if not data or "answers" not in data:
        return jsonify({"error": "缺少 answers 字段"}), 400

    answers = data["answers"]
    if len(answers) != 5:
        return jsonify({"error": f"需要 5 个答案，收到 {len(answers)} 个"}), 400

    result = engine.submit_pool_answers(sess, pool_id, answers)
    if result is None:
        return jsonify({"error": "提交失败，题池 ID 或答案格式不正确"}), 400

    response = {
        "next_pool": result["next_pool"],
        "stage": result["stage"],
        "is_final": result["is_final"],
        "route_result": result["route_result"],
    }

    if result["is_final"]:
        response["result_ready"] = True
    elif result["next_pool"] is not None:
        pool_info = engine.get_pool_info(result["next_pool"])
        response["next_pool_info"] = pool_info

    return jsonify(response)


@app.route("/api/result", methods=["POST"])
def get_result():
    """
    最终结算，生成人格类型和五维雷达图数据

    返回：
    {
        "type": "NPFJ",
        "title": "全栈掌控者",
        "description": "...",
        "path_letters": [ ... ],
        "dimensions": [ ... ],
        "radar_data": [ ... ],
    }
    """
    sid, sess = _get_or_create_session()

    if not sess["done"]:
        return jsonify({"error": "测试尚未完成"}), 400

    result = engine.finalize_result(sess)
    if result is None:
        return jsonify({"error": "结果生成失败"}), 500

    return jsonify(result)


# ============================================================
#  启动
# ============================================================

if __name__ == "__main__":
    print("🚀 NPFJ 后端启动成功！")
    print(f"  题库加载: {len(engine.pools)} 个题池")
    app.run(host="0.0.0.0", port=8080, debug=True)
