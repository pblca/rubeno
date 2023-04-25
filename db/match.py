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
        ratings: tuple
) -> Optional[dict]:
    content = {
        'uuid': f'm.{shortuuid.random(length=8)}',
        'ts': datetime.utcnow().isoformat(),
        'guild': interaction.guild.id,
        'players': [placement[0][0].id, placement[1][0].id],
        'ratings': [{
            'id': placement[0][0].id,
            'rating': ratings[0][0],
            'change': ratings[0][1],
            'result': ratings[0][0] + ratings[0][1]
        }, {
            'id': placement[1][0].id,
            'rating': ratings[1][0],
            'change': ratings[1][1],
            'result': ratings[1][0] + ratings[0][1]
        }],
        'result': [placement[0][1], placement[1][1]],
        'winner': placement[0][0].mention if not placement[2] else 'draw'
    }

    try:
        db.col['match'].insert_one(content)
    except Exception as e:
        _log.error(e)
        return None
    else:
        _log.info(f'Added Match: {content["uuid"]}')
        return content


