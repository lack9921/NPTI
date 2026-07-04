"""
NPFJ 后端 API — Flask 实现

权重计算由独立的 calculator.py 处理，与路由引擎解耦。
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from engine import NPFJEngine
from calculator import WeightCalculator
import os

# ============================================================
#  静态文件服务（集成 Vue 前端打包产物）
#  开发时：Vite 代理 /api → 8080
#  生产时：Flask 直接提供 / 页面
# ============================================================

# PyInstaller 打包后 _MEIPASS 指向临时解压目录
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 优先找 frontend/dist，找不到就找 static
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'dist')
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

if os.path.exists(STATIC_DIR):
    from flask import send_from_directory
    @app.route('/')
    def index():
        return send_from_directory(STATIC_DIR, 'index.html')
    @app.route('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory(os.path.join(STATIC_DIR, 'assets'), filename)
    # Vue Router 历史模式：所有非 API 路径返回 index.html
    @app.errorhandler(404)
    def not_found(e):
        if not request.path.startswith('/api'):
            return send_from_directory(STATIC_DIR, 'index.html')
        return e
import sys
import uuid

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


if __name__ == "__main__":
    print("🚀 NPFJ 后端启动成功！")
    print(f"  题库加载: {len(engine.pools)} 个题池")
    app.run(host="0.0.0.0", port=8080, debug=True)
