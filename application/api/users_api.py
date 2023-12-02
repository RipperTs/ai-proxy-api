from fastapi import APIRouter, Request

from application.common.vo import resultSuccess
from application.model.po.login_user_po import LoginUserPo
from application.model.po.register_user_po import RegisterUserPo
from application.model.po.update_password_po import UpdatePasswordPo
from application.service.users_sercice import create_user, login_for_access_token, do_update_password

router = APIRouter()


@router.post('/register-user')
async def register_user(data: RegisterUserPo):
    """
    注册用户
    :param data:
    :return:
    """
    result = await create_user(data)
    return resultSuccess(data=result)


@router.post('/login-user')
async def login_user(data: LoginUserPo):
    """
    登录用户
    :param data:
    :return:
    """
    result = await login_for_access_token(data.email, data.password)
    return resultSuccess(data=result)


@router.post('/update-password')
async def update_password(request: Request, data: UpdatePasswordPo):
    """
    修改密码
    :param data:
    :return:
    """
    result = await do_update_password(request.state.user_info['user_id'], data.password, data.re_password)
    return resultSuccess(data=result)
