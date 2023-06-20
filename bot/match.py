import os

from db.match import insert_match
from db.player import upsert_player, update_rating

from utils.logger import log_setup
from utils.elo import calculate_match

from messages.match_response import match_result_embed
import discord
from discord import app_commands, Member

_log = log_setup(__name__)


def command_match(bot):
    @app_commands.guild_only()
    @bot.tree.command(name='match')
    async def match_log(
            interaction: discord.Interaction,
            one: discord.Member,
            one_wins: int,
            two: discord.Member,
            two_wins: int
    ):
        """Log the results of a match

        :param interaction:
        :param one: Player 1
        :param one_wins: Player 1 Win Count
        :param two: Player 2
        :param two_wins: Player 2 Win Count
        """
        _log.info("Match Command Received")

        # Check if the user invoking the command has the 'Serenader' role
        admin = discord.utils.get(interaction.guild.roles, name='Serenader')
        if admin not in interaction.user.roles:
            await interaction.response.send_message('You are not a Serenader')
            return

        def determine_placement(p1_wins, p2_wins) -> ((Member, int), (Member, int), bool):
            if p1_wins == p2_wins:
                return (one, p1_wins), (two, p2_wins), True
            elif p1_wins > p2_wins:
                return (one, p1_wins), (two, p2_wins), False
            else:
                return (two, p2_wins), (one, p1_wins), False

        placement = determine_placement(one_wins, two_wins)

        p1_obj = upsert_player(one, interaction.guild.id)
        p2_obj = upsert_player(two, interaction.guild.id)

        ratings = calculate_match(
            p1=(p1_obj['rating'] if p1_obj.get('rating', None) else 1000, placement[0][1]),
            p2=(p2_obj['rating'] if p2_obj.get('rating', None) else 1000, placement[1][1])
        )

        _log.info(f'Rating Update: {ratings}')

        insert = insert_match(interaction, placement, ratings)
        p1_update = update_rating(one, interaction.guild.id, ratings[0][0] + ratings[0][1])
        p2_update = update_rating(two, interaction.guild.id, ratings[1][0] + ratings[1][1])

        if insert and p1_update and p2_update:
            await interaction.response.send_message(embed=match_result_embed(placement, ratings, insert["uuid"]))
        else:
            await interaction.response.send_message(f'Failed to add match')




