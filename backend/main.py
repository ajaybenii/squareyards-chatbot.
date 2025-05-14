from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost",
        "https://squareyards-frontend.onrender.com",
        "https://www.squareyards.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
print(f"MONGODB_URI: {MONGODB_URI}")  # Debug log

# MongoDB Connection
MONGODB_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
print(f"MONGODB_URI: {MONGODB_URI}")  # Debug log

try:
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi("1"),
        tls=True,
        tlsAllowInvalidCertificates=True,  # Temporarily disable certificate validation
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        maxPoolSize=5,
        minPoolSize=1,
        maxIdleTimeMS=10000,
        retryWrites=True,
        retryReads=True
    )
    # Test the connection
    client.server_info()  # This will raise an error if the connection fails
    print("MongoDB connection established.")
    db = client["squareyards"]
    collection = db["property_listings"]
except Exception as e:
    print("MongoDB connection failed:", str(e))
    raise Exception(f"MongoDB connection failed: {str(e)}")

# Pydantic model for request validation
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
        print("Received request:", listing_data)
        print("Inserted document ID:", result.inserted_id)
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        print("Error inserting document:", str(e))
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

@app.get("/debug-ssl")
def debug_ssl():
    import ssl
    import socket
    context = ssl.create_default_context()
    try:
        with socket.create_connection(("ac-ydqinoe-shard-00-00.vwdyi9p.mongodb.net", 27017)) as sock:
            with context.wrap_socket(sock, server_hostname="ac-ydqinoe-shard-00-00.vwdyi9p.mongodb.net") as ssock:
                return {"status": "SSL connection successful", "tls_version": ssock.version()}
    except Exception as e:
        return {"status": "SSL connection failed", "error": str(e)}