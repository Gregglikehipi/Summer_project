from keyboards import get_start_for_user
from datetime import datetime
from bot import bot
from DBHelper import DBHelper


class User:
    def __init__(self, name):
        self.name = name




def for_user(id_user):
    kb = get_start_for_user()
    date = datetime.today().strftime('%Y-%m-%d')
    DBHelper("recipe.db").insert('user', ['username', 'tokens', 'role', 'creation_date'],
                  [str(id_user), '10', 'User', date])
    bot.send_message(id_user, 'Привет! Я , твой личный помощник на кухне 👨‍🍳, помогу подобрать рецепты под '
                              'имеющиеся продукты!📋 Скорее жми "Подборка рецептов📃"!', reply_markup=kb)