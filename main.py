from fastapi import FastAPI, Request


app = FastAPI()

@app.post("/pregnancy")
async def pregnancyLense(request: Request):
    return request.body()

@app.get("/pregnancy")
async def welcomeMessage():
    return {"advice": "Welcome to the pregnancy lense!"}