# handlers/user_handlers.py
from aiogram import types
from aiogram.filters import Command
from database import UserDatabase

async def cmd_start(message: types.Message):
    print(f"✅ /start получен от {message.from_user.id}")
    try:
        # Проверяем, есть ли игрок в базе (Firebase)
        user_data = await UserDatabase.get_user(str(message.from_user.id))
        print(f"🔍 Результат запроса к Firebase: {user_data}")
        if user_data:
            # Игрок найден
            current_faction = user_data.get("faction", "Неизвестно")
            await message.answer(
                f"👋 С возвращением, {message.from_user.first_name}!\n"
                f"Ты играешь за фракцию **{current_faction.title()}**.\n"
                "Используй /profile или /city, чтобы посмотреть свой город.",
                parse_mode="Markdown"
            )
        else:
            # Игрок не найден — показываем выбор
            await message.answer(
                f"🔥 Добро пожаловать в *Академию Стихий*, {message.from_user.first_name}!\n\n"
                "Выбери свою стихию и начни строить свою академию магов:\n\n"
                "🔥 /fire — Огонь\n"
                "💧 /water — Вода\n"
                "🌪️ /wind — Ветер\n"
                "🌿 /earth — Земля",
                parse_mode="Markdown"
            )
    except Exception as e:
        print(f"❌ Ошибка в /start: {e}")
        await message.answer("❌ Произошла ошибка. Попробуй позже.")

async def select_faction(message: types.Message):
    try:
        faction = message.text[1:]  # /fire → "fire"
        user_id = str(message.from_user.id)
        username = message.from_user.username or message.from_user.first_name
        print(f"🔧 Выбор фракции: {faction} для пользователя {user_id}")

        # Проверяем, есть ли игрок в базе
        user_data = await UserDatabase.get_user(user_id)

        if user_data:
            current_faction = user_data.get("faction", "Неизвестно")
            await message.answer(
                f"⚠️ Ты уже играешь за **{current_faction.title()}**.\n"
                "Смена фракции не предусмотрена (пока что 😉)."
            )
            return

        # Сохраняем нового игрока в Firebase
        new_user = await UserDatabase.create_user(user_id, username, faction)

        if new_user:
            print(f"✅ Игрок {user_id} добавлен в базу: {new_user}")

            # Эмодзи для фракций
            emojis = {"fire": "🔥", "water": "💧", "wind": "🌪️", "earth": "🌿"}
            emoji = emojis.get(faction, "🧙‍♂️")

            await message.answer(
                f"{emoji} Ты выбрал фракцию **{faction.title()}**!\n\n"
                "🎉 Поздравляем! Твой путь мага начинается.\n"
                "Теперь ты можешь строить здания, нанимать магов и сражаться!\n\n"
                "Используй /profile или /city, чтобы посмотреть свой город.",
                parse_mode="Markdown"
            )
        else:
            raise Exception("Не удалось создать пользователя")

    except Exception as e:
        print(f"❌ Ошибка в select_faction: {e}")
        await message.answer("❌ Ошибка при выборе фракции. Попробуй позже.")