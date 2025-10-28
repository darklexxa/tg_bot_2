from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='help'),
            KeyboardButton(text='prosto')
        ]
    ],
    resize_keyboard=True,  # размер кнопки
    one_time_keyboard=False # свернуть клавиатуру

)