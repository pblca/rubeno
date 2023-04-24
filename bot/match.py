import os
from datetime import datetime

from utils.db import db
from utils.logger import log_setup
from messages.match_response import match_result_embed
import shortuuid
import discord
from discord import app_commands, Member
from discord.utils import get

_log = log_setup(__name__)


def command_match(bot):
    @app_commands.guild_only()
    @bot.tree.command(name='match', guild=discord.Object(id=os.getenv('TEST_GUILD')))
    async def match_log(
            interaction: discord.Interaction,
            one: discord.Member,
            one_wins: int,
            two: discord.Member,
            two_wins: int):
        """Log the results of a match

        :param interaction:
        :param one: Player 1
        :param one_wins: Player 1 Win Count
        :param two: Player 2
        :param two_wins: Player 2 Win Count
        """

        def determine_placement(p1_wins, p2_wins) -> ((Member, int), (Member, int), bool):
            if p1_wins == p2_wins:
                return (one, p1_wins), (two, p2_wins), True
            elif p1_wins > p2_wins:
                return (one, p1_wins), (two, p2_wins), False
            else:
                return (two, p2_wins), (one, p1_wins), False

        placement = determine_placement(one_wins, two_wins)
        content = {
            "uuid": f'm.{shortuuid.random(length=8)}',
            "ts": datetime.utcnow().isoformat(),
            "guild": interaction.guild.id,
            "players": [one.id, two.id],
            "result": [one_wins, two_wins],
            "winner": placement[0][0].mention if not placement[2] else 'draw'
        }

        # TODO: ELO UPDATE

        try:
            db.col['match'].insert_one(content)
        except Exception as e:
            await interaction.response.send_message(f'Failed to add match')
            _log.error(e)
            raise e

        _log.info(f'Added Match: {content["uuid"]}')

        await interaction.response.send_message(embed=match_result_embed(placement, content["uuid"]))