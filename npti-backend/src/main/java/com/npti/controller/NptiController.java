package com.npti.controller;

import com.npti.dto.NptiRequest;
import com.npti.dto.NptiResponse;
import com.npti.dto.Result;
import com.npti.service.NptiService;
import org.springframework.beans.factory.annotation.Autowired;
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
 * @CrossOrigin 是跨域注解（如果前端单独跑需要这个）
 * 但我们在 CorsConfig.java 里统一配了全局跨域，所以这里不写也行
 */
@RestController
@RequestMapping("/api/test")
public class NptiController {

    // @Autowired：让 Spring 自动帮我们创建 NptiService 的实例
    // 不需要自己 new，直接用就行
    @Autowired
    private NptiService nptiService;

    /**
     * 获取题目列表
     * 
     * 前端调用：GET http://localhost:8080/api/test/questions
     * 返回格式：Result<List<题目>>
     * 每道题包含：id(题号) / text(题目文字) / options(四个选项)
     */
    @GetMapping("/questions")
    public Result<List<Map<String, Object>>> getQuestions() {
        // 从 Service 层获取所有题目
        List<Map<String, Object>> questions = nptiService.getQuestions();
        // 用统一格式包装后返回
        return Result.success(questions);
    }

    /**
     * 提交答案并获取测试结果
     * 
     * 前端调用：POST http://localhost:8080/api/test/submit
     * 请求体：{ "answers": ["A", "B", "A", ...] }（12 个答案）
     * 返回格式：Result<NptiResponse>
     * 包含：人格类型 / 标题 / 描述 / 维度得分 / 雷达图数据
     */
    @PostMapping("/submit")
    public Result<NptiResponse> submitAnswers(@RequestBody NptiRequest request) {
        // @RequestBody：自动把前端传来的 JSON 解析成 NptiRequest 对象
        // 调用 Service 层的算分逻辑
        NptiResponse response = nptiService.calculateResult(request.getAnswers());
        return Result.success(response);
    }
}
