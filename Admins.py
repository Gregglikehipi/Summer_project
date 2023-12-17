from Managers import Manager
from keyboards import get_start_for_admin, get_start
from bot import bot
from datetime import datetime
from DBHelper import DBHelper

class Admin(Manager):
    def __init__(self, name):
        super().__init__(name)
        self.name = name




def for_admin_password(message):
    password = message.text
    if password == 'Админ':
        kb = get_start_for_admin()
        date = datetime.today().strftime('%Y-%m-%d')
        DBHelper("recipe.db").insert('user', ['username', 'password', 'tokens', 'role', 'creation_date'], [message.chat.id, 'Админ', '10000', 'Admin', date])
        bot.send_message(message.chat.id, 'Вы успешно авторизованы! Выберите дальнейшее действие:', reply_markup=kb)
    elif password == '/start':
        kb = get_start()
        bot.send_message(message.chat.id, 'Вы вернулись в начальное меню! Представьтесь ещё раз:', reply_markup=kb)

    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Поробуйте ещё раз')
        bot.register_next_step_handler(message, get_start_for_admin)