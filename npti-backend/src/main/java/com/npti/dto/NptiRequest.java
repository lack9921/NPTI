package com.npti.dto;

import java.util.List;

/**
 * 前端提交答案时发送给后端的请求格式
 * 
 * JSON 示例：
 * {
 *   "answers": ["A", "B", "A", "C", "D", "A", "B", "A", "A", "C", "D", "B"]
 * }
 * 
 * answers 是长度为 12 的字符串数组，每个元素是 "A" / "B" / "C" / "D"
 * 分别对应第 1-12 题的选项
 */
public class NptiRequest {
    private List<String> answers;  // 12 个答案，顺序对应 12 道题

    public List<String> getAnswers() { return answers; }
    public void setAnswers(List<String> answers) { this.answers = answers; }
}
