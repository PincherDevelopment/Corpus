import logging
from config import CONFIG
from personality_engine import user_conversation
from time import sleep
import discord

logger = logging.getLogger("corpus.bridges.discord")

ALLOWED_USER_ID = int(CONFIG["discord"]["user_id"])

class BotClient(discord.Client):
    async def on_ready(self):
        logger.info("Discord bridge ready. (%s)" % (self.user))

    async def on_message(self, msg):
        if msg.author.id != ALLOWED_USER_ID: return
        if not msg.content: return

        txt = msg.content
        responses = user_conversation(txt)

        while len(responses) > 0:
            data = responses.pop(0)
            await msg.channel.trigger_typing()
            if data[0] > 0: sleep(data[0])
            await msg.reply(data[1])

logger.info("Discord bridge starting.")

client = BotClient()
client.run(CONFIG["discord"]["bot_token"])