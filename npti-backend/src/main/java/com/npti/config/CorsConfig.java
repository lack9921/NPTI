package com.npti.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

/**
 * 跨域配置
 * 
 * 前端（localhost:3000）调用后端（localhost:8080）时，
 * 浏览器会阻止跨域请求。这个配置放行所有来源，
 * 让前后端可以正常通信。
 * 
 * 前端 Vite 开发时也配了代理（/api → 8080），
 * 所以一般情况下不会触发跨域问题，
 * 但加了保险，防止特殊情况报错。
 */
@Configuration
public class CorsConfig {

    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.addAllowedOriginPattern("*");     // 允许所有域名访问
        config.addAllowedHeader("*");             // 允许所有请求头
        config.addAllowedMethod("*");             // 允许所有请求方法（GET/POST/PUT等）
        config.setAllowCredentials(true);          // 允许携带 Cookie

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);  // 对所有接口生效
        return new CorsFilter(source);
    }
}
