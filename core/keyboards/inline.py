from decouple import config

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callbackdata import MacInfo

admin_id = config('ADMIN_ID')

select_macbook = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Macbook Air 13" M1 2020',
            callback_data='apple_air_13_m1_2020',
        ),
    ],
    [
        InlineKeyboardButton(
            text='Macbook Pro 14" M1 2021',
            callback_data='apple_pro_14_m1_2021',
        ),
    ],
    [
        InlineKeyboardButton(
            text='Macbook Pro 15" 2019',
            callback_data='apple_pro_15_i7_2019',
        ),
    ],
    [
        InlineKeyboardButton(
            text='Link',
            url='https://osmon23.github.io/CV/',
        ),
    ],
    [
        InlineKeyboardButton(
            text='Profile',
            url=f'tg://user?id={admin_id}',
        ),
    ],
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Macbook Air 13" M1 2020', callback_data=MacInfo(model='air', size=13, chip='m1', year=2020))
    keyboard_builder.button(text='Macbook Pro 14" M1 2021', callback_data=MacInfo(model='pro', size=14, chip='m1', year=2021))
    keyboard_builder.button(text='Macbook Pro 15" i7 2019', callback_data=MacInfo(model='pro', size=15, chip='i7', year=2019))
    keyboard_builder.button(text='Link', url='https://osmon23.github.io/CV/')
    keyboard_builder.button(text='Profile', url=f'tg://user?id={admin_id}')

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()
