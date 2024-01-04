from dotenv import load_dotenv

load_dotenv()


import os

from bot import WakscordBot

bot = WakscordBot()

bot.run(os.getenv("BOT_TOKEN") or "")
