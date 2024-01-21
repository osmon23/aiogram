from decouple import config

from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

provider_token = config('PROVIDER_TOKEN')


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка через Telegram бот.',
        description='Учимся принимать платежи через Telegram бот.',
        payload='Payment through a bot',
        provider_token=provider_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Доступ к секретной информации',
                amount=99000,
            ),
            LabeledPrice(
                label='НДС',
                amount=20000,
            ),
            LabeledPrice(
                label='Скидка',
                amount=-20000,
            ),
            LabeledPrice(
                label='Бонус',
                amount=-40000,
            ),
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter='parser-ozon',
        provider_data=None,
        photo_url='https://i.ibb.co/zGw5X0B/image.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15,
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = (f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.'
           f'\r\nНаш менеджер получил заявку и уже набирает ваш номер телефона.'
           f'\r\nПока можете скачать цифровую версию нашего продукта https://nztcoder.com')
    await message.answer(msg)
