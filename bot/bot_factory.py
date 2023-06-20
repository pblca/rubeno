import os

from bot.events import register_events
from bot.match import command_match
from bot.rating import command_rating
from bot.leaderboard import command_leaderboard
from db.database_config import db
from db.player import get_leaderboard
from utils.logger import log_setup
import discord
from discord import app_commands

_log = log_setup(__name__)

"""
This class creates a bot instance with associated data.
We create a singleton of this in the app startup.

Its likely the bot object itself will not require 
much access after this instantiation.
"""


class RubenoBot:
    def __init__(self, db):
        # Initialize the bot with the secret key obtained from an environment variable.
        self.key = os.getenv("BOT_KEY")

        self.tree = None
        self.client = None
        self.intents = None
        # Store the instance of Database received as an argument during the initialization.
        self.db = db

    def setup(self):
        # Create an instance of discord.Intents and enable the required ones.
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        # Initialize the discord client with the specified intents.
        self.client = discord.Client(intents=self.intents, )
        # Initialize the command tree for the bot.
        self.tree = app_commands.CommandTree(client=self.client)
        
        # Register Commands and Events Here.
        register_events(self)
        command_match(self)
        command_rating(self)
        command_leaderboard(self)

        # Log the available commands.
        _log.info(f'Commands available: {list(self.tree._global_commands.keys())}')

        return self
