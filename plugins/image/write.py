from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from bot import Bot
import requests


@Bot.on_message(filters.command("write"))
async def write(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(text="<b>ᴇxᴀᴍᴩʟᴇ :</b> /write YourName")
    else:
        text =message.text.split(None, 1)[1]
    m =await message.reply_text( "ᴡʀɪᴛɪɴɢ...")
    write = requests.get(f"https://apis.xditya.me/write?text={text}").url

    caption = f"""
🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
"""
    await m.delete()
    await message.reply_photo(photo=write,caption=caption)
