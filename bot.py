import json

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, TRANSLATE_API_TOKEN

#Программа-бот для телеграмма, для перевода с английского на русский язык. Максимальная длина текста 1000 символов.

PROXY_URL = "http://proxy.server:3128"

bot = Bot(token=TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


class Translate:  # класс, который содержит в себе все нужные поля для запроса
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"  # адрес запроса
    querystring = {"to[0]": "ru", "api-version": "3.0", "profanityAction": "NoAction",
                   "textType": "plain"}  # параметры запроса

    API_KEY = TRANSLATE_API_TOKEN  # наш ключ API
    API_HOST = "microsoft-translator-text.p.rapidapi.com"  # хост
    headers = {  # заголовки запроса
        "content-type": "application/json",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    @staticmethod
    def translate(text):  # метод, который отправляет запрос и возвращает перевод текста, текст передается в виде
        # параметра этого метода
        payload = [{"Text": text}]

        r = requests.request("POST", Translate.url, json=payload, headers=Translate.headers,
                             params=Translate.querystring)  # отправляем запрос со всеми параметрами
        r.encoding = "utf8"  # устанавливаем кодировку символов
        return json.loads(r.text)[0].get("translations")[0].get("text")  # возвращаем текст из ответа


@dp.message_handler(commands=["start", "help"])
async def process_start_command(message: types.Message):
    await message.reply(
        "Это бот переводчик. Я перевожу с английского на русский язык\nМаксимальная длина текста - 1000символов")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, Translate.translate(msg.text))


if __name__ == '__main__':
    executor.start_polling(dp)
