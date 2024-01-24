import sys
import asyncio
import logging
from datetime import datetime, timedelta

import asyncpg
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart

from core.handlers.basic import get_start, get_photo, get_location, get_inline
from core.handlers.contact import get_true_contact, get_fake_contact
from core.handlers.callback import select_macbook
from core.handlers.pay import order, pre_checkout_query, successful_payment, shipping_check
from core.handlers import form
from core.handlers import apsched

from core.filters.iscontact import IsTrueContact

from core.utils.commands import set_commands
from core.utils.callbackdata import MacInfo
from core.utils.statesform import StepsForm

from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschedulermiddleware import SchedulerMiddleware

token = config('BOT_TOKEN')
admin_id = config('ADMIN_ID')


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(admin_id, text='Бот остановлен!')


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='postgres', database='users',
                                     host='127.0.0.1', port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=token, parse_mode='HTML')

    pool_connect = await create_pool()
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                      kwargs={'bot': bot})
    scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour,
                      minute=datetime.now().minute + 1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()

    dp = Dispatcher()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(OfficeHoursMiddleware())

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
    dp.message.register(form.get_form, Command(commands='form'))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
