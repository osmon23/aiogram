from aiogram.types import Message


async def get_true_contact(message: Message, phone: str):
    await message.answer(f'Ты отправил <b>свой</b> контакт {phone}.')


async def get_fake_contact(message: Message):
    await message.answer(f'Ты отправил <b>не свой</b> контакт.')
