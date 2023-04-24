from dotenv import load_dotenv

from bot.bot_factory import RubenoBot
from utils.logger import log_setup

_log = log_setup(__name__)
load_dotenv()

bot = RubenoBot().setup()
bot.client.run(bot.key)
