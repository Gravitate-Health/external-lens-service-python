from fastapi import FastAPI

app = FastAPI()

@app.post("/python/lense/pregnancy/")
async def pregnancyLense():
    return {"message": "just a placeholder"}

