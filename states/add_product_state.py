from aiogram.dispatcher.filters.state import StatesGroup, State

class AddProductState(StatesGroup):
    name = State()
    description = State()
    price = State()
    category = State()
    subcategory = State()
    