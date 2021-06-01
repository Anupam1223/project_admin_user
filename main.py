from user import user
from task import task
from fastapi import FastAPI
import uvicorn


app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
