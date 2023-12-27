# Telegram Bot Template

This is a starting template to make a telegram bot.  
By having a simple and quick framework which can provide a good starting point to build almost any type of TG bot, I am hoping to make the creation of a custom Telegram bot simple and straight-forward. Ideally I would like to make this an accessible starting point even for those with little to no coding experience.

## Quickstart

Simply paste your bot token into the file TGBOTsecrets.py and then start updating bot.py with the logic you want.

The start function serves as a good template for any other functions you might want to call. You must add this to the main:

~~~
    unique_handler = CommandHandler('function_command', function_name)
    application.add_handler(unique_handler)
~~~

And there must be an internal or external function which it calls.


This repo includes requirements.txt :
~~~
pip install -r requirements.txt
~~~


## Future Development

The next step is to integrate simple authentication.
Other than this there are no development plans and is unlikely to be much changing in this repo as the purpose is to be a simple starting template for any TG bot. I am planning on creating forks of this project to create templates with more capabilities.
