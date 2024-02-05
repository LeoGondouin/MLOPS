from fastapi import FastAPI,Request
from pymongo import MongoClient

client = MongoClient('mongo', 27017)
db = client.test_database
collection = db.test_collection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/fruits")
async def fruits():
    return {"fruits": list(collection.find({}, {"_id": False}))}

@app.post("/add/fruit")
async def add_fruit(data: dict):
    fruits = data["fruits"]
    result = collection.insert_many([{"fruit": fruit} for fruit in fruits])

    return result.acknowledged,list(collection.find({}, {"_id": False}))

@app.delete("/flush/fruits")
def flushFruits():
    result = collection.delete_many({})
    return result.acknowledged