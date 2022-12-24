import telebot
import requests
import json
from config import bot, currencies
from extensions import Convertor
from exceptions import APIException


def main():
	@bot.message_handler(commands = ['start', 'help'])
	def help(message: telebot.types.Message):
		text = 'Введите запрос в формате:\n <имя валюты> \
	<в какую валюту перевести> \
	<количество валюты>\nПоказать список доступных валют: /values'
		bot.reply_to(message, text)

	@bot.message_handler(commands = ['values'])
	def values(message: telebot.types.Message):
		text = 'Доступные валюты:'
		for currency in currencies.keys():
			text = '\n'.join((text, currency ))
		bot.reply_to(message, text)

	@bot.message_handler(content_types = ['text', ])
	def convert(message: telebot.types.Message):
		values = message.text.split(' ')
		# base, quote, amount = values
		
		try:	
			if len(values) != 3:
				raise APIException('Вводите только 3 параметра.')
			respond = Convertor.get_price(*values)
		except APIException as e:
			bot.reply_to(message, f'Ошибка ввода: \n{e}')

		except Exceptioin as e:
			traceback.print_tb(e.__traceback__)
			bot.reply_to(message, f'Неизвестная ошибка: n{e}')

		else:
			bot.reply_to(message, respond)

	bot.polling()


if __name__ == '__main__':
	main()