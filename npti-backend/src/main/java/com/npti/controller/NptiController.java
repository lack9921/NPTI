package com.npti.controller;

import com.npti.dto.NptiRequest;
import com.npti.dto.NptiResponse;
import com.npti.dto.Result;
import com.npti.service.NptiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/test")
public class NptiController {

    @Autowired
    private NptiService nptiService;

    @GetMapping("/questions")
    public Result<List<Map<String, Object>>> getQuestions() {
        return Result.success(nptiService.getQuestions());
    }

    @PostMapping("/submit")
    public Result<NptiResponse> submitAnswers(@RequestBody NptiRequest request) {
        NptiResponse response = nptiService.calculateResult(request.getAnswers());
        return Result.success(response);
    }
}
