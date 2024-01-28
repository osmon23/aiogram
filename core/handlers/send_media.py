from aiogram import Bot
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo


async def get_audio(message: Message, bot: Bot):
    audio = FSInputFile(path=r'/home/osmon/Downloads/Telegram Desktop/REDZED - RAVE IN THE GRAVE')
    await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(path=r'/home/osmon/Documents/CV.odt')
    await bot.send_document(message.chat.id, document=document, caption='It\'s document')


async def get_media_group(message: Message, bot: Bot):
    ph_1 = InputMediaPhoto(type='photo', media=FSInputFile(r'/home/osmon/Documents/photo_cv.jpg'),
                           caption='It\'s mediagroup')
    ph_2 = InputMediaPhoto(type='photo', media=FSInputFile(r'/home/osmon/Documents/photo_cv.jpg'))
    vid = InputMediaVideo(type='video',
                          media=FSInputFile(r'/home/osmon/Downloads/Telegram Desktop/IMG_7683.MP4'))
    media = [ph_1, ph_2, vid]
    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(path=r'/home/osmon/Documents/photo_cv.jpg')
    await bot.send_photo(message.chat.id, photo=photo, caption='It\'s photo')


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(path=r'/home/osmon/Pictures/Screenshots/sticker.webm')
    await bot.send_sticker(message.chat.id, sticker=sticker)


async def get_video(message: Message, bot: Bot):
    video = FSInputFile(path=r'/home/osmon/Videos/Screencasts/Screencast from 11.01.2024 03:00:56.webm')
    await bot.send_video(message.chat.id, video=video, caption='It\'s video')


async def get_video_note(message: Message, bot: Bot):
    video_note = FSInputFile(path=r'/home/osmon/Videos/Screencasts/Screencast from 11.01.2024 03:00:56.webm')
    await bot.send_video_note(message.chat.id, video_note=video_note)


async def get_voice(message: Message, bot: Bot):
    voice = FSInputFile(path=r'/home/osmon/Downloads/Telegram Desktop/REDZED - RAVE IN THE GRAVE')
    await bot.send_voice(message.chat.id, voice=voice)
