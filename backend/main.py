from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from dotenv import load_dotenv
from app.core.db import get_db
import uvicorn
from app.routers.user import router as user_router

load_dotenv()

# INCLUDE ROUTERS


app = FastAPI()


@app.get("/")
async def home(db: AsyncIOMotorDatabase = Depends(get_db)):

    collections = await db.list_collection_names()

    print(collections)

    return {"message": True}


app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=8000, reload=True)
