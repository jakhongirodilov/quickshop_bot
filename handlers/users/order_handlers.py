from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_keyboards import add_to_cart_callback
from keyboards.inline.cart_keyboards import cart_keyboard
from keyboards.default.contact import phone_number_keyboard
from keyboards.default.location import location_keyboard
from keyboards.default.start_keyboard import menu

from states.order_state import Order

from loader import dp, db


@dp.callback_query_handler(text="order")
async def start_order(call: CallbackQuery):
    telegram_id = call.from_user.id
    user = await db.select_user(telegram_id)
    cart_items = await db.get_cart_items(user["id"])

    if cart_items:
        # If there are items in the cart, ask for the user's name
        await call.answer()
        await call.message.answer("Ism-familiyangizni kiriting: ")
        await Order.full_name.set()
    else:
        # If the cart is empty, display a popup message
        await call.answer("Savatchangizda mahsulotlar mavjud emas!")


@dp.message_handler(state=Order.full_name)
async def receive_full_name(message: Message, state: FSMContext):
    full_name = message.text 

    await state.update_data(
        {'full_name': full_name}
    )

    await message.answer('Telefon raqamingizni kiriting:', reply_markup=phone_number_keyboard)

    await Order.next()


@dp.message_handler(content_types=ContentType.CONTACT, state=Order.phone_number)
async def recieve_phone_number(message: Message, state: FSMContext):
    phone_number = str(message.contact.phone_number)

    await state.update_data(
        {'phone_number': phone_number}
    )

    await message.answer('Lokatsiyangizni yuboring: ', reply_markup=location_keyboard)

    await Order.next()


@dp.message_handler(content_types=ContentType.LOCATION, state=Order.location)
async def recieve_location(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = await db.select_user(telegram_id)

    location = message.location
    latitude = str(location.latitude)
    longitude = str(location.longitude)

    await state.update_data(
        {
            'latitude': latitude, 
            'longitude': longitude
        }
    )

    data = await state.get_data()
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Retrieve cart items for the user
    cart_items = await db.get_cart_items(user["id"])

    # Create an order for each item in the cart
    for cart_item in cart_items:
        product = await db.select_product(cart_item['product_id'])
        total_price = product['price'] * cart_item['quantity']
        
        # Create an order for the current cart item
        await db.add_order(
            user_id=user['id'],
            product_id=product['id'],
            quantity=cart_item['quantity'],
            price=product['price'],
            total_price=total_price
        )

    await db.clear_cart_items(user['id'])

    await state.finish()
    await message.answer('Buyurtmangiz qabul qilindi!', reply_markup=menu)