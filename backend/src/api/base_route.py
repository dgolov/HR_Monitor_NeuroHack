from fastapi import APIRouter
from ..settings import log

router = APIRouter()


@router.get("/health")
def health_check():
    log.info('healthcheck')
    return {"message": "Server is running"}
