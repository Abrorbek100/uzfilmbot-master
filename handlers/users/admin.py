import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import types

from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    print(users[0][0])
    await message.answer(users)

# @dp.message_handler(text="/reklama", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message):
#     users = db.select_all_users()
#     for user in users:
#         user_id = user[0]
#         await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
#         await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")

@dp.message_handler(text='/reklama' , user_id=ADMINS)
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Reklama postiga id ni yuboring")
    await state.set_state("reklama")


@dp.message_handler(state="reklama")
async def enter_rek(message: types.Message, state: FSMContext):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=-1001515575124, message_id=message.text)
            await asyncio.sleep(0.05)

        except:
            await bot.send_message(chat_id=5422565585, text='error')

        await state.finish()