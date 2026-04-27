import uvicorn
from fastapi import FastAPI
from api.router import router

app = FastAPI(title="StayEase AI Assistant")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to StayEase AI Assistant API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
