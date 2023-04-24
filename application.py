import os
from dotenv import load_dotenv
from datetime import datetime
from utils.db import db
from utils.logger import log_setup
import shortuuid
import discord
from discord import app_commands
from discord.utils import get

_log = log_setup(__name__)
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
bot_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=bot_client)


@bot_client.event
async def on_ready():
    _log.info(f'Logged on as {bot_client.user}!')
    db.ping()

    await tree.sync(guild=discord.Object(id=os.getenv('TEST_GUILD')))
    _log.info('Synced Commands')


@app_commands.guild_only()
@tree.command(name='match', guild=discord.Object(id=os.getenv('TEST_GUILD')))
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

    def determine_winner(p1_wins, p2_wins):
        if p1_wins > p2_wins:
            return one.id
        elif p1_wins == p2_wins:
            return 'draw'
        else:
            return two.id

    content = {
        "uuid": f'm.{shortuuid.random(length=8)}',
        "ts": datetime.utcnow().isoformat(),
        "guild": interaction.guild.id,
        "players": [one.id, two.id],
        "result": [one_wins, two_wins],
        "winner": determine_winner(one_wins, two_wins)
    }

    try:
        db.col['match'].insert_one(content)
    except Exception as e:
        await interaction.response.send_message(f'Failed to add match')
        _log.error(e)
        raise e

    _log.info(f'Added Match: {content["uuid"]}')
    await interaction.response.send_message(f'Winner: {one.mention} Match ID: {content["uuid"]}')


bot_client.run(os.getenv('BOT_KEY'))
