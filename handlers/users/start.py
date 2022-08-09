import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import CHANNELS
from keyboards.inline.subscription import check_button

from data.config import ADMINS
from loader import dp, db, bot
from utils.misc import subscription


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
                    # Adminga xabar beramiz
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=msg)
    except sqlite3.IntegrityError as err:
        pass

    for channel in CHANNELS:
        status = await subscription.check(user_id=message.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            await message.answer("Botga xush kelibsiz!\n Bu bot orqali siz kino kodi orqali kinoni topishingiz mumkin. Kerakli filmingiz uchun kodni yuboring")

        else:
            channels_format = str()
            for channel in CHANNELS:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                # logging.info(invite_link)
                channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
                await message.answer(f"Xush kelibsiz! Botdan foydalanish uchun quyidagi kanalga obuna bo'ling: \n",
                reply_markup=check_button,
                disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)
