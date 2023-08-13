from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
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

# MongoDB connection setup
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)
db = client.MIK_Database
collection = db.MIK_Collection

# Models
class FloorQuery(BaseModel):
    floor: str

    @field_validator("floor")
    def valid_floor(cls, value):
        if value not in Constants.ALL_FLOORS:
            raise ValueError(f"Floor should be one of {', '.join(Constants.ALL_FLOORS)}")
        return value

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/get_floor/")
async def get_floor(payload: FloorQuery):
    cursor = collection.find({Constants.TOPIC: {"$regex": f"^{payload.floor}/"}})
    floor_data = list(cursor)
    for doc in floor_data:
        doc["_id"] = str(doc["_id"]["$oid"])  # Convert ObjectIDs to strings for JSON serialization
    return {"data": floor_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
