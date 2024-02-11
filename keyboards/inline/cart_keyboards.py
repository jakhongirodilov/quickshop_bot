import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db



async def cart_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(
        InlineKeyboardButton(text="Buyurtma berish", callback_data="order")
    )

    markup.insert(
        InlineKeyboardButton(text="Savatchani tozalash", callback_data="clear_cart")
    )

    return markup