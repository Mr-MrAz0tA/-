import time
from datetime import datetime, timedelta
from database import load_user_data, save_user_data

class RBMK:
    FUEL_EFFICIENCY = {
        "uranium_235": 10,  # МВт/10кг
        "plutonium_239": 15,
        "californium_252": 200
    }
    
    def load_fuel(self, user_id, fuel_type, amount):
        user_data = load_user_data(user_id)
        inv = user_data["inventory"]
        
        if fuel_type not in inv or inv[fuel_type] < amount:
            return False
        
        inv[fuel_type] -= amount
        user_data["rbmk"]["loaded_fuel"] = fuel_type
        user_data["rbmk"]["loaded_amount"] = amount
        save_user_data(user_id, user_data)
        return True
    
    def start_generation(self, user_id):
        user_data = load_user_data(user_id)
        rbmk = user_data["rbmk"]
        
        if not rbmk["loaded_fuel"]:
            return False
        
        efficiency = self.FUEL_EFFICIENCY.get(rbmk["loaded_fuel"], 10)
        energy = (efficiency * (rbmk["loaded_amount"] / 10)) * 300  # 5 минут
        
        user_data["rbmk"]["is_active"] = True
        user_data["rbmk"]["start_time"] = datetime.now().isoformat()
        user_data["rbmk"]["end_time"] = (datetime.now() + timedelta(minutes=5)).isoformat()
        save_user_data(user_id, user_data)
        
        return energy