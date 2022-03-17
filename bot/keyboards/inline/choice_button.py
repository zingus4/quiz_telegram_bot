from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="да", callback_data="answer:yes"),
            InlineKeyboardButton(text="нет", callback_data="answer:no")
        ]
    ]
)

