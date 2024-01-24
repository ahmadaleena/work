from fastapi import FastAPI, APIRouter
from views import router as views_router
import os


app = FastAPI()
app.include_router(views_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
