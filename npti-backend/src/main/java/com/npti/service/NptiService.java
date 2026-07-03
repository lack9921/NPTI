package com.npti.service;

import com.npti.dto.NptiResponse;
import com.npti.dto.NptiResponse.DimensionItem;
import com.npti.dto.NptiResponse.RadarItem;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * =============================================
 *  ⭐ 核心算分逻辑 —— 整个项目的"大脑"
 *  =============================================
 *  
 *  这个类负责两件事：
 *  1. 提供 12 道测试题（每 3 题测一个维度）
 *  2. 接收用户的 12 个答案 → 算分 → 得出人格类型
 *  
 *  四个维度：
 *  维度一（1-3 题）：E（外向）/ I（内向）—— 精力来源
 *  维度二（4-6 题）：S（实感）/ N（直觉）—— 认知方式
 *  维度三（7-9 题）：T（理性）/ F（感性）—— 决策方式
 *  维度四（10-12 题）：J（计划）/ P（随性）—— 生活态度
 *  
 *  算分规则：
 *  - 每题选 A=1分, B=2分, C=3分, D=4分
 *  - 每个维度 3 题，总分范围：3~12 分
 *  - 分数 <= 6 → 归为第一类（如 E/S/T/J）
 *  - 分数 > 6  → 归为第二类（如 I/N/F/P）
 *  - 四个维度组合成 16 种人格类型
 *  
 *  🎯 如果想改成自创的 NPTI / SBTI 维度，就改这里的评分规则！
 */
@Service  // @Service 标记这是一个服务类，Spring 会自动管理它
public class NptiService {

    // =================================================================
    //  第一部分：题库（12 道题，每 3 题测一个维度）
    //  =================================================================
    //  QUESTIONS 是一个列表，每道题用 Map（类似字典）存储
    //  static { ... } 是静态代码块，类加载时自动执行，相当于初始化
    //
    //  每道题的格式：
    //  {
    //    "id": 1,              ← 题号
    //    "text": "题目文字",    ← 题目内容
    //    "options": [          ← 四个选项
    //      { "key": "A", "text": "选项文字" },
    //      ...
    //    ]
    //  }
    // =================================================================
    private static final List<Map<String, Object>> QUESTIONS = new ArrayList<>();

    static {
        // ---------- 维度一：E（外向）/ I（内向）—— 第 1-3 题 ----------
        // A 和 C 偏外向（E），B 和 D 偏内向（I）
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

        // ---------- 维度二：S（实感）/ N（直觉）—— 第 4-6 题 ----------
        // A 和 C 偏实感（S），B 和 D 偏直觉（N）
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

        // ---------- 维度三：T（理性）/ F（感性）—— 第 7-9 题 ----------
        // A 和 C 偏理性（T），B 和 D 偏感性（F）
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

        // ---------- 维度四：J（计划）/ P（随性）—— 第 10-12 题 ----------
        // A 和 C 偏计划（J），B 和 D 偏随性（P）
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

    // =================================================================
    //  第二部分：16 种人格类型及其描述
    //  =================================================================
    //  格式：Map<"四位字母", ["标题", "详细描述"]>
    //  四位字母由四个维度的结果组合而成
    //
    //  如果你想自定义人格描述，直接改这里的文字！
    //  或者如果你想加"程序员专属 SBTI"类型，在这里加新的映射
    // =================================================================
    private static final Map<String, String[]> PERSONALITY_DATA = new LinkedHashMap<>();
    static {
        // ---- 内倾（I）系列 ----
        PERSONALITY_DATA.put("ISTJ", new String[]{"检查员型人格",
            "务实、负责、可靠。你是一个做事有条理、注重细节的人，喜欢按规则和流程办事。在团队中是值得信赖的中坚力量。"});
        PERSONALITY_DATA.put("ISFJ", new String[]{"守护者型人格",
            "温暖、体贴、有责任感。你非常关心身边的人，善于察言观色，乐于默默付出。是团队里的「后勤保障」。"});
        PERSONALITY_DATA.put("INFJ", new String[]{"提倡者型人格",
            "理想主义、有洞察力、有使命感。你善于理解复杂的人性和抽象的概念，总是想为世界带来积极的改变。"});
        PERSONALITY_DATA.put("INTJ", new String[]{"建筑师型人格",
            "富有想象力、战略性、果断。你是一个天生的规划者，总能从全局视角看到问题的本质，并制定出最优方案。"});

        PERSONALITY_DATA.put("ISTP", new String[]{"鉴赏家型人格",
            "灵活、理性、注重实操。你擅长动手解决问题，喜欢探索事物运行的原理。冷静沉着，关键时刻很可靠。"});
        PERSONALITY_DATA.put("ISFP", new String[]{"探险家型人格",
            "安静、敏感、有艺术气质。你热爱美和自然，重视个人的感受和价值观。用行动而非言语表达自己。"});
        PERSONALITY_DATA.put("INFP", new String[]{"调停者型人格",
            "理想主义、充满热情、富有创造力。你内心深处有坚定的价值观，总在寻找生活的意义和真实的情感连接。"});
        PERSONALITY_DATA.put("INTP", new String[]{"逻辑学家型人格",
            "创新、理性、喜欢理论。你天生爱思考，对抽象的概念和理论充满好奇。典型的「书呆子天才」。"});

        // ---- 外倾（E）系列 ----
        PERSONALITY_DATA.put("ESTP", new String[]{"企业家型人格",
            "精力充沛、果断、善于社交。你是行动派，喜欢在实践中学习。在社交场合游刃有余，是天生的谈判家。"});
        PERSONALITY_DATA.put("ESFP", new String[]{"表演者型人格",
            "外向、快乐、充满感染力。你是人群中的开心果，喜欢成为关注的焦点。享受当下，热爱生活。"});
        PERSONALITY_DATA.put("ENFP", new String[]{"竞选者型人格",
            "热情、富有创造力、自由奔放。你充满好奇心和能量，善于发现各种可能性。能感染身边的每一个人。"});
        PERSONALITY_DATA.put("ENTP", new String[]{"辩论家型人格",
            "聪明、好奇、善辩。你热爱挑战和头脑风暴，总能从不同角度看待问题。是让人又爱又恨的「杠精」。"});

        PERSONALITY_DATA.put("ESTJ", new String[]{"总经理型人格",
            "高效、果断、有领导力。你是一个天生的管理者，注重秩序和效率。做事雷厉风行，执行力极强。"});
        PERSONALITY_DATA.put("ESFJ", new String[]{"执政官型人格",
            "热情、有责任感、重视和谐。你非常注重人际关系，乐于为他人服务。是团队里的「大家长」。"});
        PERSONALITY_DATA.put("ENFJ", new String[]{"主人公型人格",
            "有魅力、有感染力、利他主义。你天生就是领导者，善于发现并挖掘他人的潜能。总能让团队变得更好。"});
        PERSONALITY_DATA.put("ENTJ", new String[]{"指挥官型人格",
            "果断、有战略眼光、天生领袖。你目标明确，逻辑清晰，善于组织和指挥。是天生的 CEO 人格。"});
    }

    // =================================================================
    //  方法一：获取所有题目（给前端用的，不包含答案）
    //  =================================================================
    //  前端请求 GET /api/test/questions 时调用这个方法。
    //  注意：这里把原始题库复制了一份返回，而不是直接返回 QUESTIONS，
    //  因为直接返回可能不小心把答案泄露出去。
    // =================================================================
    public List<Map<String, Object>> getQuestions() {
        List<Map<String, Object>> result = new ArrayList<>();
        for (Map<String, Object> q : QUESTIONS) {
            Map<String, Object> safe = new LinkedHashMap<>();
            safe.put("id", q.get("id"));          // 题号
            safe.put("text", q.get("text"));      // 题目文字
            safe.put("options", q.get("options")); // 四个选项
            result.add(safe);
        }
        return result;
    }

    // =================================================================
    //  方法二：核心算分逻辑 ⭐
    //  =================================================================
    //  这是整个程序最关键的方法！
    //  接收 12 个答案 → 算分 → 映射人格类型
    //
    //  参数：List<String> answers
    //        例如 ["A", "B", "A", "C", "D", "A", "B", "A", "A", "C", "D", "B"]
    //        每个元素是 "A" / "B" / "C" / "D"
    //
    //  返回：NptiResponse 对象（包含人格类型、描述、雷达图数据等）
    // =================================================================
    public NptiResponse calculateResult(List<String> answers) {
        // 安全检查：如果前端没传够 12 个答案就报错
        if (answers == null || answers.size() < 12) {
            throw new IllegalArgumentException("需要 12 个答案");
        }

        // ---------- 第一步：计算每个维度的原始得分 ----------
        // dimensionScores[0] = 维度一（E/I）总分（3~12）
        // dimensionScores[1] = 维度二（S/N）总分（3~12）
        // dimensionScores[2] = 维度三（T/F）总分（3~12）
        // dimensionScores[3] = 维度四（J/P）总分（3~12）
        int[] dimensionScores = new int[4];

        // 遍历 12 个答案，每题算出 1-4 分，累加到对应维度
        // i / 3 的意思是：第 0,1,2 题 → 维度0，第 3,4,5 题 → 维度1，以此类推
        for (int i = 0; i < 12; i++) {
            String ans = answers.get(i).toUpperCase();  // 转大写，防止前端传了小写
            int score;
            switch (ans) {
                case "A": score = 1; break;
                case "B": score = 2; break;
                case "C": score = 3; break;
                case "D": score = 4; break;
                default: score = 2; break;  // 传了奇怪的值默认给 2 分
            }
            dimensionScores[i / 3] += score;  // 累加到对应维度
        }

        // ---------- 第二步：根据得分判定四个维度的字母 ----------
        // 计分规则：每个维度总分 3~12
        //   <= 6 分 → 第一类（E / S / T / J）
        //   > 6 分  → 第二类（I / N / F / P）
        //
        // 为什么用 6 分做分界线？
        // 每题 1-4 分，3 题总分 3-12，中间值是 7.5
        // 6 分意味着每题平均 2 分（选了 B），属于偏第一类
        // 7 分以上意味着平均选了 C 或 D，属于偏第二类

        // dimTypes：分数 > 6 时取的字母
        String[] dimTypes = {"I", "N", "F", "P"};
        // dimOpposites：分数 <= 6 时取的字母
        String[] dimOpposites = {"E", "S", "T", "J"};

        StringBuilder typeBuilder = new StringBuilder();  // 拼出四位字母
        List<DimensionItem> dimItems = new ArrayList<>();  // 维度详情
        List<RadarItem> radarItems = new ArrayList<>();    // 雷达图数据

        String[] dimNames = {"精力来源", "认知方式", "决策方式", "生活态度"};
        String[] dimAbbrs = {"I/E", "N/S", "F/T", "P/J"};

        for (int i = 0; i < 4; i++) {
            int score = dimensionScores[i];
            boolean isFirstType = score <= 6;
            String chosen = isFirstType ? dimOpposites[i] : dimTypes[i];
            String opposite = isFirstType ? dimTypes[i] : dimOpposites[i];
            typeBuilder.append(chosen);  // 拼出四位字母

            // 把原始得分（3-12）映射到雷达图的 0-100 范围
            // 公式：(当前分 - 最低分) / (最高分 - 最低分) * 100
            // = (score - 3) / (12 - 3) * 100 = (score - 3) * 100 / 9
            int radarValue = (score - 3) * 100 / 9;

            dimItems.add(new DimensionItem(dimNames[i], chosen, score, opposite));
            radarItems.add(new RadarItem(dimAbbrs[i], radarValue));
        }

        // ---------- 第三步：根据四位字母查找人格类型描述 ----------
        String nptiType = typeBuilder.toString();  // 例如 "INTJ"
        String[] personalityInfo = PERSONALITY_DATA.getOrDefault(nptiType,
            new String[]{"探索者型人格", "你是一个独特而复杂的人，无法被简单定义。继续保持你的独特性！"});

        // ---------- 第四步：组装返回结果 ----------
        NptiResponse res = new NptiResponse();
        res.setNptiType(nptiType);                 // 如 "INTJ"
        res.setTitle(personalityInfo[0]);           // 如 "建筑师型人格"
        res.setDescription(personalityInfo[1]);     // 详细描述
        res.setDimensions(dimItems);                // 四个维度的分数详情
        res.setRadarData(radarItems);               // 雷达图数据

        return res;
    }
}
