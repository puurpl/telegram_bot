This is a starting template to make a telegram bot. Simply paste your bot token into the file TGBOTsecrets.py and then start updating bot.py with the logic you want.

The start function serves as a good template for any other functions you might want to call. You must add this to the main:

    unique_handler = CommandHandler('function_command', function_name)
    application.add_handler(unique_handler)

And there must be an internal or external function which it calls.


This repo includes requirements.txt :

pip install -r requirements.txt