from dotenv import load_dotenv
from bot.bot_factory import RubenoBot
from db.database_config import Database   # Import the Database class
from utils.logger import log_setup, formatter

_log = log_setup(__name__)
load_dotenv()

# Create an instance of Database and setup the connection. This sets up the 
# connection to the MongoDB server using the details provided in the .env file.
db_instance = Database().setup()  

# Create an instance of RubenoBot, passing in the database instance as an argument.
# The setup() method is then called to initialize the bot, setting up intents and commands.
bot = RubenoBot(db_instance).setup()   

# Run the bot using the key obtained from the bot instance. A log formatter is also passed in.
bot.client.run(bot.key, log_formatter=formatter)



