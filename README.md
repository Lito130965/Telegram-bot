# Telegram-bot
## This bot provides next features:
1. /all -             any member can to use this command to mention everyone from current chat, except users with ignore mode(4).
                      Members will tagged in a new message from bot by using emoji instead of @nickname.
                      Initial emoji is '🐜', it's means that every people who don't changed an emoji(2) for himself, will tagged by ant emoji.
   
2. /set_emoji -       with this command any people can to set or change him emoji. You need to send message with the command and emoji through a space.
                      For example: /set_emoji 😊
 
3. /my_emoji -        with this command any people can check settled an emoji for him.

4. /ignore -          used this command, a member can to enable or disable ignore mode for /all command.
                      It's means that, if you enabled it, when the /all command will start, the bot wouldn't to count you.

5. /info -            the bot will send information about himself


## Deployment Instructions
For first, you need to clone this repo in your local or cloud machine,
Next, you need to change .env file, change variables to yours,
Finally, you would to install python variables on your local or VM machine by ```pip install -r requieremnts.txt``` and run ```python3 main.py```,     // You must to launch MongoDB before it
Or, run ```docker build -t ${image_name}```, push it into your like containers repo and deploy to a cloud.
