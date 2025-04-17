from enum import Enum


class HttpCode(str, Enum):
    SUCCESS = "success"  # 成功
    FAIL = "fail"  # 失败
    NOT_FOUND = "not_found"  # 未找到
    UNAUTHORIZED = "unauthorized"  # 未授权
    FORBIDDEN = "forbidden"  # 禁止访问
    VALIDATION_ERROR = "validation_error"  # 验证错误
