from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def open_city(message: types.Message):
    user_id = message.from_user.id
    # УБРАТЬ лишние пробелы в начале этой строки!
    web_app_url = f"https://academy-of-elements.vercel.app/?user_id={user_id}"

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Открыть город 🏰",
        web_app=types.WebAppInfo(url=web_app_url)
    )

    await message.answer(
        "Твой город ждёт тебя! Нажми кнопку ниже, чтобы войти в академию.",
        reply_markup=builder.as_markup()
    )