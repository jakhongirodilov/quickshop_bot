from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message

from keyboards.inline.menu_keyboards import add_to_cart_callback
from keyboards.inline.cart_keyboards import cart_keyboard

from loader import dp, db


# savatga mahsulot qo'shish
@dp.callback_query_handler(add_to_cart_callback.filter())
async def add_to_cart(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id

    user = await db.select_user(telegram_id=user_id)

    product_id = int(callback_data.get('product_id'))
    quantity = 1

    cart_item = await db.get_cart_item(user['id'], product_id)

    if cart_item:
        await db.increment_quantity(user['id'], product_id)
        await call.answer("The item is already in your cart. Quantity increased!", show_alert=True)
    else:
        await db.add_to_cart(user['id'], product_id, quantity)
        await call.answer(f"Item added to cart ✅\nMahsulot savatga qo'shildi ✅", show_alert=True)


#savatdagi mahsulotlarni ko'rsatish
@dp.message_handler(text="Cart")
async def cart(message: types.Message):
    user_id = message.from_user.id
    user = await db.select_user(user_id)

    cart_items = await db.get_cart_items(user["id"])

    msg = "Savatchangizdagi mahsulotlar:\n"
    total_cost = 0
    i = 1

    for item in cart_items:
        product = await db.select_product(item['product_id'])

        msg += f"\n{i}.\n{product['name']} \n{item['quantity']} x ${product['price']}\n"
        total_cost += product['price'] * item['quantity']

        i += 1

    msg += f"\nUmumiy narx: ${total_cost}"

    keyboard = await cart_keyboard()

    await message.answer(msg, reply_markup=keyboard)


# savatchani tozalash
@dp.callback_query_handler(text="clear_cart")
async def clear_cart(call: CallbackQuery):
    user_id = call.from_user.id
    user = await db.select_user(user_id)

    cart_items = await db.clear_cart_items(user["id"])

    await call.message.edit_text("Savatchangiz tozalandi ✅\nXaridni davom ettirish uchun 'Bosh Menu' tugmasini bosing⬇️")

