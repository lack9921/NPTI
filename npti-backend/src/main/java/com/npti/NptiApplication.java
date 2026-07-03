package com.npti;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * NPTI 后端入口
 * 启动后会在 http://localhost:8080 运行
 * 运行方式：在 npti-backend/ 目录下执行 mvn spring-boot:run
 */
@SpringBootApplication
public class NptiApplication {
    public static void main(String[] args) {
        SpringApplication.run(NptiApplication.class, args);
        System.out.println("🚀 NPTI 后端启动成功！访问 http://localhost:8080");
    }
}
