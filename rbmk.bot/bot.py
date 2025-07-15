from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
import commands  # Импорт всего модуля

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
dp.register_message_handler(commands.start_cmd, commands=["start"])
dp.register_message_handler(commands.mine_cmd, commands=["mine"])
dp.register_message_handler(commands.prestige_cmd, commands=["prestige"])
dp.register_message_handler(commands.inventory_cmd, commands=["inventory"])
#dp.register_message_handler(commands.load_rbmk_cmd, commands=["load_rbmk"])
#dp.register_message_handler(commands.start_rbmk_cmd, commands=["start_rbmk"])
#dp.register_message_handler(commands.sell_energy_cmd, commands=["sell_energy"])
#dp.register_message_handler(commands.give_item_cmd, commands=["give_item"])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)