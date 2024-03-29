#! /usr/bin/python3

# pip3 install pyTelegramBotAPI requests python-dotenv
import time
import json
import telebot
from dotenv import dotenv_values
import requests
import logging
from functools import wraps
import urllib.parse
from datetime import datetime
from google.cloud import texttospeech
import os

format = '%(levelname)s - %(asctime)s - %(message)s'
logging.basicConfig(filename='./logging.txt', filemode='w', format=format)
logger = logging.getLogger()

logger.error('this is a testing for logging')

config = dotenv_values(".env")

BOT_TOKEN = config['BOT_TOKEN']
api_key = config['API_KEY']
google_api = config['GOOGLE_API']
bot = telebot.TeleBot(BOT_TOKEN)
api_endpoint = "https://api.openai.com/v1/chat/completions"
model_engine = 'gpt-3.5-turbo'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ubuntu/python/tg_bot/maps-1555844439055-11d99fcd0784.json'

def is_known_username(username):
    '''
    Returns a boolean if the username is known in the user-list.
    '''
    known_usernames = ['nomad72', 'username2']

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


def get_restaurant_list(latitude, longitude):
    keys = ['name', 'rating', 'user_ratings_total', 'place_id']
    restaurant_list = []
    url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + \
        str(latitude)+'%2C'+str(longitude) + \
        '&radius=1000&type=restaurant&opennow&key='+google_api

    payload = {}
    headers = {}
    message = ''
    response1 = requests.request("GET", url1, headers=headers, data=payload)
    dict = response1.json().get('results')
    for i in range(len(dict)):

        url2 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + \
            str(latitude)+"%2C"+str(longitude)+"&destinations=place_id:" + \
            dict[i]['place_id']+"&key="+google_api
        response2 = requests.request(
            "GET", url2, headers=headers, data=payload)
        distance = response2.json(
        )['rows'][0]['elements'][0]['distance']['text']
        sub_dir = {key: (dict[i][key] if key in dict[i]
                         else 'empty') for key in keys}
        sub_dir.update({'dist': distance})
        restaurant_list.append(sub_dir)
    for i in restaurant_list:
        for j in i:
            if j == 'name':
                message += f"{j}: {i.get(j).encode('utf-8').decode('latin1')}\n"
            elif j == 'place_id':
                place = urllib.parse.quote(i.get('name'))
                message += f'Map: https://www.google.com/maps/search/?api=1&query={place}&query_place_id={i.get(j)}\n'
            else:
                message += f'{j}: {i.get(j)}\n'
        message += f'\n'

    return message


@bot.message_handler(commands=['text_to_speech'])
def send_welcome(message):
    japanese_text = bot.send_message(
        message.chat.id, "please input the text to translate to audio")
    bot.register_next_step_handler(japanese_text, to_audio)



def to_audio(message):
    # Set up the text-to-speech client
    input_text = message.text
    now =  datetime.now().strftime('%d%m%Y_%H:%M:%S')
    output_file = f'{now}.mp3'
    client = texttospeech.TextToSpeechClient()

    # Set the input text and voice parameters
    synthesis_input = texttospeech.SynthesisInput(text=input_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='ja-JP', # Japanese language code
        name='ja-JP-Neural2-B', # Japanese voice name
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,# Voice gender
    )

    # Set the audio file format and encoding
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, # MP3 encoding
        effects_profile_id=['handset-class-device'],
        speaking_rate=1.0,
        pitch=0.0
    )

    # Generate the text-to-speech response
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # Write the audio response to a file
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
    bot.send_audio(message.chat.id,audio=open(f'{now}.mp3', 'rb'))
    time.sleep(40)
    os.remove(f'{now}.mp3')




@bot.message_handler(regexp='^love$')
def default_command(message):
    msg = bot.send_message(message.chat.id, "nomadland2/7")
    delete_message(msg.chat.id, msg.message_id)


@bot.message_handler(content_types=['location'])
def handle_location(message):

    restaurant_list = get_restaurant_list(
        message.location.latitude, message.location.longitude)
    print(restaurant_list)
    # restaurant_list = [restaurants[i:i + 4000] for i in range(0, len(restaurants), 4000)]
    # for restaurant in restaurant_list:
    bot.send_message(message.chat.id, restaurant_list.encode('utf-8'))


@bot.message_handler(func=lambda message: True)
# @private_access()
def echo_all(message):

    payload = {'model': f'{model_engine}', 'messages': [
        {'role': 'user', 'content': f'{message.text}'}], "max_tokens": 500, "n": 1, "stop": "?|.", "temperature": 0.7, "presence_penalty": 0.5}

    response = requests.post(api_endpoint, json=payload, headers={
                             "Authorization": f"Bearer {api_key}"})

    response = response.json()['choices'][0]['message']['content']

    bot.send_message(message.chat.id, response)


bot.infinity_polling()
