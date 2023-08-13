from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

# Constants
class Constants:
    Floor00 = "Floor00"
    Floor01 = "Floor01"
    Floor02 = "Floor02"
    Floor03 = "Floor03"
    TOPIC = "TOPIC"
    ALL_FLOORS = [Floor00, Floor01, Floor02, Floor03]

# FastAPI app initialization
app = FastAPI()

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

# MongoDB connection setup
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)
db = client.MIK_Database
collection = db.MIK_Collection

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/get_floor/")
async def get_floor(floor: str):
    # Validate floor manually
    if floor not in Constants.ALL_FLOORS:
        raise HTTPException(status_code=400, detail=f"Floor should be one of {', '.join(Constants.ALL_FLOORS)}")

    cursor = collection.find({Constants.TOPIC: {"$regex": f"^{floor}/"}})
    floor_data = list(cursor)
    for doc in floor_data:
        doc["_id"] = str(doc["_id"])  # Convert ObjectIDs to strings for JSON serialization

    return {"data": floor_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
