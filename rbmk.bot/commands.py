import random
from aiogram import types
from database import load_user_data, save_user_data, is_admin
from rbmk_logic import RBMK

rbmk = RBMK()

async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)
    
    text = (
        f"⚡ Добро пожаловать в симулятор РБМК!\n"
        f"Уровень: {user_data['level']}\n"
        f"Престиж: {user_data['prestige']}\n"
        f"Баланс: {user_data['money']} ₽\n"
        f"Уран: {user_data['inventory']['uranium_raw']} кг"
    )
    await message.reply(text)

async def mine_cmd(message: types.Message):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)
    
    # Логика добычи
    mined = random.randint(3, 50) * (user_data['prestige'] + 1)
    user_data['inventory']['uranium_raw'] += mined
    save_user_data(user_id, user_data)
    
    await message.reply(f"⛏️ Вы добыли {mined} кг урана!")

async def prestige_cmd(message: types.Message):
    user_id = message.from_user.id
    user_data = load_user_data(user_id)
    
    required_level = 20 + (user_data["prestige"] * 10)
    if user_data["level"] < required_level:
        return await message.reply(f"❌ Нужен {required_level} уровень!")
    
    if user_data["prestige"] >= 5:
        return await message.reply("❌ Максимальный престиж достигнут!")
async def inventory_cmd(message: types.Message):
    user_data = load_user_data(message.from_user.id)
    inv = user_data["inventory"]

    text ="📦 Ваш инвентарь: \n"
    text += f"💵 Деньги: {inv['money']} ₽\n"
    text += f"⚡ Энургия: {inv['energy']} кВТ\n\n"
    text += "🔹 Топливо:\n"
    for fuel, amount in inv ["fuels"]:
        text += f"- {fuel}: {amount} кг\n"
    text += "\n🔹 Материалы:\n"
    for mat, amount in inv["materials"].items():
        text += f"- {mat}: {amount} шт"

        await message.reply(text)

    async def give_item_cmd(message: types.message):
     """Админ-команда для выдачи предметов"""
    if not is_admin(message.from_user.id):
        return

    try:
        _, user_id, item_type, item_name, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
        
        user_data = load_user_data(user_id)
        
        # Инициализация структуры данных
        if "inventory" not in user_data:
            user_data["inventory"] = {}
        if item_type == "fuel":
            if "fuels" not in user_data["inventory"]:
                user_data["inventory"]["fuels"] = {}
            user_data["inventory"]["fuels"][item_name] = user_data["inventory"]["fuels"].get(item_name, 0) + amount
        elif item_type == "mat":
            if "materials" not in user_data["inventory"]:
                user_data["inventory"]["materials"] = {}
            user_data["inventory"]["materials"][item_name] = user_data["inventory"]["materials"].get(item_name, 0) + amount
        
        save_user_data(user_id, user_data)
        await message.reply(f"✅ Выдано {amount} {item_name} игроку {user_id}")
    
    except Exception as e:
        await message.reply(f"❌ Ошибка: {str(e)}\nФормат: /give <ID> <fuel/mat> <название> <количество>")

    # Сброс прогресса
    new_data = {
        "user_id": user_id,
        "level": 1,
        "prestige": user_data["prestige"] + 1,
        "money": 0,
        "inventory": {"uranium_raw": 10},
        "rbmk": {"loaded_fuel": None, "loaded_amount": 0, "is_active": False},
        "perks": [],
        "admin": user_data.get("admin", False)
    }
    save_user_data(user_id, new_data)

    def add_to_inventory(user_id, item_type, item_name, amount):
     """Универсальная функция добавления предметов"""
    user_data = load_user_data(user_id)
    if item_type == "energy":
        user_data["inventory"]["energy"] += amount
    elif item_type == "money":
        user_data["inventory"]["money"] += amount
    elif item_type in ["fuels", "materials"]:
        user_data["inventory"][item_type][item_name] += amount
    save_user_data(user_id, user_data)

def remove_from_inventory(user_id, item_type, item_name, amount):
    """Универсальная функция удаления предметов"""
    user_data = load_user_data(user_id)
    if user_data["inventory"][item_type].get(item_name, 0) >= amount:
        user_data["inventory"][item_type][item_name] -= amount
        save_user_data(user_id, user_data)
        return True
    return False
    
async def send_reaply(message):
    await message.reply(
        f"🎉 Престиж {new_data['prestige']} получен!\n"
        f"Бонусы: x{new_data['prestige'] + 1} к деньгам и добыче\n"
        f"Макс. уровень: {20 + (new_data['prestige'] * 10)}"
        )