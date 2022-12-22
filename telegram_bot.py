import json
from aiogram import Bot, Dispatcher, executor, types
from config import token_bot
from datetime import datetime


bot = Bot(token=token_bot)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("What's up Doc?")


@dispatcher.message_handler(commands='all_news_dp')
async def get_all_news_dp(message: types.Message):
    with open('json_file/nashemisto_dp_news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{v['time']}\n" \
               f"{v['description']}\n" \
               f"Источник: {v['url']}"
        await message.answer(news)


@dispatcher.message_handler(commands='last')
async def get_last_news(message: types.Message):
    with open('json_file/nashemisto_dp_news_dict.json') as file:
        news_dict = json.load(file)

    date = datetime.now()
    day = f"{date.strftime('%d')}.{date.strftime('%m')}.{date.strftime('%Y')}"

    for k, v in sorted(news_dict.items()):
        if day == v['time'][0:-6]:
            news = f"Источник: {v['url']}"
            await message.answer(news)


if __name__ == '__main__':
    executor.start_polling(dispatcher)

