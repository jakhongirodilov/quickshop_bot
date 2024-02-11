from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message

from keyboards.inline.menu_keyboards import (
    menu_cd,
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard,
    item_keyboard
)

from loader import dp, db


@dp.message_handler(text="Bosh menyu")
async def show_menu(message: types.Message):
    categories = await db.select_all_categories()

    if categories:
        await list_categories(message)
    else:
        await message.answer("Hozircha bo'limlar mavjud emas!")



async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    keyboard = await categories_keyboard()

    if isinstance(message, Message):
        await message.answer("Bo'limni tanlang", reply_markup=keyboard)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text="Bo'limni tanlang", reply_markup=keyboard)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    keyboard = await subcategories_keyboard(category)

    
    await callback.message.edit_text(text="Mahsulot turini tanlang", reply_markup=keyboard)


async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    keyboard = await items_keyboard(category, subcategory)

    await callback.message.edit_text(text="Mahsulot tanlang:", reply_markup=keyboard)


async def item(callback: CallbackQuery, category, subcategory, item_id, **kwargs):
    keyboard = await item_keyboard(category, subcategory, item_id) 

    item = await db.select_product(item_id)
    print(f"selected item -------------------- {item}")
    item_name = item[1]
    item_description = item[2]
    item_price = item[3]

    info = f"{item_name} \n\n{item_description} \n\nNarxi: ${item_price}"

    await callback.message.edit_text(text=info, reply_markup=keyboard)


# Yuqoridagi barcha funksiyalar uchun yagona handler
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    :param call: Handlerga kelgan Callback query
    :param callback_data: Tugma bosilganda kelgan ma'lumotlar
    """

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = int(callback_data.get("item_id"))

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories, 
        "1": list_subcategories, 
        "2": list_items,
        "3": item
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id
    )