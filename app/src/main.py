import uvicorn
from fastapi import FastAPI

from src.cargo.routers import router as router_cargo
from src.car.routers import router as router_car

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


app.include_router(router_cargo)
app.include_router(router_car)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
