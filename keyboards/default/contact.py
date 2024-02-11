from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqam yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True,
)