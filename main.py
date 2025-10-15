import requests
import os
from dotenv import load_dotenv
import argparse


def get_exchange_rates(token, base_currency):
    url = f'https://v6.exchangerate-api.com/v6/{token}/latest/{base_currency}'
    response = requests.get(url)
    response.raise_for_status()
    exchange_rates = response.json()['conversion_rates']
    return exchange_rates


def convert_amount(exchange_rates, target_currency, amount):
    target_rate = exchange_rates[target_currency]
    print(f'курс целевой валюты к базовой: {target_rate}') 
    converted_amount = amount * target_rate
    return converted_amount


def main():
    load_dotenv()

    api_key = os.getenv('API_KEY')

    parser = argparse.ArgumentParser(description='Эта программа позволяет конвертировать из базовой в целевую из сервиса exchangerate-api по сумме')
    parser.add_argument('--base_currency', type=str, help='наименование валюты для просмотра курса обмены', default='RUB')
    parser.add_argument('--target_currency', type=str, help='наименование целевой валюты для просмотра курса обмены', default='USD')
    parser.add_argument('--amount', type=float, help='Сумма', default=1000)
    args = parser.parse_args()

    base_currency = args.base_currency
    target_currency = args.target_currency
    amount = args.amount

    try:
        exchange_rates = get_exchange_rates(api_key, base_currency)
        print(convert_amount(exchange_rates, target_currency, amount))
    except requests.HTTPError:
        print("Запрос не найден")


if __name__ == '__main__':
    main()