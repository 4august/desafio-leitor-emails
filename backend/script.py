from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from controller.upload_file_controller import router as upload_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def init():
    return {"status": "ok"}

app.include_router(upload_router)

if __name__ == "__main__":
    uvicorn.run("script:app", host="127.0.0.1", port=8000, reload=True)
