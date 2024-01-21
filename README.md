# Telegram Bot Template

This is a starting template to make a telegram bot.  
By having a simple and quick framework which can provide a good starting point to build almost any type of TG bot, I am hoping to make the creation of a custom Telegram bot even simpler and more straight-forward than it currently is. 
Ideally I would like to make this an accessible starting point even for those with little to no coding experience.

## Quickstart

### Clone Git

Clone the git to the machine you want to host it on. In this case:
´´´
$ git clone https://github.com/puurpl/telegram_bot.git
´´´

### Setup Environment

If you are already familiar with running Python programs and setting up virtual environments then you can skip this section entirely and do things your preferred way.
Otherwise I recommend setting up a virtual environment for this project before runnint it. First make sure that Python is installed and available on your machine.
Then set up the virtual environment:

´´´
$ cd telegram_bot # Go to the project directory
$ python3 -m venv venv 
$ source venv/bin/activate # This works on my Mac
$ . venv/bin/activate # This is for some Linux distros without 'source'

$ pip install -r requirements.txt # Install the requirements
´´´

### Setup Credentials

Simply paste your bot token and your own user ID into the .env file and then start modifying the bot as you like. (If you don't know your user ID you can start the bot and use '/whoami' command, read the terminal output from trying to call a restricted function, or you can message '/start' to @useridinfobot)

### Create

The start or helloWorld functions serve as a good template for any other functions you might want to add. For each additional command you must add this to the main:

~~~
### Add to bot.py > main
    unique_handler = CommandHandler('function_command', function_name)
    application.add_handler(unique_handler)
~~~

And there must be an internal or external function which it calls.




## Future Development

There are no development plans. The purpose of this repo is to be a simple starting template for any TG bot. I am planning on creating forks of this project to create templates for various use cases.