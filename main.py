import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import requests, random
from googletrans import Translator

# lesson_TG01_bot
bot = Bot(token=TOKEN)
dp = Dispatcher()


def translate_text(en_text):
    translator = Translator()
    ru_text = translator.translate(en_text, src='en', dest='ru').text
    return ru_text


@dp.message(Command('meteo'))
async def f_meteo(message: Message):
    city = "Москва"
    api_key = "bf599969fa3d07075ac981c3ba80fab8"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather = response.json()

    translated_city = translate_text(weather['name'])
    text_1 = f"Погода в городе {translated_city}"
    text_2 = f"Температура: {weather['main']['temp']}°C"
    translated_weather = translate_text(weather['weather'][0]['description'])
    text_3 = f"Погода: {translated_weather}"
    await message.answer(f"{text_1}:\n{text_2}\n{text_3}")


@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект – это свойство искусственных интеллектуальных систем выполнять'
                         ' творческие функции, которые традиционно считаются прерогативой человека; наука и технология'
                         ' создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(F.photo)
async def react_photo(message: Message):
    answer_list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answer = random.choice(answer_list)
    await message.answer(rand_answer)


@dp.message(Command('photo'))
async def photo(message: Message):
    photos = ["https://gallerix.ru/pic/_EX/1593896443/655331420.jpeg",
              "https://sr.gallerix.ru/M/1161425349/2468.jpg",
              "https://sr.gallerix.ru/V/369985082/2129753821.jpg",
              "https://sr.gallerix.ru/D/825575191/1663997468.jpg",
              "https://sr.gallerix.ru/_EX/1124510458/768903337.jpg",
              ]
    random_photo = random.choice(photos)
    await message.answer_photo(photo=random_photo, caption='Это супер крутая картинка')


@dp.message(Command('help'))
async def f_help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/meteo")


@dp.message(CommandStart())
async def f_start(message: Message):
    await message.answer("Приветики, я учебный бот урока TG01 !")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
