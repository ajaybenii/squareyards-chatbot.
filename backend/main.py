from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to the frontend URL after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["squareyards"]
collection = db["property_listings"]

class PropertyData(BaseModel):
    userType: str
    listingType: str
    city: str
    name: str
    number: str

@app.post("/submit")
async def submit(data: PropertyData):
    try:
        data_dict = data.dict()
        data_dict["created_at"] = datetime.utcnow().isoformat()
        collection.insert_one(data_dict)
        return {"status": "success", "message": "Data submitted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}