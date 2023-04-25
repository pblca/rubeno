from datetime import datetime
from typing import Union, Optional

import discord
import shortuuid
from pymongo.collection import ReturnDocument

from db.database_config import db
from utils.logger import log_setup

_log = log_setup(__name__)


def upsert_player(user: discord.Member, guild_id) -> Optional[dict]:
    content = {
        'ts': datetime.utcnow().isoformat(),
        'guild': guild_id,
        'd_id': user.id,
    }

    try:
        r = db.col['player'].find_one_and_update(
            {
                'd_id': user.id,
                'guild': guild_id
            },
            {'$set': content},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
    except Exception as e:
        _log.error(e)
        return None
    else:
        _log.info(f'Recorded Player: {r["d_id"]} in {r["guild"]}')
        return r


def update_rating(user: discord.Member, guild_id, rating) -> Optional[dict]:
    content = {
        'rating': rating
    }

    try:
        r = db.col['player'].update_one({'d_id': user.id, 'guild': guild_id}, {'$set': content}, upsert=True)
    except Exception as e:
        _log.error(e)
        return None
    else:
        _log.info(f'Recorded Rating: {user.id} : {rating}')
        return r.raw_result
