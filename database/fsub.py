from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import *

async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  # Your channel ID
    user_id = message.from_user.id
    try:
        # Check if user is a member of the required channel
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        # Generate the channel invite link
        channel_link = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("🔔 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=channel_link)

        # Display a message encouraging the user to join
        keyboard = [[join_button]]
        await message.reply(
            f"<b>👋 ʜᴇʟʟᴏ {message.from_user.mention()}, Welcome!</b>\n\n"
            "ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ, ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ.\n "
            "ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴀɴᴅ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛɪɴᴜᴇ ᴜsɪɴɢ ᴍᴇ 😊\n\n",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    else:
        return True
