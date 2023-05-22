import os

from db.player import upsert_player, update_rating

from utils.logger import log_setup

from messages.rating_response import rating_embed
import discord
from discord import app_commands, Member

_log = log_setup(__name__)


def command_rating(bot):
    @app_commands.guild_only()
    @bot.tree.command(name='rating')
    async def rating(
            interaction: discord.Interaction,
            user: discord.Member = None
    ):
        """Returns the rating of a player

        :param interaction:
        :param user:
        :return:
        """
        _log.info("Rating Command Received")

        selection = interaction.user
        if user:
            selection = user

        player = upsert_player(selection, interaction.guild.id)
        if not player.get('rating', None):
            update_rating(selection, interaction.guild.id, 1000)
            player['rating'] = 1000

        if player:
            await interaction.response.send_message(
                embed=rating_embed(
                    selection,
                    player.get('rating')
                )
            )
        else:
            await interaction.response.send_message(f'Failed to retrieve player')

