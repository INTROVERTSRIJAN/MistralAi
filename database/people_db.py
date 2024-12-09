#srijan

from info import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# Initialize MongoDB connection
mongo = MongoCli(MONGO_URL)
db = mongo.people  # Database name
collection = db.people  # Collection name

async def get_people():
    """
    Retrieve all people from the collection where 'person' field exists and is greater than 0.
    """
    people_list = []
    async for person in collection.find({"person": {"$gt": 0}}):
        people_list.append(person['person'])
    return people_list

async def get_person(person):
    """
    Check if a person exists in the collection.
    """
    return await collection.find_one({"person": person}) is not None

async def add_person(person):
    """
    Add a new person to the collection if they don't already exist.
    """
    if not await get_person(person):
        await collection.insert_one({"person": person})

async def del_person(person):
    """
    Delete a person from the collection if they exist.
    """
    if await get_person(person):
        await collection.delete_one({"person": person})
