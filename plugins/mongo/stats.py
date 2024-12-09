#devggn

from bot import Bot
from pyrogram import filters
from info import OWNER_ID
from database.people_db import get_people, add_person, get_person  # Updated imports to match new naming

@Bot.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            person_in_db = await get_person(message.from_user.id)  # Changed `get_user` to `get_person`
            if not person_in_db:
                await add_person(message.from_user.id)  # Changed `add_user` to `add_person`
    except:
        pass

@Bot.on_message(filters.command("stats"))
async def stats(client, message):
    people_count = len(await get_people())  # Changed `get_users` to `get_people`
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total People** : {people_count}

**Subscribe to @OriginalSrijan**
""")
