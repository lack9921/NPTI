package com.npti.dto;

import java.util.List;

public class NptiResponse {
    private String nptiType;
    private String title;
    private String description;
    private List<DimensionItem> dimensions;
    private List<RadarItem> radarData;

    public static class DimensionItem {
        private String name;
        private String abbr;
        private int score;
        private String opposite;

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

    public static class RadarItem {
        private String name;
        private int value;

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
