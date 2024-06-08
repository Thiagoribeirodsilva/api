import os
import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from . import rotas

load_dotenv()

uri = os.getenv('MONGO_URI')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere isso para permitir apenas origens confiáveis em produção
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
async def open_db() -> motor.motor_asyncio.AsyncIOMotorClient:
     app.state.mongodb = motor.motor_asyncio.AsyncIOMotorClient(uri)

async def close_db():
    app.state.mongodb.close()

app.include_router(rotas.router)
app.add_event_handler('startup', open_db)
app.add_event_handler('shutdown', close_db)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


