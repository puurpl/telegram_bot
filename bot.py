import logging, os 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, BaseHandler
from dotenv import load_dotenv, set_key

from functools import wraps

### External functions
from userCommands.externalFunction import external_function


###################################################################################################################
#Set logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

###################################################################################################################
# GLOBAL VARIABLES
# Load environment variables, with warning if missing (verbose)
load_dotenv(verbose=True)

TGBOTtoken = os.getenv('TGBOTtoken')
ADMIN_ID = os.getenv('ADMIN_ID')
AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS').split(',')

###################################################################################################################
def authorized_only(handler):
    @wraps(handler)
    async def wrapper(update, context):
        user_id = update.effective_user.id
        if str(user_id) in AUTHORIZED_USERS:
            return await handler(update, context)
        else:
            logging.warning("Unauthorized access to %s denied for %s (User ID: %s)", handler, update.effective_user.first_name, update.effective_user.id)
            await context.bot.send_message(chat_id=ADMIN_ID, text="Unauthorized message received from %s (User ID: %s): %s for %s" % (update.effective_user.first_name, update.effective_user.id, update.message.text, handler))
            await context.bot.send_message(chat_id=user_id, text="You are not authorized to use this function.")
    return wrapper
###
##### USE THIS DECORATOR TO RESTRICT ACCESS TO A FUNCTION TO AUTHORIZED USERS ONLY
##### CALL IT DIRECTLY FROM THE HANDLER
##### sample_handler = CommandHandler('command', authorized_only(sample_function))
###

def admin_only(handler):
    @wraps(handler)
    async def wrapper(update, context):
        user_id = update.effective_user.id
        if str(user_id) in ADMIN_ID:
            return await handler(update, context)
        else:
            logging.warning("Unauthorized ADMIN access to %s denied for %s (User ID: %s)", handler, update.effective_user.first_name, update.effective_user.id)
            await context.bot.send_message(chat_id=ADMIN_ID, text="Unauthorized ADMIN message received from %s (User ID: %s): %s for %s" % (update.effective_user.first_name, update.effective_user.id, update.message.text, handler))
            await context.bot.send_message(chat_id=user_id, text="You are not authorized to use this function.")
        return handler(update, context)
    return wrapper
###
##### USE THIS DECORATOR TO RESTRICT ACCESS TO A FUNCTION TO ADMIN ONLY
##### sample_handler = CommandHandler('command', admin_only(sample_function))
###
###################################################################################################################
# ADMIN COMMANDS

@admin_only
async def authorize_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AUTHORIZED_USERS
    if context.args == []:
        user_id_to_add = await context.bot(chat_id=update.effective_chat.id, text="Please send me the user ID of the user you want to authorize.")     
    user_id_to_add = context.args[0]
    if AUTHORIZED_USERS:
        AUTHORIZED_USERS.append(user_id_to_add)
        authorized_users_str = ",".join(authorized_users)
    else:
        AUTHORIZED_USERS = []
        AUTHORIZED_USERS.append(user_id_to_add)
        authorized_users_str = ",".join(authorized_users)
    # Update the AUTHORIZED_USERS variable in the .env file
    set_key(".env", "AUTHORIZED_USERS", authorized_users_str)
    logging.info("Dot_env: AUTHORIZED_USERS updated to %s", os.getenv('AUTHORIZED_USERS').split(','))
    await context.bot.send_message(chat_id=user_id_to_add, text="You are now authorized to use this bot.")
    await context.bot.send_message(chat_id=ADMIN_ID, text="User ID: %s is now authorized to use this bot." % user_id_to_add)

@admin_only
async def list_authorized_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AUTHORIZED_USERS
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await context.bot.send_message(chat_id=user_id, text="Authorized Users: %s" % AUTHORIZED_USERS)
# Later format this list returning names too, and allowing selection of users to action

###################################################################################################################

async def request_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=ADMIN_ID, text="User ID: %s is requesting access to this bot." % user_id)
    await context.bot.send_message(chat_id=user_id, text="Your request for access has been sent to the bot admin. Please wait for approval.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_handle = update.effective_user.username
    user_name = update.effective_user.first_name
    user_language = update.effective_user.language_code

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your user ID: {user_id} \nHandle: {user_handle} \nName: {user_name} \nLanguage: {user_language}")

#@authorized_only
async def hello_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a test message. Your user ID: %s is authorized." % update.effective_user.id)




###################################################################################################################
if __name__ == '__main__':
    application = ApplicationBuilder().token(TGBOTtoken).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    request_access_handler = CommandHandler('knockknock', request_access)
    application.add_handler(request_access_handler)

    whoami_handler = CommandHandler('whoami', whoami)
    application.add_handler(whoami_handler)

# ADMIN COMMANDS
    authorize_user_handler = CommandHandler('authorize', authorize_user)
    application.add_handler(authorize_user_handler)

#    users_handler = CommandHandler('users', list_authorized_users)
#    application.add_handler(users_handler)
    
# SAMPLE AND TEST COMMANDS
    helloWorld_handler = CommandHandler('hello', authorized_only(hello_world))
    application.add_handler(helloWorld_handler)

    externalFunction_handler = CommandHandler('external', authorized_only(external_function))
    application.add_handler(externalFunction_handler)

    application.run_polling()

