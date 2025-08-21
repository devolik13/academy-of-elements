# handlers/wizard_handlers.py
from aiogram import types
from database import UserDatabase
from buildings_config import BUILDINGS_DATA

async def cmd_profile(message: types.Message):
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
             await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
             return

        faction = user_data.get("faction", "Неизвестно")
        emojis = {"fire": "🔥", "water": "💧", "wind": "🌪️", "earth": "🌿"}
        emoji = emojis.get(faction, "🧙‍♂️")

        # Форматируем дату создания
        created_at = user_data.get("created_at", "Неизвестно")
        if isinstance(created_at, dict) and ".sv" in created_at:
            created_date = "Только что"
        elif created_at:
            # Если это timestamp, конвертируем в читаемый формат
            from datetime import datetime
            try:
                # Предполагаем, что timestamp в миллисекундах
                dt = datetime.fromtimestamp(created_at / 1000)
                created_date = dt.strftime("%Y-%m-%d")
            except:
                created_date = str(created_at)[:10]
        else:
            created_date = "Неизвестно"

        # Формируем информацию о магах
        wizards_info = "\n🧙‍♂️ **Маги:**\n"
        wizards = user_data.get("wizards", [])
        if wizards:
            for wizard in wizards:
                wizard_name = wizard.get("name", "Безымянный")
                wizard_faction = wizard.get("faction", "Неизвестно")
                wizard_spells_ids = wizard.get("spells", [])
                
                # Получаем названия заклинаний
                spell_names = []
                available_spells = user_data.get("spells", {}).get(wizard_faction, {})
                for spell_id in wizard_spells_ids:
                    spell_info = available_spells.get(spell_id, {})
                    spell_name = spell_info.get("name", spell_id)
                    spell_level = spell_info.get("level", 1)
                    spell_names.append(f"{spell_name} (ур. {spell_level})")
                
                wizards_info += f"  • {wizard_name} ({wizard_faction.title()}): {', '.join(spell_names) if spell_names else 'Нет заклинаний'}\n"
        else:
            wizards_info += "  Нет магов\n"

        # Формируем информацию об исследованиях
        research_info = "\n🔬 **Исследования:**\n"
        research = user_data.get("research", {})
        if research.get("active", False):
            spell_id = research.get("spell")
            target_level = research.get("target_level")
            time_left = research.get("time_left", 0)
            faction_bonus = research.get("faction_bonus", False)
            
            # Найдем название заклинания
            spell_name = "Неизвестное заклинание"
            spell_tier = 1
            for fact, spells_dict in user_data.get("spells", {}).items():
                if spell_id in spells_dict:
                    spell_info = spells_dict[spell_id]
                    spell_name = spell_info.get("name", spell_id)
                    spell_tier = spell_info.get("tier", 1)
                    break
            
            faction_text = "своей фракции" if faction_bonus else "чужой фракции"
            research_info += f"  • {spell_name} (Ступень {spell_tier}) → Уровень {target_level} ({faction_text}, {time_left} дней осталось)\n"
        else:
            research_info += "  Нет активных исследований\n"
            
        # Формируем информацию о строительстве
        construction_info = "\n🏗️ **Строительство:**\n"
        construction = user_data.get("construction", {})
        if construction.get("active", False):
            building_id = construction.get("building_id")
            target_level = construction.get("target_level")
            time_left = construction.get("time_left", 0)
            construction_type = construction.get("type", "build")
            
            # Получаем название здания
            building_name = "Неизвестное здание"
            building_data = BUILDINGS_DATA.get(building_id)
            if building_data:
                building_name = building_data.get("name", building_id)
            
            type_text = "постройка" if construction_type == "build" else "улучшение"
            target_text = f"до уровня {target_level}" if construction_type == "upgrade" else ""
            
            construction_info += f"  • {building_name} ({type_text} {target_text}, {time_left} дней осталось)\n"
        else:
            construction_info += "  Нет активных построек\n"

        # Формируем информацию о найме магов (временно, пока нет системы времени)
        # hire_info = "\n🧙‍♂️ **Найм магов:**\n"
        # hire_info += "  Используй /hire_wizard для найма нового мага.\n"
        # Временно показываем количество магов
        wizards_count = len(wizards)
        wizards_summary = f"\n🧙‍♂️ **Маги:** {wizards_count}\n"

        await message.answer(
            f"{emoji} **Профиль игрока**\n\n"
            f"🔹 Фракция: **{faction.title()}**\n"
            f"📅 Создан: {created_date}"
            f"{wizards_summary}" # Используем краткую информацию о магах
            f"{research_info}"
            f"{construction_info}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"❌ Ошибка в /profile: {e}")
        import traceback
        traceback.print_exc() # Для отладки
        await message.answer("❌ Ошибка загрузки профиля.")

async def cmd_wizards(message: types.Message):
    """Показать список магов игрока"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        wizards = user_data.get("wizards", [])
        if not wizards:
            await message.answer("🧙‍♂️ У тебя пока нет магов. Используй /hire_wizard, чтобы нанять!")
            return

        response_text = "🧙‍♂️ **Твои маги:**\n\n"
        for i, wizard in enumerate(wizards, 1):
            wizard_name = wizard.get("name", f"Маг {i}")
            wizard_faction = wizard.get("faction", "Неизвестно").title()
            
            # Получаем заклинания мага
            wizard_spells_ids = wizard.get("spells", [])
            spell_info_list = []
            
            # Получаем информацию о заклинаниях из userData
            all_spells = user_data.get("spells", {})
            for spell_id in wizard_spells_ids:
                # Ищем заклинание во всех фракциях
                found_spell = None
                found_faction = None
                for faction_key, faction_spells in all_spells.items():
                    if spell_id in faction_spells:
                        found_spell = faction_spells[spell_id]
                        found_faction = faction_key
                        break
                
                if found_spell:
                    spell_name = found_spell.get("name", spell_id)
                    spell_level = found_spell.get("level", 1)
                    spell_tier = found_spell.get("tier", 1)
                    spell_info_list.append(f"{spell_name} (С{spell_tier} У{spell_level})")
                else:
                    spell_info_list.append(f"{spell_id} (Неизвестно)")
            
            spells_text = ", ".join(spell_info_list) if spell_info_list else "Нет заклинаний"
            response_text += f"{i}. **{wizard_name}** ({wizard_faction})\n"
            response_text += f"   Заклинания: {spells_text}\n\n"

        await message.answer(response_text, parse_mode="Markdown")

    except Exception as e:
        print(f"❌ Ошибка в /wizards: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при получении списка магов.")

async def cmd_spells(message: types.Message):
    """Показать список изученных заклинаний"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        all_spells = user_data.get("spells", {})
        available_spells = user_data.get("available_spells", [])
        
        if not any(all_spells.values()):  # Проверяем, есть ли хотя бы одно заклинание
            await message.answer("📖 У тебя пока нет изученных заклинаний.")
            return

        response_text = "📖 **Твои заклинания:**\n\n"
        
        # Словарь для перевода фракций
        faction_names = {
            "fire": "🔥 Огонь",
            "water": "💧 Вода", 
            "wind": "🌪️ Ветер",
            "earth": "🌿 Земля"
        }
        
        for faction_key, faction_spells in all_spells.items():
            if faction_spells:  # Если есть заклинания у этой фракции
                faction_display = faction_names.get(faction_key, faction_key.title())
                response_text += f"**{faction_display}:**\n"
                
                for spell_id, spell_info in faction_spells.items():
                    spell_name = spell_info.get("name", spell_id)
                    spell_level = spell_info.get("level", 1)
                    spell_tier = spell_info.get("tier", 1)
                    availability = "✅" if spell_id in available_spells else "🔒"
                    
                    response_text += f"  {availability} {spell_name} (Ступень {spell_tier}, Уровень {spell_level})\n"
                response_text += "\n"

        # Добавляем информацию о доступных для изучения заклинаниях
        response_text += "✅ - Доступно для использования\n"
        response_text += "🔒 - В процессе изучения\n"

        await message.answer(response_text, parse_mode="Markdown")

    except Exception as e:
        print(f"❌ Ошибка в /spells: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при получении списка заклинаний.")

async def cmd_research(message: types.Message):
    """Показать текущее исследование или начать новое"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        research = user_data.get("research", {})
        
        if research.get("active", False):
            # Есть активное исследование
            spell_id = research.get("spell")
            target_level = research.get("target_level")
            time_left = research.get("time_left", 0)
            faction_bonus = research.get("faction_bonus", False)
            
            # Найдем название заклинания
            spell_name = "Неизвестное заклинание"
            spell_tier = 1
            for fact, spells_dict in user_data.get("spells", {}).items():
                if spell_id in spells_dict:
                    spell_info = spells_dict[spell_id]
                    spell_name = spell_info.get("name", spell_id)
                    spell_tier = spell_info.get("tier", 1)
                    break
            
            faction_text = "своей фракции" if faction_bonus else "чужой фракции"
            await message.answer(
                f"🔬 **Активное исследование:**\n\n"
                f"Заклинание: **{spell_name}** (Ступень {spell_tier})\n"
                f"Цель: Уровень {target_level}\n"
                f"Осталось времени: {time_left} дней\n"
                f"Тип: {faction_text}\n\n"
                f"Используй /cancel_research для отмены.",
                parse_mode="Markdown"
            )
        else:
            # Нет активного исследования - предлагаем начать
            await message.answer(
                f"🔬 **Лаборатория исследований**\n\n"
                f"У тебя нет активных исследований.\n\n"
                f"Доступные действия:\n"
                f"• Улучшить заклинание своей фракции\n"
                f"• Изучить заклинание другой фракции\n\n"
                f"Используй команду в формате:\n"
                f"`/research upgrade <spell_id>` - улучшить заклинание\n"
                f"`/research learn <faction> <spell_id>` - изучить новое заклинание\n"
                f"Пример: `/research upgrade spark`\n"
                f"Пример: `/research learn water icicle`",
                parse_mode="Markdown"
            )

    except Exception as e:
        print(f"❌ Ошибка в /research: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при работе с исследованиями.")

async def cmd_cancel_research(message: types.Message):
    """Отменить текущее исследование"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        research = user_data.get("research", {})
        
        if not research.get("active", False):
            await message.answer("❌ У тебя нет активных исследований для отмены.")
            return

        # Отменяем исследование
        await UserDatabase.update_research(user_id, {
            "active": False,
            "spell": None,
            "target_level": None,
            "time_left": 0,
            "faction_bonus": False
        })
        
        await message.answer("✅ Активное исследование отменено.")

    except Exception as e:
        print(f"❌ Ошибка в /cancel_research: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при отмене исследования.")

async def cmd_hire_wizard(message: types.Message):
    """Нанять нового мага (временно мгновенно)"""
    try:
        user_id = str(message.from_user.id)
        user_data = await UserDatabase.get_user(user_id)
        if not user_data:
            await message.answer("❌ Ты ещё не зарегистрирован. Напиши /start")
            return

        # Получаем текущее количество магов
        wizards = user_data.get("wizards", [])
        wizards_count = len(wizards)
        
        # Создаем нового мага
        new_wizard_id = f"wizard_{wizards_count + 1}"
        user_faction = user_data.get("faction", "fire")
        
        # Определяем начальное заклинание для нового мага (берем первое доступное своей фракции)
        initial_spell = None
        user_spells = user_data.get("spells", {}).get(user_faction, {})
        available_spells = user_data.get("available_spells", [])
        
        # Ищем первое доступное заклинание своей фракции
        for spell_id in user_spells:
            if spell_id in available_spells:
                initial_spell = spell_id
                break
        
        if not initial_spell and user_spells:
            # Если нет доступных, берем первое изученное
            initial_spell = next(iter(user_spells), None)
        
        wizard_data = {
            "id": new_wizard_id,
            "name": f"Маг {wizards_count + 1}",
            "faction": user_faction,
            "spells": [initial_spell] if initial_spell else []
        }

        # Добавляем мага
        success = await UserDatabase.add_wizard(user_id, wizard_data)
        
        if success:
            await message.answer(
                f"✅ Ты успешно нанял нового мага!\n"
                f"Имя: **{wizard_data['name']}**\n"
                f"Фракция: {user_faction.title()}\n",
                parse_mode="Markdown"
            )
        else:
            await message.answer("❌ Ошибка при найме мага.")

    except Exception as e:
        print(f"❌ Ошибка в /hire_wizard: {e}")
        import traceback
        traceback.print_exc()
        await message.answer("❌ Ошибка при найме мага.")
