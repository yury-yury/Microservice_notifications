from fastapi import FastAPI, APIRouter

from handlers import router


app = FastAPI(title="Test task")

main_router = APIRouter()
main_router.include_router(router, prefix="", tags=["Notifications"])

app.include_router(main_router)
