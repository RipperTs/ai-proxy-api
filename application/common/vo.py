'''
公共返回方法
'''

ERROR_CODE = 422
SUCCESS_CODE = 0


# 成功返回
def resultSuccess(data, msg='success', code=SUCCESS_CODE) -> dict:
    return {
        "code": code,
        "data": data,
        "msg": msg
    }


# 失败返回
def resultError(msg='error', code=ERROR_CODE) -> dict:
    return {
        "code": code,
        "data": [],
        "msg": msg
    }
