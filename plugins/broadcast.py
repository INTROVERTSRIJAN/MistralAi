from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

# Access the bot token and owner ID from environment variables (configured in Koyeb)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # Ensure this is set as an integer

# Initialize the bot
app = Client(
    "broadcast_bot",
    bot_token=BOT_TOKEN,
)

# Store user IDs in this list or fetch dynamically from your database
user_ids = []  # Replace with the list of user IDs you want to broadcast to

@app.on_message(filters.command("broadcast") & filters.user([OWNER_ID]))  # Restrict to OWNER_ID only
async def broadcast_message(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a message to broadcast. Example:\n`/broadcast Your message here`")
        return

    broadcast_text = message.text.split(" ", 1)[1]
    sent, failed = 0, 0

    await message.reply("Broadcast started. Please wait...")

    for user_id in user_ids:
        try:
            await client.send_message(chat_id=user_id, text=broadcast_text)
            sent += 1
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
            failed += 1
        await asyncio.sleep(0.1)  # Optional: avoid hitting rate limits

    await message.reply(f"Broadcast completed!\n\n**Sent:** {sent}\n**Failed:** {failed}")

if __name__ == "__main__":
    app.run()
