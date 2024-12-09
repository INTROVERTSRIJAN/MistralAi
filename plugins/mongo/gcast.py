import asyncio
from pyrogram import filters
from info import OWNER_ID
from bot import Bot
from database.people_db import get_people  # Updated to match "people" collection

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await send_msg(user_id, message)  # Ensure recursive call awaits
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user ID invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {e}\n"

@Bot.on_message(filters.command("gcast") & filters.user(OWNER_ID))
async def broadcast(_, message):
    """
    Broadcasts a message to all users in the people collection.
    """
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast it.")
        return

    exmsg = await message.reply_text("Started broadcasting!")
    all_people = (await get_people()) or []  # Fetch all users from the people collection
    done_people = 0
    failed_people = 0

    for person in all_people:
        try:
            await send_msg(person, message.reply_to_message)
            done_people += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed_people += 1

    if failed_people == 0:
        await exmsg.edit_text(
            f"**Successfully Broadcasted ✅**\n\n**Message sent to** `{done_people}` **users.**"
        )
    else:
        await exmsg.edit_text(
            f"**Broadcast Completed ✅**\n\n**Message sent to** `{done_people}` **users.**\n"
            f"**Failed to send to** `{failed_people}` **users.**"
        )

@Bot.on_message(filters.command("announce") & filters.user(OWNER_ID))
async def announce(_, message):
    """
    Forwards a message to all users in the people collection.
    """
    if not message.reply_to_message:
        await message.reply_text("Reply to a post to broadcast it.")
        return

    to_send = message.reply_to_message.id
    people = await get_people() or []
    failed_people = 0
    successful_people = 0

    for person in people:
        try:
            await _.forward_messages(
                chat_id=int(person),
                from_chat_id=message.chat.id,
                message_ids=to_send
            )
            successful_people += 1
            await asyncio.sleep(1)
        except Exception:
            failed_people += 1

    if failed_people == 0:
        await message.reply_text(
            f"**Successfully Broadcasted ✅**\n\n**Message sent to** `{successful_people}` **users.**"
        )
    else:
        await message.reply_text(
            f"**Broadcast Completed ✅**\n\n**Message sent to** `{successful_people}` **users.**\n"
            f"**Failed to send to** `{failed_people}` **users.**"
        )
