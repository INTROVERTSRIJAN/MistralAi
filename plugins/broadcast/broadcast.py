from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import asyncio
import os

# Access environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URI = os.getenv("MONGO_URI")

# Check if environment variables are loaded correctly
if not BOT_TOKEN or not OWNER_ID or not MONGO_URI:
    print("Error: Make sure BOT_TOKEN, OWNER_ID, and MONGO_URI are set as environment variables!")
    exit(1)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_bot"]
users_collection = db["users"]  # Collection to store user IDs

# Initialize the bot
app = Client("broadcast_bot", bot_token=BOT_TOKEN)


# Save user ID when the bot starts
@app.on_message(filters.command("start"))
async def save_user(client: Client, message: Message):
    user_id = message.from_user.id
    # Check if user already exists in the database
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})
        print(f"New user added: {user_id}")
    await message.reply("👋🏻☺️❤️")


# Broadcast message (restricted to bot owner)
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_message(client: Client, message: Message):
    # Get the message to broadcast (must be a reply)
    broadcast_text = message.reply_to_message.text or message.reply_to_message.caption
    if not broadcast_text:
        await message.reply("Error: The message to broadcast must contain text or a caption.")
        return

    # Fetch all user IDs from the database
    all_users = users_collection.find()
    user_ids = [user["user_id"] for user in all_users]

    sent, failed = 0, 0

    # Notify the owner that the broadcast is starting
    await message.reply("Broadcast is running...")

    for user_id in user_ids:
        try:
            await client.send_message(chat_id=user_id, text=broadcast_text)
            sent += 1
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
            failed += 1
        await asyncio.sleep(0.1)  # Optional: avoid hitting Telegram rate limits

    # Notify the owner about the results
    await client.send_message(
        chat_id=OWNER_ID,
        text=(
            f"Broadcast completed!\n\n"
            f"**Successfully Sent:** {sent}\n"
            f"**Failed to Send:** {failed}"
        )
    )


if __name__ == "__main__":
    app.run()
  
