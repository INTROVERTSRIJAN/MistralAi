#srijan

from info import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# Initialize MongoDB connection
mongo = MongoCli(MONGO_URL)
db = mongo.people  # Database remains the same, collection is now 'people'

async def get_people():
    """
    Retrieve all people from the collection where 'person' field exists and is greater than 0.
    """
    people_list = []
    async for person in db.find({"person": {"$gt": 0}}):
        people_list.append(person['person'])
    return people_list

async def get_person(person):
    """
    Check if a person exists in the collection.
    """
    people = await get_people()
    return person in people

async def add_person(person):
    """
    Add a new person to the collection if they don't already exist.
    """
    people = await get_people()
    if person in people:
        return
    else:
        await db.insert_one({"person": person})

async def del_person(person):
    """
    Delete a person from the collection if they exist.
    """
    people = await get_people()
    if person not in people:
        return
    else:
        await db.delete_one({"person": person})
