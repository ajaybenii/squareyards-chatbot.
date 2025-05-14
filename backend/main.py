from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost", "https://squareyards-frontend.onrender.com", "https://www.squareyards.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
print(f"MONGODB_URI: {MONGODB_URI}")  # Debug log

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)  # 5-second timeout
    # client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=False)
    # Test the connection
    client.server_info()  # This will raise an error if the connection fails
    print("Connected databases:", client.list_database_names())
    db = client["squareyards"]
    collection = db["property_listings"]
    print("Inserting into Database:", db.name, "Collection:", collection.name)
except Exception as e:
    # print(f"Failed to connect to MongoDB: {str(e)}")
    raise Exception(f"MongoDB connection failed: {str(e)}")

class PropertyListing(BaseModel):
    userType: str
    listingType: str
    city: str
    name: str
    number: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/submit")
async def submit_listing(listing: PropertyListing):
    try:
        listing_data = listing.dict()
        listing_data["created_at"] = datetime.utcnow()
        result = collection.insert_one(listing_data)
        print("Received request:", listing_data)  # Debug log
        print("Inserted document ID:", result.inserted_id)
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

@app.get("/")
async def root():
    return {"message": "SquareYards Chatbot Backend"}