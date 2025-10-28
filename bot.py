# подключение библиотек
from aiohttp.helpers import TOKEN
from mistralai import Mistral # импортируем клиент для Mistral
import asyncio # асинхронный фреймворк для запуска бота
import logging # журнал ошибок и тп
from aiogram import Bot, Dispatcher, types, F #
from aiogram.filters import Command # фильтр для команд
from aiogram.methods import DeleteWebhook # метод для удаления Webhook перед запуском long polling
from aiogram.types import Message
from mistralai.client import MistralClient
from dotenv import load_dotenv
import os
import keyboards as kb

load_dotenv()  # загружает переменные из .env


# ключ от mistral ai
mistral_token_key = os.getenv("MISTRAL_TOKEN")
# ключ от тг бота
TOKEN = os.getenv("TELEGRAM_TOKEN")


# модели и клиент ии
model = "mistral-tiny"
client = Mistral(api_key=mistral_token_key)

# список для сохранения сообщений и истории бота
chat_history = {}

# создание бота
# включается логирование и создаютя объекты для бота
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# обработка команды старт
@dp.message(Command("start"))
async def start(message: types.Message):
    # ответ пользователью на команду
    await message.answer("Привет, я бот с Mistral! Нажми кнопку help, чтобы узнать подробнее про меня!", reply_markup=kb.start_menu)

@dp.message(F.text == "help")
async def text(message: types.Message):
    await message.answer(
        "Привет, я бот с Mistral! Меня создал студент группы БиК2403 Филиппов Вячеслав. "
        "Ты можешь задать мне любой вопрос или просто поговорить со мной ")

@dp.message(F.text == "prosto")
async def text(message: types.Message):
    await message.answer(
        "это просто кнопка, которая ничего не делает"
         )

# обработка любого текстового сообщения
@dp.message(F.text)
async def text(message: types.Message):
    # получаем id чата
    chat_id = message.chat.id
# если история чата пустая, то создаем ее сами с ролью и системой
    if chat_id not in chat_history:
        chat_history[chat_id] = [
            {
                "role": "system",
                "content": "Ты полезный ассистент, отвечай кратко и по делу."
            }
        ]

    # добавляем сообщение пользователя в историю.
    chat_history[chat_id].append({
        "role": "user",
        "content": message.text
    })

    # отправляем запрос в Mistral, но это делаем с историей чата.
    chat_response = client.chat.complete(
        model=model,
        messages=chat_history[chat_id]
    )

    # получаем ответ и добавляем его в историю.
    response_text = chat_response.choices[0].message.content
    chat_history[chat_id].append({
        "role": "assistant",
        "content": response_text
    })

    # ограничиваем историю, чтобы не превышать лимит сообщений
    if len(chat_history[chat_id]) > 10:
        # добавляем в историю 1 системное и остальные
        chat_history[chat_id] = [chat_history[chat_id][0]] + chat_history[chat_id][-9:]

    # отправляем ответ пользователю
    await message.answer(response_text, parse_mode="Markdown")

# Удаляем Webhook (если был), запускаем long polling (ожидание сообщений)
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())