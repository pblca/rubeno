from datetime import datetime
from typing import Union, Optional

import discord
import shortuuid

from db.database_config import db
from utils.logger import log_setup

_log = log_setup(__name__)


def insert_match(
        interaction: discord.Interaction,
        placement: tuple,
        one: discord.Member,
        two: discord.Member,
        one_wins: int,
        two_wins: int
) -> Optional[dict]:
    content = {
        "uuid": f'm.{shortuuid.random(length=8)}',
        "ts": datetime.utcnow().isoformat(),
        "guild": interaction.guild.id,
        "players": [one.id, two.id],
        "result": [one_wins, two_wins],
        "winner": placement[0][0].mention if not placement[2] else 'draw'
    }

    try:
        db.col['match'].insert_one(content)
    except Exception as e:
        _log.error(e)
        return None
    else:
        _log.info(f'Added Match: {content["uuid"]}')
        return content


