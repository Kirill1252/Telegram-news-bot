import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from datetime import datetime

from config import token_bot
from nashemisto_dp import update_news_02
from km_5692 import update_news_01
from weather import get_weather
from currency_converter import getting_prices_for_currencies

bot = Bot(token=token_bot)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands='start')
async def start(message: types.Message):
    buttons = [
        'Новости за сегодня: nashemisto_dp', 'Свежие новости: nashemisto_dp',
        'Новости за сегодня: 5692', 'Свежие новости: 5692',
        'Погода Днепр', 'Погода Каменское', 'Курс валют'
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.reply("Панель", reply_markup=keyboard)


#News Dnepr
@dispatcher.message_handler(Text(equals='Курс валют'))
async def get_currency(message: types.Message):
    currency = getting_prices_for_currencies()
    response = f"ПриватБанк\n" \
               f"EUR:\t{currency['EUR']['buy']} / {currency['EUR']['sale']}\n" \
               f"USD:\t{currency['USD']['buy']} / {currency['USD']['sale']}"
    await message.answer(response)


@dispatcher.message_handler(Text(equals='Новости за сегодня: nashemisto_dp'))
async def get_last_news_dp(message: types.Message):
    with open('json_file/nashemisto_dp_news_dict.json') as file:
        news_dict = json.load(file)

    date = datetime.now()
    day = f"{date.strftime('%d')}.{date.strftime('%m')}.{date.strftime('%Y')}"

    for k, v in sorted(news_dict.items()):
        if day == v['time'][0:-6]:
            news = f"Источник: {v['url']}"
            await message.answer(news)


@dispatcher.message_handler(Text(equals='Свежие новости: nashemisto_dp'))
async def get_fresh_news_dp(message: types.Message):
    fresh_news = update_news_02()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"Источник: {v['url']}"
            await message.answer(news)
    else:
        await message.answer("Свежих новостей нету...")


@dispatcher.message_handler(Text(equals='Погода Днепр'))
async def get_weather_dp(message: types.Message):
    weath = get_weather('Днепр')
    response = f"Город: {weath['city']}\n" \
               f"Температура: {weath['temperature']} °C\n" \
               f"Влажность воздуха: {weath['air_humidity']} %\n" \
               f"Скорость ветра: {weath['wind_speed']} м/с"

    await message.answer(response)

#News Kamen
@dispatcher.message_handler(Text(equals='Новости за сегодня: 5692'))
async def get_last_news_km(message: types.Message):
    with open('json_file/5692_news_dict.json') as file:
        news_dict = json.load(file)

    date = datetime.now()
    day = f"{date.strftime('%d')}.{date.strftime('%m')}.{date.strftime('%Y')}"

    for k, v in sorted(news_dict.items()):
        if day == v['time']:
            news = f"Источник: {v['url']}"
            await message.answer(news)


@dispatcher.message_handler(Text(equals='Свежие новости: 5692'))
async def get_fresh_news_dp(message: types.Message):
    fresh_news = update_news_01()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"Источник: {v['url']}"
            await message.answer(news)
    else:
        await message.answer("Свежих новостей нету...")


@dispatcher.message_handler(Text(equals='Погода Каменское'))
async def get_weather_dp(message: types.Message):
    weath = get_weather('Каменское')
    response = f"Город: {weath['city']}\n" \
               f"Температура: {weath['temperature']} °C\n" \
               f"Влажность воздуха: {weath['air_humidity']} %\n" \
               f"Скорость ветра: {weath['wind_speed']} м/с"

    await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dispatcher)

