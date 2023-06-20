import os
import discord

from db.player import get_leaderboard
from messages.leaderboard_response import leaderboard_embed
from discord import app_commands
from utils.logger import log_setup

_log = log_setup(__name__)

def command_leaderboard(bot):
    @app_commands.guild_only()
    @bot.tree.command(name='leaderboard', description="Shows the highest rated players")
    async def leaderboard(interaction: discord.Interaction, count: int = 10):
        """Shows the top players and their elo based on the provided count

        :param interaction:
        :param count: The number of top players to display. Defaults to 10.
        """
        _log.info("Leaderboard Command Received")

        # The max() function ensures that at least 1 player is shown
        count = max(1, count)

        leaderboard_list = get_leaderboard(bot, limit=count)

        if leaderboard_list:
            # Here is where the change is. Pass the bot as the first argument.
            await interaction.response.send_message(
                embed = leaderboard_embed(leaderboard_list)
            )
        else:
            await interaction.response.send_message('No players found.')

