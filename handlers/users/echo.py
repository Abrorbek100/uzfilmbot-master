from aiogram import types
from data.config import ADMINS
from loader import dp , bot


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    try:
        await bot.copy_message(chat_id=message.chat.id , from_chat_id=-1001515575124, message_id=message.text)

    except:
        for admin in ADMINS:
            user=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
            await bot.send_message(chat_id=admin, text=f'{user}\n{message.text}')
