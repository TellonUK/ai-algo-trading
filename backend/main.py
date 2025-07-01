from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import historic, current, stream

app = FastAPI(title="Trading API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(historic.router, prefix="/historic", tags=["historic"])
app.include_router(current.router, prefix="/current", tags=["current"])
app.include_router(stream.router, prefix="/stream", tags=["stream"])

@app.get("/")
async def root():
    return {"message": "Trading API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)