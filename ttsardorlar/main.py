from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputMediaPhoto, InputMediaVideo
import logging

API_TOKEN = '7550928148:AAHV2KfyrZcoOaTvx-xadVehQh-f3XV-4Ks'
CHANNEL_ID = '@americauzuz'
ADMIN_ID = 1921911753


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

user_media = {}


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    await message.reply(f"<i>Salom Hurmatli <b><a href='tg://user?id={user_id}'>{full_name}👋</a></b>\nToshkent tumani botiga xush kelibsiz\nYangi yil bezagi tanlovi🏆 uchun loyihangizni🎥 (rasm yoki video) yuboring Omad yor bo'lsin😊</i>")


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO])
async def collect_media(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_media:
        user_media[user_id] = {'media': [], 'caption': '', 'notified': False}

    if message.photo:
        user_media[user_id]['media'].append(InputMediaPhoto(media=message.photo[-1].file_id))
    elif message.video:
        user_media[user_id]['media'].append(InputMediaVideo(media=message.video.file_id))

    if message.caption:
        if user_media[user_id]['caption']:
            user_media[user_id]['caption'] += f"\n{message.caption}"
        else:
            user_media[user_id]['caption'] = message.caption

    if not user_media[user_id]['notified']:
        await message.answer("Loyihangiz qabul qilindi✅. Agar hammasi tayyor bo'lsa, /send buyrug'ini yuboring.")
        user_media[user_id]['notified'] = True


@dp.message_handler(commands=['send'])
async def send_to_channel(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_media or not user_media[user_id]['media']:
        await message.answer("Hech qanday Loyiha yuborilmadi❌. Iltimos, avval loyihangizni yuboring!")
        return

    media_group = user_media[user_id]['media']
    if user_media[user_id]['caption']:
        media_group[0].caption = user_media[user_id]['caption']
        media_group[0].parse_mode = 'HTML'

    try:
        await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
        await message.answer("<b>Sizning loyihangiz kanalga yuborildi✅\nOmad😊</b>")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}\nAdmin bilan bog'laning <b><a href='tg://user?id={1921911753}'>Mutalov Nuriddin</a></b>")

    user_media[user_id] = {'media': [], 'caption': '', 'notified': False}



@dp.message_handler(commands=['send'])
async def send_to_channel(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_media or not user_media[user_id]['media']:
        await message.reply("Hech qanday loyiha yuborilmadi❌. Iltimos, avval loyiha yuboring!")
        return

    media_group = user_media[user_id]['media']
    caption = user_media[user_id]['caption']

    try:
        if caption:
            media_group[0].caption = caption
            media_group[0].parse_mode = 'HTML'

        await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
        await message.reply("Loyihangiz kanalga muvaffaqiyatli joylashtirildi✅")
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.reply(f"Loyihangizni kanalga yuborishda xatolik yuz berdi.\nAdmin bilan bog'laning <b><a href='tg://user?id={1921911753}'>Mutalov Nuriddin</a></b>")

    user_media[user_id] = {'media': [], 'caption': ''}


@dp.message_handler()
async def handle_other_messages(message: types.Message):
    await message.reply("Iltimos, loyiha sifatida rasm, video yuboring va /send buyrug‘idan foydalaning.")


async def on_startup(dp):
    """Bot ishga tushganda."""
    await bot.send_message(chat_id=ADMIN_ID, text='Bot ishga tushdi!')


async def on_shutdown(dp):
    """Bot o'chirilganda."""
    await bot.send_message(chat_id=ADMIN_ID, text="Bot o'chdi!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
