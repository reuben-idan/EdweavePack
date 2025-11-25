from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/auth/register")
async def register(user_data: dict):
    return {"message": "Registration endpoint working", "access_token": "test_token"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)