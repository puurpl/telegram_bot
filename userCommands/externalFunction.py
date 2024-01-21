# This is an example of an external function that can be called from the main file.
from telegram import Update
from telegram.ext import ContextTypes


# To load ADMIN_ID from .env file #
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
ADMIN_ID = os.getenv('ADMIN_ID')
###################################


async def external_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text="This is an external function.")
    await context.bot.send_message(chat_id=ADMIN_ID, text="External function called by %s (User ID: %s)" % (update.effective_user.first_name, update.effective_user.id))
    return