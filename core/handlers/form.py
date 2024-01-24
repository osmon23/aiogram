from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.utils.statesform import StepsForm
from core.handlers.apsched import send_message_middleware


async def get_form(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.full_name}, начинаем заполнять анкету. Введи свое имя')
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Твое имя:\r\n{message.text}\r\nТеперь введи фамилию')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LAST_NAME)


async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f'Твоя фамилия:\r\n{message.text}\r\nТеперь введи возраст')
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_AGE)


async def get_age(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    await message.answer(f'Твой возраст:\r\n{message.text}\r\n')
    context_data = await state.get_data()
    await message.answer(f'Сохраненные данные в машине состоянии\r\n{str(context_data)}')
    name = context_data.get('name')
    last_name = context_data.get('last_name')
    data_user = (f'Вот твои данные\r\n'
                 f'Имя: {name}\r\n'
                 f'Фамилия: {last_name}\r\n'
                 f'Возраст: {message.text}\r\n')
    await message.answer(data_user)
    await state.clear()
    apscheduler.add_job(send_message_middleware, trigger='date', run_date=datetime.now() + timedelta(seconds=60),
                        kwargs={'chat_id': message.from_user.id})
