# app/db.py
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv() 

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise Exception("MONGO_URL environment variable not set")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.krishimitra
