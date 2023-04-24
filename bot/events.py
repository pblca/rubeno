import os
import discord

from db.database_config import db
from utils.logger import log_setup

_log = log_setup(__name__)

"""
Events dont seem crazy useful for a bot
So for now, we can stack them in 1 register call
"""


def register_events(bot):
    @bot.client.event
    async def on_ready():
        _log.info(f'Logged on as {bot.client.user}!')
        db.ping()

        await bot.tree.sync(guild=discord.Object(id=os.getenv('TEST_GUILD')))
        _log.info('Synced Commands')
