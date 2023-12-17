from Users import User
from keyboards import get_start_for_manager, get_start
from datetime import datetime
from bot import bot
from DBHelper import DBHelper



class Manager(User):
    def __init__(self, name):
        super().__init__(name)
        self.name = name




def for_manager_password(message):
    password = message.text
    if password == 'Менеджер':
        kb = get_start_for_manager()
        date = datetime.today().strftime('%Y-%m-%d')
        DBHelper("recipe.db").insert('user', ['username', 'password', 'tokens', 'role', 'creation_date'],
                      [message.chat.id, 'Менеджер', '500', 'Manager', date])
        bot.send_message(message.chat.id, 'Вы успешно авторизованы! Выберите дальнейшее действие:', reply_markup=kb)
    elif password == '/start':
        kb = get_start()
        bot.send_message(message.chat.id, 'Вы вернулись в начальное меню! Представьтесь ещё раз:', reply_markup=kb)

    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Поробуйте ещё раз')
        bot.register_next_step_handler(message, for_manager_password)