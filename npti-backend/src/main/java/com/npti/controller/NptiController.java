package com.npti.controller;

import com.npti.dto.NptiRequest;
import com.npti.dto.NptiResponse;
import com.npti.dto.Result;
import com.npti.service.NptiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 测试系统的接口控制器
 * 
 * 前端（Vue）通过 HTTP 请求来调用这里的接口：
 * 
 * 1. GET  /api/test/questions  → 获取所有题目
 * 2. POST /api/test/submit     → 提交答案，获取测试结果
 *
 * 异常处理：
 * - 如果提交的答案数量不对，返回 400 错误
 * - 其他未捕获的异常由 Spring Boot 默认处理
 */
@RestController
@RequestMapping("/api/test")
public class NptiController {

    @Autowired
    private NptiService nptiService;

    /**
     * 获取题目列表
     * 
     * 前端调用：GET http://localhost:8080/api/test/questions
     * 
     * 返回格式：
     * {
     *   "code": 200,
     *   "message": "success",
     *   "data": [ { "id": 1, "text": "...", "options": [...] }, ... ]
     * }
     */
    @GetMapping("/questions")
    public Result<List<Map<String, Object>>> getQuestions() {
        try {
            List<Map<String, Object>> questions = nptiService.getQuestions();
            return Result.success(questions);
        } catch (Exception e) {
            // 捕获所有异常，返回 500 错误
            return Result.error("获取题目失败：" + e.getMessage());
        }
    }

    /**
     * 提交答案并获取测试结果
     * 
     * 前端调用：POST http://localhost:8080/api/test/submit
     * 
     * 请求体：
     * { "answers": ["A", "B", "A", "C", "D", "A", "B", "A", "A", "C", "D", "B"] }
     * 
     * 返回格式见 NptiResponse.java
     */
    @PostMapping("/submit")
    public Result<?> submitAnswers(@RequestBody NptiRequest request) {
        // 1. 检查答案数量
        List<String> answers = request.getAnswers();
        if (answers == null) {
            return Result.error("缺少答案数据");
        }
        if (answers.size() != 12) {
            return Result.error("需要 12 个答案，实际收到 " + answers.size() + " 个");
        }

        // 2. 检查每个答案是否合法（只能是 A/B/C/D）
        for (int i = 0; i < answers.size(); i++) {
            String ans = answers.get(i).toUpperCase();
            if (!List.of("A", "B", "C", "D").contains(ans)) {
                return Result.error("第 " + (i + 1) + " 题的答案不合法：" + answers.get(i) + "，只允许 A/B/C/D");
            }
        }

        // 3. 调用算分逻辑
        try {
            NptiResponse response = nptiService.calculateResult(answers);
            return Result.success(response);
        } catch (Exception e) {
            return Result.error("计算结果失败：" + e.getMessage());
        }
    }
}
