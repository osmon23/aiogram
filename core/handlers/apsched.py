from decouple import config

from aiogram import Bot

admin_id = config('ADMIN_ID')


async def send_message_time(bot: Bot):
    await bot.send_message(admin_id, 'Это сообщение отправляется через несколько секунд после старта.')


async def send_message_cron(bot: Bot):
    await bot.send_message(admin_id, 'Это сообщение отправляется ежедневно в указанное время.')


async def send_message_interval(bot: Bot):
    await bot.send_message(admin_id, 'Это сообщение отправляется с интервалом в одну минуту.')


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, 'Это сообщение отправлено с помощью сформированной через middleware задачи.')
