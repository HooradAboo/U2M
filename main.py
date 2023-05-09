'''
    pip install uvicorn
    uvicorn main:app --reload --host 0.0.0.0
    lsof -i :8000
    kill -9 
'''
from fastapi import Request, FastAPI
from pymongo import MongoClient
from  json import loads

app = FastAPI()


# Connect to MongoDB
client = MongoClient("mongodb+srv://hoorad:h8rad@cluster0.qm6fhqa.mongodb.net/?retryWrites=true&w=majority")  # Replace <mongo-db-url> with your MongoDB connection URL
db = client["U2M"]  # Replace "mydatabase" with the name of your MongoDB database
collection = db["sensor"]  # Replace "mycollection" with the name of your MongoDB collection

@app.post("/{pid}")
async def get_body(pid: str, request: Request):
    if request.body:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8")

        body_dict = {'participantId': pid}
        body_dict.update(loads(body_str))

        # Save the data to MongoDB
        collection.insert_one(body_dict)

        return body_str
    else:
        return "No request body found"