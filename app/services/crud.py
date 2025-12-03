from bson import ObjectId

def normalize_id(doc):
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc

async def insert_document(collection, data: dict):
    result = await collection.insert_one(data)
    return str(result.inserted_id)

async def find_documents(collection, query={}, limit=10):
    cursor = collection.find(query).limit(limit)
    docs = [normalize_id(doc) async for doc in cursor]
    return docs

async def find_one(collection, query):
    doc = await collection.find_one(query)
    return normalize_id(doc)

async def update_document(collection, query, update):
    await collection.update_one(query, {"$set": update})
