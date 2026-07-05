class WeightCalculator:

    def __init__(self):
        self.dim_names = ["精神续航", "社交磁场", "秩序洁癖", "压力解压阀", "脑力劳作"]
        self.max_per_question = 2
        self.total_questions = 20

    def accumulate(self, state, option_weights):
        for i in range(5):
            state[i] += option_weights[i]
        return state

    def compute_radar(self, state):
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

    def compute_color(self, state):
        if not state or len(state) < 5:
            return "rgb(15, 12, 41)"

        max_v = self.max_per_question * self.total_questions
        w = [min(max_v, max(0, s)) for s in state]

        r = int(8 + w[3] * 0.7)

        g = int(6 + w[1] * 0.5)

        b = int(10 + w[4] * 0.6)

        r += int(w[0] * 0.15)

        b += int(w[2] * 0.2)

        r = min(55, max(5, r))
        g = min(45, max(3, g))
        b = min(55, max(5, b))

        return f"rgb({r},{g},{b})"

    def compute_color_gradient(self, state, stage):
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

    def compute_all(self, state, stage=0):
        return {
            "radar": self.compute_radar(state),
            "color": self.compute_color(state),
            "gradient": self.compute_color_gradient(state, stage),
        }
