"""
NPFJ 后端 API — Flask 实现

权重计算由独立的 calculator.py 处理，与路由引擎解耦。
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from engine import NPFJEngine
from calculator import WeightCalculator
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "npfj-secret-key-2026"

engine = NPFJEngine()
calc = WeightCalculator()

# 内存会话存储
_sessions = {}


def _get_or_create_session():
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
    meta = engine.get_meta()
    return jsonify({
        "status": "ok",
        "total_pools": len(engine.pools),
        "dimensions": meta.get("dimensions", []),
        "weight_dims": meta.get("weight_dims", []),
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
    sid, sess = _get_or_create_session()
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
    sid, sess = _get_or_create_session()
    data = request.get_json()

    if not data or "answers" not in data:
        return jsonify({"error": "缺少 answers 字段"}), 400

    answers = data["answers"]
    if len(answers) != 5:
        return jsonify({"error": f"需要 5 个答案，收到 {len(answers)} 个"}), 400

    # 交给引擎做路由判定
    result = engine.submit_pool_answers(sess, pool_id, answers)
    if result is None:
        return jsonify({"error": "提交失败"}), 400

    # 提交完成后，用 calculator 处理所有选项的权重
    # （engine.py 不碰权重，权重全部由 calculator.py 管理）
    questions = engine.pools.get(str(pool_id), {}).get("questions", [])
    for i, ans in enumerate(answers):
        if i < len(questions):
            opt = questions[i]["options"].get(ans.upper(), questions[i]["options"].get("A"))
            w = opt.get("weights", [0, 0, 0, 0, 0])
            calc.accumulate(sess["weights"], w)

    response = {
        "next_pool": result["next_pool"],
        "stage": result["stage"],
        "is_final": result["is_final"],
        "route_result": result["route_result"],
        # 每次提交后返回当前权重计算的颜色
        "color": calc.compute_color(sess["weights"]),
        "gradient": calc.compute_color_gradient(sess["weights"], result["stage"]),
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
    最终结算。
    人格信息由 engine.py 生成，雷达图和颜色由 calculator.py 生成。
    """
    sid, sess = _get_or_create_session()
    if not sess["done"]:
        return jsonify({"error": "测试尚未完成"}), 400

    result = engine.finalize_result(sess)
    if result is None:
        return jsonify({"error": "结果生成失败"}), 500

    # 用 calculator 补充权重计算结果
    weight_result = calc.compute_all(sess["weights"], stage=3)

    result["radar_data"] = weight_result["radar"]
    result["color"] = weight_result["color"]
    result["gradient"] = weight_result["gradient"]

    return jsonify(result)


# ============================================================
#  启动
# ============================================================

if __name__ == "__main__":
    print("🚀 NPFJ 后端启动成功！")
    print(f"  题库加载: {len(engine.pools)} 个题池")
    print(f"  权重引擎: calculator.py（独立于路由）")
    app.run(host="0.0.0.0", port=8080, debug=True)
