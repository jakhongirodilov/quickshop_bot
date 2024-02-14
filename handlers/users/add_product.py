import asyncpg
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command

from keyboards.inline.menu_keyboards import menu_cd, categories_keyboard, subcategories_keyboard
from states.add_product_state import AddProductState

from loader import dp, db, bot
from data.config import ADMINS

@dp.message_handler(Command("add_product"))
async def add_product(message: types.Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        await message.answer("Mahsulot nomini kiriting: ")
        await AddProductState.name.set()
    else:
        await message.answer("Mahsulot qo'shish uchun admin bo'lishingiz kerak!")


@dp.message_handler(state=AddProductState.name)
async def receive_product_name(message: types.Message, state: FSMContext):
    name = message.text
    print(name)

    await state.update_data({'name': name})

    await message.answer("Mahsulot tavsifini kiriting:")

    await AddProductState.next()


@dp.message_handler(state=AddProductState.description)
async def recieve_product_description(message: types.Message, state: FSMContext):
    description = message.text

    await state.update_data(
        {'description': description}
    )

    await message.answer("Mahsulot narxini kiriting:")

    await AddProductState.next()


@dp.message_handler(state=AddProductState.price)
async def recieve_product_price(message: types.Message, state: FSMContext):
    price = message.text
    print(price)

    await state.update_data(
        {'price': price}
    )

    keyboard = await categories_keyboard()
    print(keyboard)

    await message.answer("Mahsulot kategoriyasini tanlang:", reply_markup=keyboard)
    
    await AddProductState.next()


@dp.callback_query_handler(menu_cd.filter(level='1'), state=AddProductState.category)
async def recieve_product_category(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category = callback_data.get('category')

    await state.update_data({'category': category})

    keyboard = await subcategories_keyboard(category)

    await bot.send_message(callback_query.message.chat.id, "Mahsulot ostkategoriyasini tanlang:", reply_markup=keyboard)

    await AddProductState.next()



@dp.callback_query_handler(menu_cd.filter(level='2'), state=AddProductState.subcategory)
async def recieve_product_subcategory(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subcategory = callback_data.get('subcategory')

    await state.update_data(
        {'subcategory': subcategory}
    )

    data = await state.get_data()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')
    subcategory = data.get('subcategory')

    await db.add_product(name, description, price, int(category), int(subcategory))

    await bot.send_message(callback_query.message.chat.id, "Mahsulot bazaga qo'shildi!")