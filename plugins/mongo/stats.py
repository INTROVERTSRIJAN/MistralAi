#devggn

from bot import Bot
from pyrogram import filters
from database.people_db import get_people, add_person, get_person

@Bot.on_message(group=10)
async def chat_watcher_func(_, message):
    """
    Adds the sender to the database if they're not already in it.
    """
    try:
        if message.from_user:
            person_in_db = await get_person(message.from_user.id)
            if not person_in_db:
                await add_person(message.from_user.id)
    except Exception as e:
        print(f"Error in chat_watcher_func: {e}")

@Bot.on_message(filters.command("stats"))
async def stats(client, message):
    """
    Sends stats about the bot's users.
    """
    try:
        people_count = len(await get_people())
        await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total People** : {people_count}

**Subscribe to @OriginalSrijan**
""")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
