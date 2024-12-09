from pyrogram import Client, filters
from pyrogram.types import Message

# Create your bot instance
app = Client("my_bot")

# /ban command
@app.on_message(filters.command("ban") & filters.group)
async def ban_member(client: Client, message: Message):
    # Check if the user is an admin
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if not chat_member.can_restrict_members:
        await message.reply("You need to be an admin with permission to restrict members to use this command.")
        return

    # Ensure the command is a reply
    if not message.reply_to_message:
        await message.reply("You need to reply to a user's message to ban them.")
        return

    # Get the user to ban
    user_to_ban = message.reply_to_message.from_user

    try:
        # Ban the user
        await client.kick_chat_member(message.chat.id, user_to_ban.id)
        await message.reply(f"Banned {user_to_ban.mention} successfully!")
    except Exception as e:
        await message.reply(f"Failed to ban {user_to_ban.mention}. Error: {str(e)}")

# Run the bot
app.run()
