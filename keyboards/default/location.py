from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Lokatsiya yuborish", request_location=True),
        ],
    ],
    resize_keyboard=True,
)