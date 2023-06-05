from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse


def create_app() -> FastAPI:
    app = FastAPI(
        title="Search service",
        description="API: Search service for the nearest trucks for the transportation of goods.",
        openapi_url="/openapi.json",
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def validation_exception_handler(request, err):
        base_error_message = f"Failed to execute: {request.method}: {request.url}"
        return JSONResponse(
            status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
        )

    @app.get("/health")
    def health() -> str:
        return "ok"

    from src.cargo.routers import router as router_cargo
    from src.car.routers import router as router_car

    app.include_router(router_cargo)
    app.include_router(router_car)

    return app
