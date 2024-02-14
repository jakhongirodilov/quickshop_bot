from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bosh menyu"),
        ],
        [ 
            KeyboardButton(text="Cart"), 
        ],
        [ 
            KeyboardButton(text="Buyurtmalarim"), 
        ],
    ],
    resize_keyboard=True,
)