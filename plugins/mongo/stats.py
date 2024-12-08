#devggn

from bot import Bot
from pyrogram import filters
from info import OWNER_ID
from database.users_db import get_users, add_user, get_user




@Bot.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass


@Bot.on_message(filters.command("stats"))
async def stats(client, message):
    users = len(await get_users())
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}

**Subscribe to @OriginalSrijan**
""")
  
