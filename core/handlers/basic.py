from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from core.keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.keyboards.inline import select_macbook, get_inline_keyboard


async def get_start(message: Message):
    await message.answer(f'<s>Добро пожаловать</s>, {hbold(message.from_user.full_name)}!\n'
                         f'<b>Напишите токен</b> <tg-spoiler>для доступа</tg-spoiler>.',
                         reply_markup=get_reply_keyboard())


async def get_inline(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}. Показываю инлайн кнопки!',
                         reply_markup=get_inline_keyboard())


async def get_location(message: Message):
    await message.answer(f'Ты отправил локацию!\r\a'
                         f'{message.location.latitude}\r\a{message.location.longitude}')


async def get_photo(message: Message, bot: Bot):
    await message.answer('Я сохраню эту картину себе.')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'images/{file.file_id}.jpg')
