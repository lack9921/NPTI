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
POOLS_PATH = os.path.join(ROOT, "pools.json")


# ============================================================
#  16 种人格类型描述（纯心理学中性描述，无贬义）
#  按路径组合 [N/S][P/L][F/R][J/W] 排列
# ============================================================
PERSONALITY_MAP = {
    "N_L_F_J": ("N-L-F-J", "占位标题", "占位描述"),
    "N_L_F_W": ("N-L-F-W", "占位标题", "占位描述"),
    "N_L_R_J": ("N-L-R-J", "占位标题", "占位描述"),
    "N_L_R_W": ("N-L-R-W", "占位标题", "占位描述"),
    "N_P_F_J": ("N-P-F-J", "占位标题", "占位描述"),
    "N_P_F_W": ("N-P-F-W", "占位标题", "占位描述"),
    "N_P_R_J": ("N-P-R-J", "占位标题", "占位描述"),
    "N_P_R_W": ("N-P-R-W", "占位标题", "占位描述"),
    "S_L_F_J": ("S-L-F-J", "占位标题", "占位描述"),
    "S_L_F_W": ("S-L-F-W", "占位标题", "占位描述"),
    "S_L_R_J": ("S-L-R-J", "占位标题", "占位描述"),
    "S_L_R_W": ("S-L-R-W", "占位标题", "占位描述"),
    "S_P_F_J": ("S-P-F-J", "占位标题", "占位描述"),
    "S_P_F_W": ("S-P-F-W", "占位标题", "占位描述"),
    "S_P_R_J": ("S-P-R-J", "占位标题", "占位描述"),
    "S_P_R_W": ("S-P-R-W", "占位标题", "占位描述"),
}

# 四个维度的字母映射（路径方向 → 人格字母）
# Stage 1: L=N, R=S
# Stage 2: L=P, R=L
# Stage 3: L=F, R=R
# Stage 4: L=J, R=W
DIM_LETTERS = [
    {"L": "N", "R": "S"},  # Stage 1
    {"L": "P", "R": "L"},  # Stage 2
    {"L": "F", "R": "R"},  # Stage 3
    {"L": "J", "R": "W"},  # Stage 4
]


class NPFJEngine:
    """NPFJ 二分树路由引擎"""

    def __init__(self):
        self.pools = self._load_pools()

    def _load_pools(self) -> dict:
        """加载题库 JSON"""
        if not os.path.exists(POOLS_PATH):
            return {}
        with open(POOLS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("pools", {})

    def get_meta(self) -> dict:
        """返回题库元信息"""
        if not os.path.exists(POOLS_PATH):
            return {}
        with open(POOLS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("meta", {})

    def create_session(self) -> dict:
        """创建新会话（用户开始测试时调用）"""
        return {
            "path": [],               # 路由路径，如 ["L", "R", "L"]
            "pool_history": [0],      # 走过的题池，从 0（基准校准）开始
            "current_pool": 0,        # 当前题池 ID
            "weights": [0, 0, 0, 0, 0],  # 五维权重累加
            "done": False,            # 是否已完成
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
                ]
            }
            safe_questions.append(safe_q)
        return safe_questions

    def get_pool_info(self, pool_id: int) -> Optional[dict]:
        """返回题池信息（不含题目细节）"""
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
                "next_pool": int | None,    # 下一题池 ID，None 表示已完成
                "stage": int,               # 当前阶段
                "is_final": bool,           # 是否已完成所有阶段
                "route_result": str,        # 本阶段路由结果（L/R）
            }
        """
        pool = self.pools.get(str(pool_id))
        if not pool:
            return None

        questions = pool.get("questions", [])
        if len(answers) != len(questions):
            return None

        # 统计路由方向 + 累加权重
        route_counts = {"L": 0, "R": 0}
        for i, ans in enumerate(answers):
            q_data = questions[i]
            opt = q_data["options"].get(ans.upper(), q_data["options"].get("A"))
            label = opt["route"]
            route_counts[label] = route_counts.get(label, 0) + 1
            # 累加五维权重
            w = opt.get("weights", [0, 0, 0, 0, 0])
            for j in range(5):
                session["weights"][j] += w[j]

        # 路由：多数决
        route_result = "L" if route_counts.get("L", 0) >= route_counts.get("R", 0) else "R"
        session["path"].append(route_result)

        # 根据 route_map 确定下一题池
        route_map = pool.get("route_map", {})
        next_pool_str = route_map.get(route_result)

        next_pool = None
        is_final = False

        if next_pool_str is None:
            # Stage 0（基准校准）：固定路由到 Stage 1（pool 1）
            next_pool = 1
        elif isinstance(next_pool_str, int):
            next_pool = next_pool_str
        elif next_pool_str in ("J", "W"):
            # Stage 4：最终决出，没有下一题池
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

        # 从路径生成 4 位字母
        path = session["path"]  # ["L", "R", "L", "R"]
        letters = []
        for i, direction in enumerate(path):
            if i < len(DIM_LETTERS):
                letters.append(DIM_LETTERS[i].get(direction, "?"))
        type_code = "".join(letters)

        # 获取人格描述
        path_key = "_".join(path[:4]) if len(path) >= 4 else "_".join(path)
        # 也支持直接用字母码查找
        personality = PERSONALITY_MAP.get(path_key)
        if not personality:
            personality = PERSONALITY_MAP.get(type_code)

        if personality:
            _, title, desc = personality
        else:
            title = "未命名人格"
            desc = "描述待补充"

        # 生成维度信息
        dim_names = self.get_meta().get("dimensions", ["D1", "D2", "D3", "D4"])
        dim_labels = self.get_meta().get("dimension_names", ["维度一", "维度二", "维度三", "维度四"])
        dimensions = []
        for i in range(min(4, len(path))):
            direction = path[i]
            letter = DIM_LETTERS[i].get(direction, "?")
            opposite = "R" if direction == "L" else "L"
            opp_letter = DIM_LETTERS[i].get(opposite, "?")

            # 为每个方向给一个分布分数（基于路径确定性）
            # 这里简化：L 方向给 7-9 分，R 方向给 3-5 分
            base = 8 if direction == "L" else 4
            dimensions.append({
                "name": dim_labels[i] if i < len(dim_labels) else dim_names[i],
                "abbr": letter,
                "score": base,
                "opposite": opp_letter,
            })

        # 五维雷达图数据（归一化到 0-100）
        weight_dims = self.get_meta().get("weight_dims", ["W1", "W2", "W3", "W4", "W5"])
        weights = session["weights"]

        # 归一化：假设最大可能每题 2 分 × 20 题 = 40 分，归一化到 0-100
        max_possible = 40  # 20 题 × 2 分每题（一个维度的最大累积）
        radar_data = []
        for i in range(min(5, len(weights))):
            normalized = min(100, int(weights[i] / max_possible * 100)) if max_possible > 0 else 50
            dim_label = weight_dims[i] if i < len(weight_dims) else f"W{i+1}"
            radar_data.append({
                "name": dim_label,
                "value": normalized,
            })

        # 路径字母表示（给前端展示）
        path_letters = []
        stage_names = ["基准校准", "连接拓扑", "探针模式", "路由逻辑", "输出格式"]
        for i, direction in enumerate(path):
            letter = DIM_LETTERS[i].get(direction, "?") if i < len(DIM_LETTERS) else "?"
            stage_name = stage_names[i + 1] if i + 1 < len(stage_names) else f"阶段{i+1}"
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
            "radar_data": radar_data,
        }
