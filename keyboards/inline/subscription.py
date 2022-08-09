from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_button = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Obunani bo'lish", url="https://t.me/myeterniiity"),

        InlineKeyboardButton(text="Obunani tekshirish ✅", callback_data="check_subs")
    ]]
)
