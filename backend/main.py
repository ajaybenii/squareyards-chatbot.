from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://squareyards-frontend.onrender.com","https://squareyards-chatbot-1.onrender.com"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Async MongoDB connection using Motor
mongo_uri = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(mongo_uri)
db = client["squareyards"]
collection = db["property_listings"]

# Pydantic model
class PropertyData(BaseModel):
    userType: str
    listingType: str
    city: str
    name: str
    number: str

# Submit route
@app.post("/submit")
async def submit(data: PropertyData):
    try:
        data_dict = data.dict()
        data_dict["created_at"] = datetime.utcnow().isoformat()
        await collection.insert_one(data_dict)
        return {"status": "success", "message": "Data submitted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Optional: DB ping endpoint
@app.get("/pingdb")
async def ping_db():
    try:
        await db.command("ping")
        return {"message": "MongoDB connection is working ✅"}
    except Exception as e:
        return {"message": f"DB ping failed: {str(e)}"}
