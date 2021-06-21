import logging
from config import CONFIG
from personality_engine import user_conversation
from telegram.ext import Updater, MessageHandler, Filters
from time import sleep

logger = logging.getLogger("corpus.bridges.telegram")

updater = Updater(token=CONFIG["telegram"]["bot_token"], use_context=True)
dispatcher = updater.dispatcher

ALLOWED_USER_ID = int(CONFIG["telegram"]["user_id"])

def handle_text_message(update, context):
    msg = update.message
    if ALLOWED_USER_ID != msg.from_user.id: return

    txt = msg.text
    responses = user_conversation(txt)

    while len(responses) > 0:
        data = responses.pop(0)
        updater.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
        if data[0] > 0: sleep(data[0])
        update.message.reply_text(data[1])

text_handler = MessageHandler(Filters.text, handle_text_message)
dispatcher.add_handler(text_handler)

updater.start_polling()

logger.info("Telegram bridge ready.")

updater.idle()