"""
NPFJ 引擎：二分树状态机路由 + 五维隐性权重累加器

架构：
========================================
用户会话状态 (session)：
{
    "path": [],               ← 路由路径，如 ["L", "R", "L"]
    "pool_history": [0, 2],   ← 走过的题池 ID
    "current_pool": 3,        ← 当前题池 ID
    "weights": [0,0,0,0,0],   ← 五维权重累加
    "stage_answers": {}       ← 当前题池的答案缓存
}
========================================

路由规则：
- 每个题池 5 题
- 每题两个选项（A/B），各有 route_label（L/R）和 weights[5]
- 5 题答完后：
  ① 统计 L/R 出现次数，多数决确定走向
  ② 累加 5 题的 weights 到 session.weights
  ③ 根据 route_map 路由到下一题池
- Stage 4 完成后，根据路径组合出 4 位字母人格
"""

import json
import os
from typing import Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_REPORTS_PATH = os.path.join(ROOT, "reports.json")

POOLS_PATH = os.path.join(ROOT, "pools.json")

ANALYSIS_REPORTS = None
def _load_reports():
    global ANALYSIS_REPORTS
    if ANALYSIS_REPORTS is not None:
        return ANALYSIS_REPORTS
    path = os.path.join(ROOT, "reports.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            ANALYSIS_REPORTS = json.load(f)
    else:
        ANALYSIS_REPORTS = {}
    return ANALYSIS_REPORTS

PERSONALITY_MAP = {
    "I_P_A_D": ("IPAD", "逻辑爆破者",
        "评论区的长文战神。看到逻辑漏洞会忍不住拆解，享受思辨本身带来的快感。不是为了赢，是为了「说清楚」。"),
    "I_P_A_F": ("IPAF", "精准评论者",
        "能用一句话说完的绝不写一千字。短评犀利幽默，信息密度极高。精准、干脆、不啰嗦。"),
    "I_P_C_D": ("IPCD", "语境控场者",
        "带节奏的人——不是贬义。擅长把散乱的讨论重新框定，用叙事把大家拉到一个频道上来。"),
    "I_P_C_F": ("IPCF", "气氛制造者",
        "评论区发动机。表情包库存丰富，接梗天赋点满。上网就是为了大家一起开心。"),
    "I_S_A_D": ("ISAD", "结构冲击者",
        "长期潜水，但一发帖就是精华。大量输入后爆发式输出一次，然后消失。不需要解释第二遍。"),
    "I_S_A_F": ("ISAF", "精准狙击手",
        "平时不说话，一开口就让人无法反驳。只说关键的那一句，剩下的你自己消化。"),
    "I_S_C_D": ("ISCD", "情绪表达者",
        "安静但有深度。他的表达不是辩论，是倾诉。写长篇感受不是为了说服谁，是为了记录自己被打动的瞬间。"),
    "I_S_C_F": ("ISCF", "接梗王",
        "不主动挑事，但谁挑事他都接得住。点赞收藏转发表情包，轻量互动让气氛热起来。"),
    "R_P_A_D": ("RPAD", "冷静拆解者",
        "标准理性分析用户。不轻易发言，但一旦发言就准备充分。情绪化的言论无法带偏他——他只在乎逻辑。"),
    "R_P_A_F": ("RPAF", "轻量拆解者",
        "理性但不啰嗦。偶尔参与讨论，每句话踩在点上。不服来辩？没必要，我说了我的观点就够了。"),
    "R_P_C_D": ("RPCD", "结构建构者",
        "搭框架的人。主动整理信息、搭建体系、写入门指南。不在乎谁对谁错，只在乎有没有被组织好。"),
    "R_P_C_F": ("RPCF", "轻互动者",
        "有人@他就回一句。没人找他就默默刷。愿意帮忙但不愿寒暄。存在感不高但确实在。"),
    "R_S_A_D": ("RSAD", "深潜分析者",
        "长期潜水但比谁都懂。每天花几小时阅读吸收，但不发帖不评论。知识本身即奖励。"),
    "R_S_A_F": ("RSAF", "碎片思考者",
        "偶尔冒泡，但冒泡的那一句往往有意思。在多个领域浅层涉猎，什么都看一点，什么都能聊一句。"),
    "R_S_C_D": ("RSCD", "语境观察者",
        "他什么都知道，但从不说。对人和事有极强的洞察力，理解一切但不参与。享受的是理解本身。"),
    "R_S_C_F": ("RSCF", "轻观察者",
        "纯浏览型用户。互联网的隐形人。不点赞不评论不转发，唯一存在的证据就是DAU里的一个数字。"),
}

DIM_LETTERS = [
    {"L": "I", "R": "R"},

    {"L": "P", "R": "S"},

    {"L": "A", "R": "C"},

    {"L": "D", "R": "F"},

]

class NPFJEngine:

    def __init__(self):
        self.pools = self._load_pools()

    def _load_pools(self) -> dict:
        if not os.path.exists(POOLS_PATH):
            return {}
        with open(POOLS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("pools", {})

    def get_meta(self) -> dict:
        if not os.path.exists(POOLS_PATH):
            return {}
        with open(POOLS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("meta", {})

    def create_session(self) -> dict:
        return {
            "path": [],

            "pool_history": [1],

            "current_pool": 1,

            "weights": [0, 0, 0, 0, 0],

            "done": False,

        }

    def get_pool_questions(self, pool_id: int) -> Optional[list]:
        """
        获取指定题池的题目（给前端用，过滤掉权重等内部数据）
        返回每题的 id、text、选项文字（不含 route_label 和 weights）
        """
        pool = self.pools.get(str(pool_id))
        if not pool:
            return None

        safe_questions = []
        for q in pool.get("questions", []):
            safe_q = {
                "id": q["id"],
                "text": q["text"],
                "options": [
                    {"key": "A", "text": q["options"]["A"]["text"]},
                    {"key": "B", "text": q["options"]["B"]["text"]},
                    {"key": "C", "text": q["options"]["C"]["text"]},
                    {"key": "D", "text": q["options"]["D"]["text"]},
                ]
            }
            safe_questions.append(safe_q)
        return safe_questions

    def get_pool_info(self, pool_id: int) -> Optional[dict]:
        pool = self.pools.get(str(pool_id))
        if not pool:
            return None
        return {
            "id": pool_id,
            "stage": pool["stage"],
            "name": pool["name"],
            "description": pool.get("description", ""),
        }

    def submit_pool_answers(self, session: dict, pool_id: int, answers: list) -> Optional[dict]:
        """
        提交当前题池的 5 个答案，处理路由和权重累加

        参数：
            session: 当前用户会话
            pool_id: 当前题池 ID
            answers: ["A", "B", "A", "A", "B"] 长度 5 的列表

        返回：
            {
                "next_pool": int | None,

                "stage": int,

                "is_final": bool,

                "route_result": str,

            }
        """
        pool = self.pools.get(str(pool_id))
        if not pool:
            return None

        questions = pool.get("questions", [])
        if len(answers) != len(questions):
            return None

        route_counts = {"L": 0, "R": 0}
        for i, ans in enumerate(answers):
            q_data = questions[i]
            opt = q_data["options"].get(ans.upper(), q_data["options"].get("A"))
            label = opt["route"]
            route_counts[label] = route_counts.get(label, 0) + 1

        route_result = "L" if route_counts.get("L", 0) >= route_counts.get("R", 0) else "R"
        session["path"].append(route_result)

        route_map = pool.get("route_map", {})
        next_pool_str = route_map.get(route_result)

        next_pool = None
        is_final = False

        if next_pool_str is None:
            next_pool = 1
        elif isinstance(next_pool_str, int):
            next_pool = next_pool_str
        elif next_pool_str in ("D", "F", "J", "W"):
            is_final = True
            next_pool = None

        session["current_pool"] = next_pool
        if next_pool is not None:
            session["pool_history"].append(next_pool)

        if is_final:
            session["done"] = True

        return {
            "next_pool": next_pool,
            "stage": pool["stage"],
            "is_final": is_final,
            "route_result": route_result,
        }

    def finalize_result(self, session: dict) -> Optional[dict]:
        """
        最终结算：生成人格类型 + 五维雷达图数据

        参数：
            session: 已完成所有阶段的会话

        返回：
            {
                "type": "NPFJ",
                "type_title": "全栈掌控者",
                "description": "...",
                "path": ["L", "R", "L", "R"],
                "dimensions": [...],
                "radar_data": [...],
            }
        """
        if not session["done"]:
            return None

        path = session["path"]  # ["L", "L", "L", "L", "L"]
        letters = []
        for i, direction in enumerate(path):
            if i < len(DIM_LETTERS):
                letters.append(DIM_LETTERS[i].get(direction, "?"))
        type_code = "".join(letters)

        map_key = "_".join(letters)

        personality = PERSONALITY_MAP.get(map_key)

        if personality:
            _, title, desc = personality
        else:
            title = "未命名人格"
            desc = "描述待补充"

        report = _load_reports().get(map_key, "暂无分析报告")

        dim_names = self.get_meta().get("dimensions", ["D1", "D2", "D3", "D4"])
        dim_labels = self.get_meta().get("dimension_names", ["维度一", "维度二", "维度三", "维度四"])
        dimensions = []
        for i in range(min(4, len(path))):
            direction = path[i]
            letter = DIM_LETTERS[i].get(direction, "?")
            opposite = "R" if direction == "L" else "L"
            opp_letter = DIM_LETTERS[i].get(opposite, "?")

            base = 8 if direction == "L" else 4
            dimensions.append({
                "name": dim_labels[i] if i < len(dim_labels) else dim_names[i],
                "abbr": letter,
                "score": base,
                "opposite": opp_letter,
            })

        stage_names = ["能量表达", "参与方式", "认知方式", "表达方式"]
        path_letters = []
        for i, direction in enumerate(path):
            letter = DIM_LETTERS[i].get(direction, "?") if i < len(DIM_LETTERS) else "?"
            stage_name = stage_names[i] if i < len(stage_names) else f"阶段{i+1}"
            path_letters.append({
                "stage": stage_name,
                "direction": direction,
                "letter": letter,
            })

        return {
            "type": type_code,
            "title": title,
            "description": desc,
            "path": path,
            "path_letters": path_letters,
            "dimensions": dimensions,
            "report": report,
        }
