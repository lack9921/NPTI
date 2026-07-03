package com.npti.dto;

/**
 * 统一返回结果类
 * 
 * 后端所有接口都返回这个格式，前端统一解析。
 * 
 * 返回给前端的 JSON 格式：
 * {
 *   "code": 200,        ← 200 成功，500 出错
 *   "message": "success",
 *   "data": { ... }     ← 真正的数据放在这里
 * }
 *
 * @param <T> data 的类型（可能是 NptiResponse、List 等）
 */
public class Result<T> {
    private Integer code;    // 状态码：200=成功，500=服务器错误
    private String message;  // 提示信息
    private T data;          // 真正的返回数据，类型由调用处决定

    /** 成功时调用：return Result.success(你的数据); */
    public static <T> Result<T> success(T data) {
        Result<T> r = new Result<>();
        r.code = 200;
        r.message = "success";
        r.data = data;
        return r;
    }

    /** 失败时调用：return Result.error("原因"); */
    public static <T> Result<T> error(String message) {
        Result<T> r = new Result<>();
        r.code = 500;
        r.message = message;
        return r;
    }

    public Integer getCode() { return code; }
    public void setCode(Integer code) { this.code = code; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public T getData() { return data; }
    public void setData(T data) { this.data = data; }
}
