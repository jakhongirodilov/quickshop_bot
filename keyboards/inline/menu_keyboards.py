import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")


# Quyidagi funksiya yordamida menyudagi har bir element uchun callback data yaratib olinadi
# Agar mahsulot kategoriyasi, ost-kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(
        level=level, category=category, subcategory=subcategory, item_id=item_id
    )


# Kategoriyalar uchun keyboard
async def categories_keyboard():
    CURRENT_LEVEL = 0

    # Keyboard yaratamiz
    markup = InlineKeyboardMarkup(row_width=1)

    # Bazadagi barcha kategoriyalarni olamiz
    categories = await db.select_all_categories()

    # Har bir kategoriya uchun quyidagilarni bajaramiz:
    for category in categories:
        # Tugma matnini yasab olamiz
        button_text = f"{category['category_name']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, 
            category=category["id"]
        )

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    category = int(category)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = await db.select_all_subcategories(category)
    for subcategory in subcategories:
        # Tugma matnini yasaymiz
        button_text = f"{subcategory['subcategory_name']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory["id"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasini yasaymiz (yuoqri qavatga qaytamiz)
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    items = await db.select_all_products(category_id=int(category), subcategory_id=int(subcategory))

    for item in items:
        button_text = f"{item['name']}"

        callback_data = make_callback_data(
            level = CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory,
            item_id = item['id']
        )

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)    
        )

    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category
            ),
        )
    )
    return markup


add_to_cart_callback = CallbackData("add_to_cart", "product_id")

async def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=3)

    item = await db.select_product(item_id)

    markup.row(
        InlineKeyboardButton(
            text="-",
            callback_data="decrement_quantity"
        ),
        InlineKeyboardButton(
            text="1",
            callback_data="set_quantity_1"
        ),
        InlineKeyboardButton(
            text="+",
            callback_data="increment_quantity"
        )
    )

    callback_data = add_to_cart_callback.new(product_id=item['id'])

    markup.row(
        InlineKeyboardButton(
            text="Add to cart",
            callback_data=callback_data
        )
    )

    print(callback_data)

    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory
            ),
        )
    )

    return markup