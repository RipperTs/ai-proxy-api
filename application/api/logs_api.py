from fastapi import APIRouter

from application.service.logs_service import get_log_list
from application.common.vo import resultSuccess

router = APIRouter()


@router.get('/log-list')
async def log_list(page: int = 1, limit: int = 30):
    results, total_count = await get_log_list(page, limit)
    return resultSuccess(data={
        "list": results,
        "total_count": total_count
    })
