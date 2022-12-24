import requests
import json
from config import currencies
from exceptions import APIException

class Convertor:
	@staticmethod
	def get_price(base, quote, amount):
		try:
			base_key = currencies[base.lower()]
		except KeyError:
			raise APIException(f'Валюта {base} не найдена')

		try:
			quote_key = currencies[quote.lower()]
		except KeyError:
			raise APIException(f'Валюта {quote} не найдена')

		if base_key == quote_key:
			raise APIException(f'Вы пытаетесь перевести одинаковые валюты')

		try:
			amount = float(amount)
		except ValueError:
			raise APIException(f'Не удалось обработать {amount}')
		r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currencies[base]}&tsyms={currencies[quote]}')
		total_base = json.loads(r.content)[currencies[quote]]
		total_base = float(total_base) * float(amount)
		text = f'{amount} {base} = {total_base} {quote}'
		return text

