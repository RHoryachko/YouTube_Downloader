import telebot
import os
import time

from telebot import types
from config import TOKEN
from pytube import YouTube

bot = telebot.TeleBot(TOKEN)



def download_audio(message):
	try:
		print(f'{message.from_user.id} - {message.from_user.username} = download ')
		yt_obj = YouTube(str(message))
		bot.send_message(message.chat.id, 'Зачекай, іде скачування...')
		yt_obj.streams.get_audio_only().download(output_path='files/', filename=f'{yt_obj.title}.mp3')
		print(f'YouTube audio {yt_obj.title} downloaded successfully')
		audio = open(f'files/{yt_obj.title}.mp3', 'rb')
		bot.send_audio(message.chat.id, audio)
		audio.close()
		os.remove(f'files/{yt_obj.title}.mp3')
		print(f'Audio {yt_obj.title} removed')
		bot.send_message(message.chat.id, "Процес завершено, щоб повторити скинь ссилку")
		bot.register_next_step_handler(message, download_audio)
	except Exception as e:
		print(e)
		print(f'{message.from_user.id} - {message.from_user.username} = error ')
		bot.send_message(message.chat.id, 'Посилання не працює, скинь коректне')
		bot.register_next_step_handler(message, download_audio)



@bot.message_handler(commands=['start'])
def start(message):

	print(f'{message.from_user.id} - {message.from_user.username} = start ')
	bot.send_message(message.chat.id, "Кинь ссилку на скачування")
	bot.register_next_step_handler(message, download_audio)


bot.polling(none_stop=True)