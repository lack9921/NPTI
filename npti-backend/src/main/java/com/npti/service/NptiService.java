package com.npti.service;

import com.npti.dto.NptiResponse;
import com.npti.dto.NptiResponse.DimensionItem;
import com.npti.dto.NptiResponse.RadarItem;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class NptiService {

    // 12 道题，每 3 题测一个维度
    private static final List<Map<String, Object>> QUESTIONS = new ArrayList<>();

    static {
        // 维度一：E/I（精力来源）—— 第 1-3 题
        QUESTIONS.add(Map.of(
            "id", 1, "text", "周末你更倾向于？",
            "options", List.of(
                Map.of("key", "A", "text", "约朋友出去玩"),
                Map.of("key", "B", "text", "在家打游戏或看书"),
                Map.of("key", "C", "text", "参加线下活动聚会"),
                Map.of("key", "D", "text", "一个人安静待着")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 2, "text", "在团队讨论中，你通常？",
            "options", List.of(
                Map.of("key", "A", "text", "积极发言，带动气氛"),
                Map.of("key", "B", "text", "认真听，偶尔插话"),
                Map.of("key", "C", "text", "主导话题走向"),
                Map.of("key", "D", "text", "默默记笔记，心里有数")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 3, "text", "你交朋友的方式是？",
            "options", List.of(
                Map.of("key", "A", "text", "主动认识，扩宽圈子"),
                Map.of("key", "B", "text", "通过共同朋友认识"),
                Map.of("key", "C", "text", "在各种场合都能自来熟"),
                Map.of("key", "D", "text", "随缘，不主动社交")
            )
        ));

        // 维度二：S/N（认知方式）—— 第 4-6 题
        QUESTIONS.add(Map.of(
            "id", 4, "text", "你更喜欢哪种类型的问题？",
            "options", List.of(
                Map.of("key", "A", "text", "有明确答案的具体问题"),
                Map.of("key", "B", "text", "需要想象力的开放问题"),
                Map.of("key", "C", "text", "跟实际生活相关的实用问题"),
                Map.of("key", "D", "text", "充满可能性的抽象问题")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 5, "text", "看说明书时，你通常会？",
            "options", List.of(
                Map.of("key", "A", "text", "一步一步照着做"),
                Map.of("key", "B", "text", "扫一眼大概，自己摸索"),
                Map.of("key", "C", "text", "只关注关键步骤"),
                Map.of("key", "D", "text", "凭直觉操作，出问题再看")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 6, "text", "你更容易记住？",
            "options", List.of(
                Map.of("key", "A", "text", "具体发生过的事情细节"),
                Map.of("key", "B", "text", "当时的感受和整体氛围"),
                Map.of("key", "C", "text", "事实和数据"),
                Map.of("key", "D", "text", "对未来的联想和可能")
            )
        ));

        // 维度三：T/F（决策方式）—— 第 7-9 题
        QUESTIONS.add(Map.of(
            "id", 7, "text", "朋友向你倾诉烦恼，你第一反应是？",
            "options", List.of(
                Map.of("key", "A", "text", "帮ta分析问题出在哪"),
                Map.of("key", "B", "text", "理解ta的感受，表示支持"),
                Map.of("key", "C", "text", "直接给解决方案"),
                Map.of("key", "D", "text", "陪着ta，说什么不重要")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 8, "text", "做重要决定时，你更依赖？",
            "options", List.of(
                Map.of("key", "A", "text", "逻辑分析和事实依据"),
                Map.of("key", "B", "text", "内心的价值观和感受"),
                Map.of("key", "C", "text", "效率和收益最大化"),
                Map.of("key", "D", "text", "这件事对人际关系的影响")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 9, "text", "别人对你提出批评，你通常？",
            "options", List.of(
                Map.of("key", "A", "text", "先看ta说得有没有道理"),
                Map.of("key", "B", "text", "有点受伤，但会反思"),
                Map.of("key", "C", "text", "如果没道理就直接忽略"),
                Map.of("key", "D", "text", "在意对方的感受多于对错")
            )
        ));

        // 维度四：J/P（生活态度）—— 第 10-12 题
        QUESTIONS.add(Map.of(
            "id", 10, "text", "你的书桌/工作区通常是？",
            "options", List.of(
                Map.of("key", "A", "text", "整整齐齐，每样东西有固定位置"),
                Map.of("key", "B", "text", "有自己的一套乱序但找得到"),
                Map.of("key", "C", "text", "定期收拾，但日常会乱"),
                Map.of("key", "D", "text", "随心所欲，懒得整理")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 11, "text", "你更喜欢哪种生活方式？",
            "options", List.of(
                Map.of("key", "A", "text", "提前制定好计划按部就班"),
                Map.of("key", "B", "text", "有大方向但细节随缘"),
                Map.of("key", "C", "text", "排好优先级按重要程度来"),
                Map.of("key", "D", "text", "想到什么做什么，随性")
            )
        ));
        QUESTIONS.add(Map.of(
            "id", 12, "text", "面对未预期的变化，你的态度是？",
            "options", List.of(
                Map.of("key", "A", "text", "不太喜欢，希望按原计划走"),
                Map.of("key", "B", "text", "可以接受，随机应变"),
                Map.of("key", "C", "text", "有点烦躁但能调整"),
                Map.of("key", "D", "text", "拥抱变化，觉得很有趣")
            )
        ));
    }

    // 16 种人格类型的详细数据
    private static final Map<String, String[]> PERSONALITY_DATA = new LinkedHashMap<>();
    static {
        PERSONALITY_DATA.put("ISTJ", new String[]{"检查员型人格", "务实、负责、可靠。你是一个做事有条理、注重细节的人，喜欢按规则和流程办事。在团队中是值得信赖的中坚力量。"});
        PERSONALITY_DATA.put("ISFJ", new String[]{"守护者型人格", "温暖、体贴、有责任感。你非常关心身边的人，善于察言观色，乐于默默付出。是团队里的"后勤保障"。"});
        PERSONALITY_DATA.put("INFJ", new String[]{"提倡者型人格", "理想主义、有洞察力、有使命感。你善于理解复杂的人性和抽象的概念，总是想为世界带来积极的改变。"});
        PERSONALITY_DATA.put("INTJ", new String[]{"建筑师型人格", "富有想象力、战略性、果断。你是一个天生的规划者，总能从全局视角看到问题的本质，并制定出最优方案。"});
        PERSONALITY_DATA.put("ISTP", new String[]{"鉴赏家型人格", "灵活、理性、注重实操。你擅长动手解决问题，喜欢探索事物运行的原理。冷静沉着，关键时刻很可靠。"});
        PERSONALITY_DATA.put("ISFP", new String[]{"探险家型人格", "安静、敏感、有艺术气质。你热爱美和自然，重视个人的感受和价值观。用行动而非言语表达自己。"});
        PERSONALITY_DATA.put("INFP", new String[]{"调停者型人格", "理想主义、充满热情、富有创造力。你内心深处有坚定的价值观，总在寻找生活的意义和真实的情感连接。"});
        PERSONALITY_DATA.put("INTP", new String[]{"逻辑学家型人格", "创新、理性、喜欢理论。你天生爱思考，对抽象的概念和理论充满好奇。典型的"书呆子天才"。"});
        PERSONALITY_DATA.put("ESTP", new String[]{"企业家型人格", "精力充沛、果断、善于社交。你是行动派，喜欢在实践中学习。在社交场合游刃有余，是天生的谈判家。"});
        PERSONALITY_DATA.put("ESFP", new String[]{"表演者型人格", "外向、快乐、充满感染力。你是人群中的开心果，喜欢成为关注的焦点。享受当下，热爱生活。"});
        PERSONALITY_DATA.put("ENFP", new String[]{"竞选者型人格", "热情、富有创造力、自由奔放。你充满好奇心和能量，善于发现各种可能性。能感染身边的每一个人。"});
        PERSONALITY_DATA.put("ENTP", new String[]{"辩论家型人格", "聪明、好奇、善辩。你热爱挑战和头脑风暴，总能从不同角度看待问题。是让人又爱又恨的"杠精"。"});
        PERSONALITY_DATA.put("ESTJ", new String[]{"总经理型人格", "高效、果断、有领导力。你是一个天生的管理者，注重秩序和效率。做事雷厉风行，执行力极强。"});
        PERSONALITY_DATA.put("ESFJ", new String[]{"执政官型人格", "热情、有责任感、重视和谐。你非常注重人际关系，乐于为他人服务。是团队里的"大家长"。"});
        PERSONALITY_DATA.put("ENFJ", new String[]{"主人公型人格", "有魅力、有感染力、利他主义。你天生就是领导者，善于发现并挖掘他人的潜能。总能让团队变得更好。"});
        PERSONALITY_DATA.put("ENTJ", new String[]{"指挥官型人格", "果断、有战略眼光、天生领袖。你目标明确，逻辑清晰，善于组织和指挥。是天生的 CEO 人格。"});
    }

    // 获取全部题目（给前端用，不含答案）
    public List<Map<String, Object>> getQuestions() {
        List<Map<String, Object>> result = new ArrayList<>();
        for (Map<String, Object> q : QUESTIONS) {
            Map<String, Object> safe = new LinkedHashMap<>();
            safe.put("id", q.get("id"));
            safe.put("text", q.get("text"));
            safe.put("options", q.get("options"));
            result.add(safe);
        }
        return result;
    }

    // 核心算分逻辑
    public NptiResponse calculateResult(List<String> answers) {
        if (answers == null || answers.size() < 12) {
            throw new IllegalArgumentException("需要 12 个答案");
        }

        // 四个维度的得分（每个维度 3 题，每题 1-4 分）
        int[] dimensionScores = new int[4];

        for (int i = 0; i < 12; i++) {
            String ans = answers.get(i).toUpperCase();
            int score;
            switch (ans) {
                case "A": score = 1; break;
                case "B": score = 2; break;
                case "C": score = 3; break;
                case "D": score = 4; break;
                default: score = 2; break;
            }
            dimensionScores[i / 3] += score;
        }

        // 每个维度 3-12 分，<=6 归第一类，>6 归第二类
        // 维度 0: E(<=6) / I(>6)
        // 维度 1: S(<=6) / N(>6)
        // 维度 2: T(<=6) / F(>6)
        // 维度 3: J(<=6) / P(>6)

        String[] dimTypes = {"I", "N", "F", "P"};  // >6 时取
        String[] dimOpposites = {"E", "S", "T", "J"}; // <=6 时取

        StringBuilder typeBuilder = new StringBuilder();
        List<DimensionItem> dimItems = new ArrayList<>();
        List<RadarItem> radarItems = new ArrayList<>();

        String[] dimNames = {"精力来源", "认知方式", "决策方式", "生活态度"};
        String[] dimAbbrs = {"I/E", "N/S", "F/T", "P/J"};

        for (int i = 0; i < 4; i++) {
            int score = dimensionScores[i];
            boolean isFirstType = score <= 6;
            String chosen = isFirstType ? dimOpposites[i] : dimTypes[i];
            String opposite = isFirstType ? dimTypes[i] : dimOpposites[i];
            typeBuilder.append(chosen);

            // 雷达图用归一化分数 (3-12 → 0-100)
            int radarValue = (score - 3) * 100 / 9;

            dimItems.add(new DimensionItem(dimNames[i], chosen, score, opposite));
            radarItems.add(new RadarItem(dimAbbrs[i], radarValue));
        }

        String nptiType = typeBuilder.toString();
        String[] personalityInfo = PERSONALITY_DATA.getOrDefault(nptiType,
            new String[]{"探索者型人格", "你是一个独特而复杂的人，无法被简单定义。继续保持你的独特性！"});

        NptiResponse res = new NptiResponse();
        res.setNptiType(nptiType);
        res.setTitle(personalityInfo[0]);
        res.setDescription(personalityInfo[1]);
        res.setDimensions(dimItems);
        res.setRadarData(radarItems);

        return res;
    }
}
