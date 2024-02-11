from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bosh menyu"),
        ],
        [ 
            KeyboardButton(text="Cart"), 
        ],
    ],
    resize_keyboard=True,
)