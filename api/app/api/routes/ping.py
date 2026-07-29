from fastapi import APIRouter, Depends

from app.api.deps import get_ping_service
from app.schemas.ping import PingRequest, PingResponse
from app.services.ping_service import PingService

router = APIRouter()


@router.post("/ping", response_model=PingResponse)
async def ping(body: PingRequest, service: PingService = Depends(get_ping_service)) -> PingResponse:
    result = await service.record(body.message)
    return PingResponse(id=result.id, message=result.message, reply=result.reply)
