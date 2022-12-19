import requests


def getting_prices_for_currencies():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    data = response.json()

    buy_eur = data[0]['buy'][:-3]
    sale_eur = data[0]['sale'][:-3]

    buy_usd = data[1]['buy'][:-3]
    sale_usd = data[1]['sale'][:-3]

    cour_dict = {
        'EUR': {
            'buy': buy_eur,
            'sale': sale_eur
        },
        'USD': {
            'buy': buy_usd,
            'sale': sale_usd
        }
    }

    return cour_dict
