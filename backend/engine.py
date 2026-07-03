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
    "N_L_F_J": ("N-L-F-J", "全栈掌控者", "你是典型的全栈型数字公民。在公网中自如穿梭，主动探索新工具，追求效率至上的工作流，同时保持着结构化的数字生活管理。"),
    "N_L_F_W": ("N-L-F-W", "赛博游侠", "你是公网中的自由探险家。喜欢在开源世界主动摸索新事物，凭直觉高效解决眼前问题，但数字生活随性而为，不拘泥于条条框框。"),
    "N_L_R_J": ("N-L-R-J", "架构师", "你是公网中的深度思考者。倾向于吸收信息后系统性地消化，追求底层逻辑的清晰，同时用严密的体系管理你的数字世界。"),
    "N_L_R_W": ("N-L-R-W", "信息收藏家", "你在公网中安静地吸收大量信息，习惯于深度追踪感兴趣的话题，但你的数字世界更像一个巨大的收藏夹，随性而丰富。"),
    "N_P_F_J": ("N-P-F-J", "开源布道师", "你是社区中的活跃贡献者。乐于在公网中分享和输出，追求快速产出和实用结果，同时用有序的方式管理你的项目和任务。"),
    "N_P_F_W": ("N-P-F-W", "精炼科普者", "你是公网中的高效传播者。喜欢用简洁的方式输出干货，追求快速传达核心信息，但不拘泥于长篇大论的系统框架。"),
    "N_P_R_J": ("N-P-R-J", "敏捷开发者", "你在社区中积极参与，乐于协作共建，习惯在动手前理清逻辑关系，同时保持着结构化的开发流程。"),
    "N_P_R_W": ("N-P-R-W", "气氛组组长", "你是社区的活跃分子，喜欢在各大平台上留下自己的印记，凭直觉快速回应各种话题，但你的参与方式灵活多变，不成体系。"),
    "S_L_F_J": ("S-L-F-J", "本地掌控者", "你偏爱本地化和私有化的数字环境。安静地构建自己的专属工具链，追求最高效的工作流，一切都在你的绝对掌控之中。"),
    "S_L_F_W": ("S-L-F-W", "静默体验派", "你在自己的数字世界里安静操作，遇到新工具先默默试用，追求直觉式的操作体验，不关心外界的评价和标准。"),
    "S_L_R_J": ("S-L-R-J", "隐秘架构师", "你在本地环境中深耕，倾向于系统性地研究技术底层，喜欢一切井井有条，打造完美配置的数字堡垒。"),
    "S_L_R_W": ("S-L-R-W", "前沿冲浪者", "你虽然不爱公开表达，但一直在自己的轨道上追踪最新技术趋势，随性地在各种技术栈之间穿梭探索。"),
    "S_P_F_J": ("S-P-F-J", "效率工程师", "你在自己的专业领域内积极产出，追求最优解和最高效率，同时用严谨的方法论管理你的工作和学习。"),
    "S_P_F_W": ("S-P-F-W", "实用主义者", "你专注于解决实际问题，在自己的领域内高效输出，灵活运用各种工具达成目标，不在乎用的是不是"标准做法"。"),
    "S_P_R_J": ("S-P-R-J", "系统构建者", "你在专业领域深入耕耘，习惯在行动前构建完整的知识体系，并将其系统地组织和管理起来。"),
    "S_P_R_W": ("S-P-R-W", "特立独行者", "你在自己的专业领域有着独特的见解和输出，凭兴趣深入探索各种技术方向，路径独特但充满创意。"),
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
        type_code = "".join(letters)  # 如 "NPLF"

        # 构建 PERSONALITY_MAP 的查询键："N_P_L_F"
        map_key = "_".join(letters)

        # 获取人格描述
        personality = PERSONALITY_MAP.get(map_key)

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
