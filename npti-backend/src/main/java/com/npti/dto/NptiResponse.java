package com.npti.dto;

import java.util.List;

/**
 * 后端计算完成后返回给前端的结果数据
 * 
 * JSON 示例：
 * {
 *   "nptiType": "INTJ",
 *   "title": "建筑师型人格",
 *   "description": "富有想象力、战略性、果断...",
 *   "dimensions": [           ← 四个维度的详细得分
 *     { "name": "精力来源", "abbr": "I", "score": 8, "opposite": "E" }
 *   ],
 *   "radarData": [            ← 给 ECharts 雷达图用的数据
 *     { "name": "I/E", "value": 56 }
 *   ]
 * }
 */
public class NptiResponse {
    private String nptiType;               // 四位字母：如 "INTJ"
    private String title;                  // 中文标题：如 "建筑师型人格"
    private String description;            // 详细的人格描述文字
    private List<DimensionItem> dimensions; // 四个维度的得分明细
    private List<RadarItem> radarData;     // 雷达图渲染数据

    /**
     * 某个维度的得分详情
     * 比如：精力来源 I=8分（对面是 E），表示偏内向
     */
    public static class DimensionItem {
        private String name;      // 维度中文名："精力来源"
        private String abbr;      // 得分高的一方："I"（内向）
        private int score;        // 该维度总分（3-12 分）
        private String opposite;  // 对立面简称："E"（外向）

        public DimensionItem(String name, String abbr, int score, String opposite) {
            this.name = name; this.abbr = abbr;
            this.score = score; this.opposite = opposite;
        }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getAbbr() { return abbr; }
        public void setAbbr(String abbr) { this.abbr = abbr; }
        public int getScore() { return score; }
        public void setScore(int score) { this.score = score; }
        public String getOpposite() { return opposite; }
        public void setOpposite(String opposite) { this.opposite = opposite; }
    }

    /**
     * 雷达图数据点
     * name: 维度缩写 "I/E"
     * value: 归一化后的 0-100 分数
     */
    public static class RadarItem {
        private String name;   // 维度标签："I/E"、"N/S" 等
        private int value;     // 得分（0-100），给 ECharts 渲染用

        public RadarItem(String name, int value) {
            this.name = name; this.value = value;
        }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public int getValue() { return value; }
        public void setValue(int value) { this.value = value; }
    }

    public String getNptiType() { return nptiType; }
    public void setNptiType(String nptiType) { this.nptiType = nptiType; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public List<DimensionItem> getDimensions() { return dimensions; }
    public void setDimensions(List<DimensionItem> dimensions) { this.dimensions = dimensions; }
    public List<RadarItem> getRadarData() { return radarData; }
    public void setRadarData(List<RadarItem> radarData) { this.radarData = radarData; }
}
