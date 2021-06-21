# Before run the code,
# we need to run 'pip install python-telegram-bot --upgrade' in terminal

import telegram

api_key = 'here, input your chatbot api token key you got from botfather(telegram)'

bot = telegram.Bot(token=api_key)

# chat_id = bot.get_updates()[-1].message.chat_id   # <-this code is for checking chat_id of my bot
# print(chat_id)
chat_id = # <- input your chat_id you got from 2 lines of code above in here  
# this chat_id will be a bridge btw our code and telegram response, we will use this id and token key in the final code

# In case we want to check if bot works well, we can try this simple welcoming sentence
bot.sendMessage(chat_id = chat_id,
                text="Hi, I'm ALL ABOUT COVID bot!")
