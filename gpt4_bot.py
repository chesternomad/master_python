#! /usr/bin/python3

# pip3 install pyTelegramBotAPI requests python-dotenv
import time
import json
import telebot
from dotenv import dotenv_values
import requests
import logging
from functools import wraps
format = '%(levelname)s - %(asctime)s - %(message)s'
logging.basicConfig(filename='./logging.txt', filemode='w', format=format)
logger = logging.getLogger()

logger.error('this is a testing for logging')

config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
api_key = config['API_KEY']
bot = telebot.TeleBot(BOT_TOKEN)
api_endpoint = "https://api.openai.com/v1/chat/completions"
model_engine = 'gpt-3.5-turbo'


def is_known_username(username):
    '''
    Returns a boolean if the username is known in the user-list.
    '''
    known_usernames = ['username1', 'username2']

    return username in known_usernames




def private_access():
    """
    Restrict access to the command to users allowed by the is_known_username function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.username

            if is_known_username(username):
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='Who are you?  Keep on walking...')

        return f_restrict  # true decorator

    return deco_restrict



def delete_message(chat_id, msg_id):
    time.sleep(5)
    bot.delete_message(chat_id, msg_id)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey, what are you doing now?")


@bot.message_handler(regexp='^love$')
def default_command(message):
    msg = bot.send_message(message.chat.id, "Nomadland2/7")
    delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(func=lambda message: True)
@private_access()
def echo_all(message):
    

	payload = {'model':f'{model_engine}','messages':[{'role':'user','content':f'{message.text}'}],"max_tokens": 500,"n": 1, "stop": "?|.", "temperature":0.7, "presence_penalty": 0.5}

	response = requests.post(api_endpoint, json=payload, headers={"Authorization": f"Bearer {api_key}"})


	response = response.json()['choices'][0]['message']['content']

	bot.send_message(message.chat.id, response)


bot.infinity_polling()
