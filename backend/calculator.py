"""
calculator.py —— 权重计算引擎

与 engine.py（路由引擎）完全解耦。
此文件仅负责：五维雷达图计算 + 背景染色 + 未来任何基于权重的扩展。

你可以在这里引入任意高级数学公式。
"""


class WeightCalculator:
    """权重计算器，独立于路由引擎"""

    def __init__(self):
        self.dim_names = ["精神续航", "社交磁场", "秩序洁癖", "压力解压阀", "脑力劳作"]
        self.max_per_question = 2
        self.total_questions = 20

    def accumulate(self, state: list, option_weights: list) -> list:
        """
        累加一道题的权重到状态中。
        state: 当前累积权重 [w0, w1, w2, w3, w4]
        option_weights: 本题选项的权重 [w0, w1, w2, w3, w4]
        返回新的 state。
        """
        for i in range(5):
            state[i] += option_weights[i]
        return state

    def compute_radar(self, state: list) -> list:
        """
        从累积权重计算五维雷达图数据（归一化到 0-100）。
        
        以实际累积值的最大值为基准，让图表撑满显示区域。
        """
        if not state or len(state) < 5:
            return [{"name": n, "value": 0} for n in self.dim_names]
        
        actual_max = max(state[:5])
        base = max(20, actual_max)
        radar = []
        for i in range(5):
            raw = state[i] if i < len(state) else 0
            normalized = min(100, int(raw / base * 100)) if base > 0 else 50
            radar.append({"name": self.dim_names[i], "value": normalized})
        return radar

    def compute_color(self, state: list) -> str:
        """
        从累积权重计算背景颜色。
        
        当前公式：每维权重映射到 RGB 通道。
        你可以换成任何配色算法——HSL 插值、色相偏移、粒子系统映射等。
        
        映射规则：
          - 压力解压阀 → R 通道
          - 社交磁场 → G 通道
          - 脑力劳作 → B 通道
          - 精神续航和秩序洁癖混合影响饱和度和偏移
        """
        if not state or len(state) < 5:
            return "rgb(15, 12, 41)"

        max_v = self.max_per_question * self.total_questions
        w = [min(max_v, max(0, s)) for s in state]

        # RGB 通道映射
        r = int(8 + w[3] * 0.7)
        g = int(6 + w[1] * 0.5)
        b = int(10 + w[4] * 0.6)

        r += int(w[0] * 0.15)
        b += int(w[2] * 0.2)

        r = min(55, max(5, r))
        g = min(45, max(3, g))
        b = min(55, max(5, b))

        return f"rgb({r},{g},{b})"

    def compute_color_gradient(self, state: list, stage: int) -> str:
        """
        生成阶段背景渐变 CSS。
        结合阶段基色和权重累积色。
        """
        base_dark = [
            (10, 15, 35),
            (8, 18, 22),
            (18, 10, 35),
            (32, 12, 25),
        ]

        bg = self.compute_color(state)
        nums = [int(x) for x in bg.replace("rgb(", "").replace(")", "").split(",")]

        stage_base = base_dark[stage] if stage < len(base_dark) else base_dark[0]

        mixed_r = int(stage_base[0] * 0.7 + nums[0] * 0.3)
        mixed_g = int(stage_base[1] * 0.7 + nums[1] * 0.3)
        mixed_b = int(stage_base[2] * 0.7 + nums[2] * 0.3)

        mixed_r = min(50, max(5, mixed_r))
        mixed_g = min(45, max(3, mixed_g))
        mixed_b = min(50, max(5, mixed_b))

        return (
            f"linear-gradient(135deg, "
            f"rgb({mixed_r},{mixed_g},{mixed_b}) 0%, "
            f"rgb({mixed_r+10},{mixed_g+6},{mixed_b+8}) 50%, "
            f"rgb({mixed_r},{mixed_g},{mixed_b}) 100%)"
        )

    def compute_all(self, state: list, stage: int = 0) -> dict:
        """
        一次性计算所有基于权重的输出。
        
        返回：
        {
            "radar": [...],
            "color": "rgb(...)",
            "gradient": "linear-gradient(...)",
        }
        
        未来扩展：在此方法中加入新的计算项即可。
        """
        return {
            "radar": self.compute_radar(state),
            "color": self.compute_color(state),
            "gradient": self.compute_color_gradient(state, stage),
        }
