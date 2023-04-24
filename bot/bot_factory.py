import os

from bot.events import register_events
from bot.match import command_match
from utils.logger import log_setup
import discord
from discord import app_commands

_log = log_setup(__name__)

"""
This creates a bot instance with associated data.
We create a singleton of this in the app startup.

Its likely the bot object itself will not require 
much access after this instantiation.
"""


class RubenoBot:
    def __init__(self):
        self.key = os.getenv('BOT_KEY')
        self.tree = None
        self.client = None
        self.intents = None

    def setup(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents, )
        self.tree = app_commands.CommandTree(client=self.client)

        """
        Register Commands and Events Here
        
        New Commands should exist in individual files with their business logic
        Response content should exist in individual files under messages
        """
        register_events(self)
        command_match(self)

        return self
