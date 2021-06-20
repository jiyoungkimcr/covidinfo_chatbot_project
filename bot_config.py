# Before run the code,
# we need to run 'pip install python-telegram-bot --upgrade' in terminal

import telegram

api_key = '1743843452:AAF8fd99PD6ZlWArtPMOSMyuCsiGKXI2gnc'

bot = telegram.Bot(token=api_key)

# chat_id = bot.get_updates()[-1].message.chat_id   # <-this code is for checking chat_id of my bot
# print(chat_id)
chat_id = 1871793518 # this chat_id will be a bridge btw our code and telegram response, we will use this id and token key in the final code

# In case we want to check if bot works well, we can try this simple welcoming sentence
bot.sendMessage(chat_id = chat_id,
                text="Hi, I'm ALL ABOUT COVID bot!")
