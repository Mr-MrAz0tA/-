import json
import os
from pathlib import Path

STARTING_URANIUM = 10
SAVES_DIR = Path("saves")

def ensure_user_folder(user_id):
    user_dir = SAVES_DIR / f"user_{user_id}"
    user_dir.mkdir(exist_ok=True, parents=True)
    return user_dir

def load_user_data(user_id):
    user_file = SAVES_DIR / f"user_{user_id}.json"
    try:
        with open(user_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Создаем нового игрока
        default_data = {
            "user_id": user_id,
            "level": 1,
            "prestige": 0,
            "admin": False,
            "money": 0,
            "inventory": {
                "uranium_raw": STARTING_URANIUM,
                "uranium_235": 0,
                "plutonium_239": 0,
                "thorium": 0,
                "energy_kwt": 0
            },
            "rbmk": {
                "loaded_fuel": None,
                "loaded_amount": 0,
                "is_active": False
            },
            "perks": []
        }
        save_user_data(user_id, default_data)
        return default_data

def save_user_data(user_id, data):
    user_file = SAVES_DIR / f"user_{user_id}.json"
    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def is_admin(user_id):
    user_data = load_user_data(user_id)
    return user_data.get("admin", False)