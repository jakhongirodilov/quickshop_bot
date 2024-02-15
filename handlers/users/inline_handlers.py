from aiogram import types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from keyboards.inline.menu_keyboards import item_keyboard

from loader import dp, db, bot


@dp.inline_handler()
async def search_product(inline_query: types.InlineQuery):
    query = inline_query.query
    print(query)

    if query:
        products = await db.search_products(query)

        results = []
        for product in products:
            print(f"Product: {product}")
            print('--------', product['category_id'], product['subcategory_id'], product['id'])

            keyboard = await item_keyboard(product['category_id'], product['subcategory_id'], product['id'], inline_mode=True)

            result = InlineQueryResultArticle(
                id=str(product['id']),
                title=product['name'],
                description=product['description'],
                input_message_content=InputTextMessageContent(
                    message_text=f"Name: {product['name']}\nDescription: {product['description']}\nPrice: {product['price']}"
                ),
                reply_markup=keyboard
            )
            results.append(result)

        # Send the results back to the user
        await bot.answer_inline_query(inline_query.id, results=results)
    else:
        # If no query is provided, don't return any results
        await bot.answer_inline_query(inline_query.id, results=[])