from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from telegram.error import BadRequest
from telegram.utils.helpers import mention_html


def ban(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    # Check if the user is an admin
    member = chat.get_member(user.id)
    if not member.status in ["administrator", "creator"]:
        message.reply_text("Only admins can use this command.")
        return

    # Check if the command is used as a reply
    if not message.reply_to_message:
        message.reply_text("Reply to a user's message to ban them.")
        return

    target_user = message.reply_to_message.from_user

    try:
        chat.ban_member(target_user.id)
        message.reply_text(
            f"{mention_html(target_user.id, target_user.first_name)} has been banned.",
            parse_mode=ParseMode.HTML,
        )
    except BadRequest as e:
        message.reply_text(f"Failed to ban the user: {e.message}")


# Add the handler to your dispatcher
handler = CommandHandler("ban", ban)
dispatcher.add_handler(handler)
