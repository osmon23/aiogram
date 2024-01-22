import sys
import asyncio
import logging

from decouple import config
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart

from core.handlers.basic import get_start, get_photo, get_location, get_inline
from core.handlers.contact import get_true_contact, get_fake_contact
from core.handlers.callback import select_macbook
from core.handlers.pay import order, pre_checkout_query, successful_payment, shipping_check
from core.filters.iscontact import IsTrueContact
from core.utils.commands import set_commands
from core.utils.callbackdata import MacInfo

token = config('BOT_TOKEN')
admin_id = config('ADMIN_ID')


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(admin_id, text='Бот остановлен!')


async def start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=token, parse_mode='HTML')

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, CommandStart())
    # dp.message.register(get_photo, F.content_type == 'photo')
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.message.register(get_location, F.location)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.callback_query.register(select_macbook, MacInfo.filter())  # MacInfo.filter(F.model == 'pro')
    dp.message.register(order, Command(commands='pay'))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)
    dp.shipping_query.register(shipping_check)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
