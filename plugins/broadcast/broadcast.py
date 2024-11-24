from bot import db

usersdb = db.users

async def is_served_user(user_id: int) -> bool:
    user = usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def get_served_userss():
    user_docs = usersdb.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['user_id'])
    return user_ids

async def add_served_user(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    return usersdb.insert_one({"user_id": user_id})
