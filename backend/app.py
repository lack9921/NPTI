"""
NPFJ 后端 API — Flask 实现

权重计算由独立的 calculator.py 处理，与路由引擎解耦。

一体运行模式：
  python run.py               # 从项目根目录启动（推荐）
  python backend/app.py       # 纯 API 模式（开发时用，无前端界面）
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine import NPFJEngine
from calculator import WeightCalculator
import os
import uuid

# ============================================================
#  路径配置
# ============================================================
# 自动探测前端 dist 目录：优先项目根 frontend/dist，回退 backend/static
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJ_DIR = os.path.dirname(_BACKEND_DIR)
_DIST_DIR = os.path.join(_PROJ_DIR, "frontend", "dist")
if not os.path.isdir(_DIST_DIR):
    _DIST_DIR = os.path.join(_BACKEND_DIR, "static")
_DIST_EXISTS = os.path.isdir(_DIST_DIR)

app = Flask(__name__)
CORS(app)

engine = NPFJEngine()
calc = WeightCalculator()

# 内存会话存储
_sessions = {}


def _get_session(sid):
    """根据显式传入的 session_id 获取会话"""
    if not sid or sid not in _sessions:
        return None
    return _sessions[sid]


# ============================================================
#  API 端点
# ============================================================

@app.route("/api/health")
def health():
    meta = engine.get_meta()
    return jsonify({
        "status": "ok",
        "total_pools": len(engine.pools),
    })


@app.route("/api/pool/<int:pool_id>")
def get_pool(pool_id):
    """获取指定题池的题目"""
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
    """创建新测试会话"""
    sid = str(uuid.uuid4())[:8]
    _sessions[sid] = engine.create_session()
    pool_info = engine.get_pool_info(1)
    return jsonify({
        "session_id": sid,
        "first_pool": 1,
        "pool_info": pool_info,
    })


@app.route("/api/pool/<int:pool_id>/submit", methods=["POST"])
def submit_pool(pool_id):
    """
    提交一组答案。
    路由由 engine.py 处理，权重由 calculator.py 处理。
    """
    data = request.get_json()
    if not data or "answers" not in data or "session_id" not in data:
        return jsonify({"error": "缺少 session_id 或 answers 字段"}), 400

    sess = _get_session(data["session_id"])
    if sess is None:
        return jsonify({"error": "会话不存在或已过期"}), 400

    answers = data["answers"]
    if len(answers) != 5:
        return jsonify({"error": f"需要 5 个答案，收到 {len(answers)} 个"}), 400

    # 路由判定
    result = engine.submit_pool_answers(sess, pool_id, answers)
    if result is None:
        return jsonify({"error": "提交失败"}), 400

    # 权重累加（独立于路由）
    questions = engine.pools.get(str(pool_id), {}).get("questions", [])
    for i, ans in enumerate(answers):
        if i < len(questions):
            opt = questions[i]["options"].get(ans.upper(), questions[i]["options"].get("A"))
            calc.accumulate(sess["weights"], opt.get("weights", [0, 0, 0, 0, 0]))

    response = {
        "next_pool": result["next_pool"],
        "stage": result["stage"],
        "is_final": result["is_final"],
        "route_result": result["route_result"],
        "color": calc.compute_color(sess["weights"]),
        "gradient": calc.compute_color_gradient(sess["weights"], result["stage"]),
    }

    if result["is_final"]:
        response["result_ready"] = True
    elif result["next_pool"] is not None:
        response["next_pool_info"] = engine.get_pool_info(result["next_pool"])

    return jsonify(response)


@app.route("/api/result", methods=["POST"])
def get_result():
    """
    最终结算。
    人格信息由 engine.py 生成，雷达图和颜色由 calculator.py 生成。
    """
    data = request.get_json()
    if not data or "session_id" not in data:
        return jsonify({"error": "缺少 session_id"}), 400

    sess = _get_session(data["session_id"])
    if sess is None:
        return jsonify({"error": "会话不存在或已过期"}), 400
    if not sess["done"]:
        return jsonify({"error": "测试尚未完成"}), 400

    result = engine.finalize_result(sess)
    if result is None:
        return jsonify({"error": "结果生成失败"}), 500

    # 补充权重计算结果
    wres = calc.compute_all(sess["weights"], stage=3)
    result["radar_data"] = wres["radar"]
    result["color"] = wres["color"]
    result["gradient"] = wres["gradient"]

    return jsonify(result)


# ============================================================
#  前端静态文件服务（一体运行模式）
# ============================================================

# ============================================================
#  前端静态文件服务（一体运行模式）
# ============================================================

@app.route("/")
def serve_index():
    """首页：serve frontend/dist/index.html"""
    if not _DIST_EXISTS:
        return '<h1>⚠️ 前端资源未找到</h1><p>请先构建前端：<br><code>cd frontend &amp;&amp; npm install &amp;&amp; npm run build</code></p><p>或者下载 release 分支的完整包。</p>', 200, {'Content-Type': 'text/html; charset=utf-8'}
    return send_from_directory(_DIST_DIR, "index.html")


@app.route("/<path:path>")
def serve_spa(path):
    """
    SPA 全路由处理：
      1. 如果是 dist 中的静态文件（JS/CSS 等），直接返回
      2. 其余所有非 /api/ 路径 → index.html（SPA fallback）
    """
    if not _DIST_EXISTS:
        return serve_index()
    filepath = os.path.join(_DIST_DIR, path)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return send_from_directory(_DIST_DIR, path)
    return send_from_directory(_DIST_DIR, "index.html")


# ============================================================
#  入口
# ============================================================

if __name__ == "__main__":
    print("🚀 NPFJ 服务启动成功！")
    print(f"  题库加载: {len(engine.pools)} 个题池")
    if _DIST_EXISTS:
        print(f"  前端资源: {_DIST_DIR} (已加载)")
        print(f"  打开浏览器 → http://localhost:8080")
    else:
        print("  ⚠️ 前端资源未找到，仅 API 模式可用")
        print(f"  请执行: cd frontend && npm install && npm run build")
    app.run(host="0.0.0.0", port=8080, debug=True)
