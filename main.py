import requests
import time
from telebot import types

from Admins import for_admin_password
from Managers import for_manager_password
from Users import for_user
from datetime import datetime
from bot import bot
from DBHelper import DBHelper
from Recipe import Recipe, get_all_recipe, find_recipe_with_categories, find_recipe_with_ingredients, get_random_recipe, test, clear_text, get_recipe, get_recipe_by_manual
from keyboards import get_selection_of_recipes, get_personal_account, get_filters_for_dishes, \
    get_list_of_recipes, get_viewing_a_dish, get_add_to_the_cooked, get_start, get_info_get_balance, get_time_interval, \
    get_caloricity, get_start_for_user, get_category, get_menu, get_cuisines, cuisines, arr_category, arr_menu, kalor, \
    personal_and_favorites, get_start_for_admin, get_selection_of_products, products, get_types_of_meat, \
    get_types_of_vegetables, get_types_of_milk_and_eggs, get_mushrooms, get_nuts, \
    get_fruits_and_berries, get_greenery, get_cereals_legumes_and_flour, com, \
    get_write_a_recipe, get_start2, get_back
from ML import predict

user_state = {}

#print('1')
all_recipe = get_all_recipe()
#test(all_recipe)
print('1')

# @bot.message_handler(commands=["start"])
@bot.message_handler(func=lambda message: message.text == '/start')
def start(m):
    kb = get_start()
    text = ''
    text = m.chat.id
    print(text)
    bot.send_message(m.chat.id, 'Привет!👋🏼 Представься, пожалуйста, кто ты❓🔍', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in ['Пользователь👤', 'Менеджер💼', 'Администратор🔒'])
def handle_role_selection(message):
    role = message.text
    user_state[message.chat.id] = {'role': role}
    if role == 'Администратор🔒':
        bot.send_message(message.chat.id, 'Введите пароль для администратора:')
        bot.register_next_step_handler(message, for_admin_password)
    elif role == 'Менеджер💼':
        # id_manager = message.chat.id
        # man_pass(id_manager)
        # bot.send_message(message.chat.id, 'Введите пароль для менеджера:')
        bot.register_next_step_handler(message, for_manager_password)
        bot.send_message(message.chat.id, 'Введите пароль для менеджера:')
    elif role == 'Пользователь👤':
        id_user = message.chat.id
        for_user(id_user)


@bot.message_handler(func=lambda message: message.text == 'Вернутся в главное меню🏠')
def action_on_the_user(message):
    kb = get_start2()
    bot.send_message(message.chat.id, 'Кто ты❓🔍', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Действие над пользователем👤')
def action_on_the_user(message):
    kb = get_info_get_balance()
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Посмотреть активность📊')
def activity(m):
    bot.send_message(m.chat.id, 'Активность:')
    date = datetime.today().strftime('%Y-%m-%d')
    users = DBHelper("recipe.db").get('user', ['creation_date'], [date])
    bot.send_message(m.chat.id, f'Было активно недавно: {len(users)}')
    # TODO реализовать активноть


@bot.message_handler(func=lambda message: message.text == 'Посмотреть число новых пользователей👥')
def number_of_new_users(m):
    kb = get_time_interval()
    bot.send_message(m.chat.id, 'Выберите временной промежуток:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Действия пользователя🙋‍♂️')
def user_actions(m):
    user_id = m.chat.id
    for_user(user_id)


@bot.message_handler(func=lambda message: message.text == 'Обновить данные о рецептах🔄️')
def update_recipe_data(m):
    bot.send_message(m.chat.id, 'Данные о рецептах обновлены')
    # TODO обновить данные о рецептах


@bot.message_handler(func=lambda message: message.text == 'Посмотреть информация📋')
def view_information(m):
    bot.send_message(m.chat.id, 'Введите id нужного вам пользователя:')
    ids_ = m.text
    user = DBHelper("recipe.db").get('user', ['id'], [ids_])
    if len(user) == 0:
        bot.send_message(m.chat.id, 'Такого пользователя нет')
    if len(user) == 1:
        user_ = user[0]
        if user_[4] == 'User':
            user_[2] = "Null"
        if user_[7] == None:
            user_[7] = "Null"
        text = f"id: {user_[0]}" \
               f"username: {user_[1]}" \
               f"password: {user_[2]}" \
               f"tokens: {user_[3]}" \
               f"role: {user_[4]}" \
               f"creation_date: {user_[5]}" \
               f"last_recipe_id: {user_[6]}"
        bot.send_message(m.chat.id, text)


@bot.message_handler(func=lambda message: message.text == 'На основе избранных❤️')
def get_recipe_like(m):
    recipes = DBHelper("recipe.db").get('recipe_like', ['user_id'], [str(m.chat.id)])
    manuals_like = []
    for rec in recipes:
        recipe_ = get_recipe(all_recipe, rec[2])
        manuals_like.append(recipe_.manual)
    manuals = predict(manuals_like)
    new_recipe = get_recipe_by_manual(all_recipe, manuals[0])
    bot.register_next_step_handler(m, print_recipe(m, new_recipe))


@bot.message_handler(func=lambda message: message.text == 'Изменить баланс тоненов💰')
def change_the_balance_of_tokens(m):
    bot.send_message(m.chat.id, 'Введите id нужного вам пользователя:')
    ids_ = m.text
    bot.send_message(m.chat.id, 'Введите нужный баланс:')
    num = m.text
    DBHelper("recipe.db").update('user', 'id', ids_, 'tokens', num)
    # TODO реализовать


@bot.message_handler(func=lambda message: message.text == '1️⃣ день')
def one_day(m):
    date = datetime.today().strftime('%Y-%m-%d')
    users = DBHelper("recipe.db").get('user', ['creation_date'], [date])
    bot.send_message(m.chat.id, f"Число новых пользователей за день: {len(users)}")

    # TODO показ количества пользователей


@bot.message_handler(func=lambda message: message.text == '1️⃣ неделя')
def one_week(m):
    date = datetime.today().strftime('%Y-%m-%d')
    users = DBHelper("recipe.db").get('user', ['creation_date'], [date])
    bot.send_message(m.chat.id, f"Число новых пользователей за неделю: {len(users)}")
    # TODO показ количества пользователей


@bot.message_handler(func=lambda message: message.text == '1️⃣ месяц')
def one_month(m):
    date = datetime.today().strftime('%Y-%m-%d')
    users = DBHelper("recipe.db").get('user', ['creation_date'], [date])
    bot.send_message(m.chat.id, f"Число новых пользователей за месяц: {len(users)}")
    # TODO показ количества пользователей


@bot.message_handler(func=lambda message: message.text == '1️⃣ год')
def one_year(m):
    date = datetime.today().strftime('%Y-%m-%d')
    users = DBHelper("recipe.db").get('user', ['creation_date'], [date])
    bot.send_message(m.chat.id, f"Число новых пользователей за год: {len(users)}")
    # TODO показ количества пользователей


@bot.message_handler(func=lambda message: message.text == 'Обновить данные о рецептах🔄')
def recipe_data(m):
    kb = get_start_for_admin()
    bot.send_message(m.chat.id, 'Данные о рецептах обновлены:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Подборка рецептов📃')
def selection_of_recipes(message):
    kb = get_selection_of_recipes()
    bot.send_message(message.chat.id, 'Выберите дальнейшнее действие:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Рецепты на день📚️')
def recipes_for_the_day(message):
    bot.send_message(message.chat.id, 'Ваш список рецептов на день:')
    take_token(message.chat.id, 3)
    bot.send_message(message.chat.id, 'Завтрак')
    recipe_ = get_random_recipe(find_recipe_with_categories(all_recipe, ['Завтраки']))
    bot.register_next_step_handler(message, print_recipe(message, recipe_))
    bot.send_message(message.chat.id, 'Обед')
    recipe_ = get_random_recipe(find_recipe_with_categories(all_recipe, ['Супы']))
    bot.register_next_step_handler(message, print_recipe(message, recipe_))
    bot.send_message(message.chat.id, 'Ужин')
    recipe_ = get_random_recipe(find_recipe_with_categories(all_recipe, ['Горячие блюда']))
    bot.register_next_step_handler(message, print_recipe(message, recipe_))


def print_recipe(message, recipe_):
    kb = get_back()
    text = ''
    if recipe_ != None:
        text = f"Название: {recipe_.name} \nВремя готовки: {recipe_.cook_time}\nПорций: {recipe_.count_portion}\n" \
              f"Калории: {recipe_.calories[0]}\nБелки: {recipe_.calories[1]}\nЖиры: {recipe_.calories[2]}\n" \
              f"Углеводы: {recipe_.calories[3]} \nИнгредиенты: "
        ing_str = ''
        for ing in recipe_.ingredients:
            ing_str += ing[0] + ', '
        ing_str = ing_str[:len(ing_str) - 2]
        text += ing_str + '\nКатегории: '
        cat_str = ''
        for cat in recipe_.categories:
            cat_str += cat + ', '
        cat_str = cat_str[:len(cat_str) - 2]
        text += cat_str + '\nРецепт: ' + recipe_.manual
        bot.send_photo(message.chat.id, recipe_.photo)
    else:
        text = 'Таких рецептов нет'
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text == 'Личный кабинет❤️')
def personal_account(m):
    kb = get_personal_account()
    bot.send_message(m.chat.id, 'Ваш личный кабинет:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Приготовленное🍳')
def cooked(m):
    bot.send_message(m.chat.id, 'Ваше приготовленное:')
    recipes = DBHelper("recipe.db").get('recipe_cooked', ['user_id'], [str(m.chat.id)])
    for rec in recipes:
        if rec[3] == '1':
            bot.send_message(m.chat.id, 'Вам понравилось')
        else:
            bot.send_message(m.chat.id, 'Вам не понравилось')
        recipe_ = get_recipe(all_recipe, rec[2])
        bot.register_next_step_handler(m, print_recipe(m, recipe_))
    # TODO вывод списка приготовленного со смайликами палец вверх, палец вниз


#  bot.register_next_step_handler(message, ask_feedback)


@bot.message_handler(func=lambda message: message.text == 'Продукты на кухне🥡')
def products_in_the_kitchen(m):
    kb = get_selection_of_products()
    bot.send_message(m.chat.id, 'Выберите продукты:', reply_markup=kb)
    # TODO дальше реализовать переход к продуктам


@bot.message_handler(func=lambda message: message.text == 'Фильтры для блюд🔍')
def filters_for_dishes(m):
    kb = get_filters_for_dishes()
    bot.send_message(m.chat.id, 'Настройте фильтры для подборки рецептов:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Кухня🥐')
def types_of_cuisine(m):
    kb = get_cuisines()
    bot.send_message(m.chat.id, 'Выберите кухню:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Продукты🥩')
def choose_products(m):
    kb = get_selection_of_products()
    bot.send_message(m.chat.id, 'Выберите продукты:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Категория🍕')
def category(m):
    kb = get_category()
    bot.send_message(m.chat.id, 'Выберите категорию:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in cuisines)
def category(message):
    kind = message.text
    print(clear_text(kind))
    DBHelper("recipe.db").insert('selected_categories', ['user_id', 'category'], [message.chat.id, clear_text(kind)])
    kb = get_filters_for_dishes()
    for cuisine in cuisines:
        if kind == cuisine:
            bot.send_message(message.chat.id, f"Выбрано: {kind}", reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in arr_category)
def category(message):
    kind = message.text
    print(clear_text(kind))
    DBHelper("recipe.db").insert('selected_categories', ['user_id', 'category'], [message.chat.id, clear_text(kind)])
    kb = get_filters_for_dishes()
    for arr in arr_category:
        if kind == arr:
            bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Меню🍽️')
def menu(m):
    kb = get_menu()
    bot.send_message(m.chat.id, 'Выберите меню:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in arr_menu)
def types_of_menu(message):
    kind = message.text
    print(clear_text(kind))
    DBHelper("recipe.db").insert('selected_categories', ['user_id', 'category'], [message.chat.id, clear_text(kind)])
    kb = get_filters_for_dishes()
    for arr in arr_menu:
        if kind == arr:
            bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Калорийность🍔')
def caloricity(m):
    kb = get_caloricity()
    bot.send_message(m.chat.id, 'Выберите калорийность:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in kalor)
def caloricity(message):
    kind = message.text
    kb = get_filters_for_dishes()
    for arr in kalor:
        if kind == arr:
            bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Сбросить🔄')
def reset(m):
    DBHelper("recipe.db").delete('selected_categories', 'user_id', m.chat.id)
    DBHelper("recipe.db").delete('selected_ingredients', 'user_id', m.chat.id)
    bot.send_message(m.chat.id, 'Ваши фильтры сброшены')


@bot.message_handler(func=lambda message: message.text == 'Список рецептов📃')
def list_of_recipes(m):
    kb = get_list_of_recipes()
    bot.send_message(m.chat.id, 'Ваш рецепт:', reply_markup=kb)


#  bot.register_next_step_handler(message, ask_feedback)
@bot.message_handler(func=lambda message: message.text == 'На основе продуктов на кухне🥡')
def based_on_products_in_the_kitchen(m):
    bot.send_message(m.chat.id, 'Вы выбрали на основе продуктов на кухне:')
    # TODO реализовать тот факт, что будет подбирать рецепт на основе продуктов на кухне и отметка галочка


@bot.message_handler(func=lambda message: message.text == 'На основе личного кабинета❤️')
def based_on_favorites(m):
    bot.send_message(m.chat.id, 'Вы выбрали на личного кабинета:')
    # TODO реализовать тот факт, что будет подбирать рецепт на основе продуктов на кухне и отметка галочка


@bot.message_handler(func=lambda message: message.text == 'Посмотреть рецепт📜')
def viewing_a_dish(m):
    kb = get_viewing_a_dish()
    ing = []
    ingredients = DBHelper("recipe.db").get('selected_ingredients', ['user_id'], [str(m.chat.id)])
    for inr in ingredients:
        ing.append(inr[2])
    recipes = find_recipe_with_ingredients(all_recipe, ing)
    cat = []
    categories = DBHelper("recipe.db").get('selected_categories', ['user_id'], [str(m.chat.id)])
    for ca in categories:
        cat.append(ca[2])
    recipes = find_recipe_with_ingredients(recipes, ing)
    recipe_ = get_random_recipe(recipes)
    take_token(m.chat.id, 1)
    DBHelper("recipe.db").update('user', 'username', m.chat.id, 'last_recipe_id', recipe_.id_)
    print('2')
    bot.register_next_step_handler(m, print_recipe(m, recipe_))
    bot.send_message(m.chat.id, 'Ваш рецепт. Нажмите ещё раз для получения нового рецепта:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Добавить в личный кабинет❤️')
def add_to_your_personal_account(m):
    kb = personal_and_favorites()
    print('1')
    user = DBHelper("recipe.db").get('user', ['username'], [str(m.chat.id)])
    DBHelper("recipe.db").insert('recipe_like', ['user_id', 'recipe_id'], [str(m.chat.id), user[0][6]])
    bot.send_message(m.chat.id, 'Выберите, куда хотите добавить рецепт:', reply_markup=kb)
    # TODO реализоваь добавление в список избранного и возврат на нужную страницу


def take_token(name, num):
    user = DBHelper("recipe.db").get('user', ['username'], [str(name)])
    tokens = int(user[0][3])
    tokens -= num
    DBHelper("recipe.db").update('user', 'username', name, 'tokens', tokens)


@bot.message_handler(func=lambda message: message.text == 'Добавить в приготовленное🍳')
def add_to_the_cooked(m):
    kb = get_add_to_the_cooked()
    bot.send_message(m.chat.id, 'Понравилось ли вам приготовленное блюдо?', reply_markup=kb)
    # TODO реализоваь добавление смайликов к рецепту и возврат на нужную страницу


@bot.message_handler(func=lambda message: message.text == 'Понравилось👍🏻')
def like(m):
    user = DBHelper("recipe.db").get('user', ['username'], [str(m.chat.id)])
    DBHelper("recipe.db").insert('recipe_cooked', ['user_id', 'recipe_id', 'rating'], [str(m.chat.id), user[0][6], '1'])
    bot.send_message(m.chat.id, 'Спасибо за ваш отзыв')
    return start(m)


# TODO реализовать добавление лайка к рецепту


@bot.message_handler(func=lambda message: message.text == 'Не понравилось👎🏻')
def dislike(m):
    user = DBHelper("recipe.db").get('user', ['username'], [str(m.chat.id)])
    DBHelper("recipe.db").insert('recipe_cooked', ['user_id', 'recipe_id', 'rating'], [str(m.chat.id), user[0][6], '0'])
    bot.send_message(m.chat.id, 'Спасибо за ваш отзыв')
    return start(m)


@bot.message_handler(func=lambda message: message.text == 'Удалить папку🗑️')
def delete_a_folder(m):
    # TODO реализовать показ папок и удаление по кнопке
    bot.send_message(m.chat.id, 'Выберите папку для удаления:')


@bot.message_handler(func=lambda message: message.text == 'Добавить в существующую папку🗂️')
def delete_a_folder(m):
    # TODO реализовать показ папок и добавление по кнопке
    bot.send_message(m.chat.id, 'Выберите папку для добавления:')


@bot.message_handler(func=lambda message: message.text == 'Личные рецепты📜')
def personal_recipes(m):
    # TODO реализовать вывод рецептов
    bot.send_message(m.chat.id, 'Ваши личные рецепты:')


@bot.message_handler(func=lambda message: message.text == 'Избранные рецепты❤️')
def dislike(m):
    # TODO реализовать вывод рецептов
    bot.send_message(m.chat.id, 'Ваши избранные рецепты:')
    recipes = DBHelper("recipe.db").get('recipe_like', ['user_id'], [str(m.chat.id)])
    for rec in recipes:
        recipe_ = get_recipe(all_recipe, rec[2])
        bot.register_next_step_handler(m, print_recipe(m, recipe_))



@bot.message_handler(func=lambda message: message.text == 'Добавить рецепт📝')
def add_a_recipe(m):
    # TODO реализовать добавление рецепта
    bot.send_message(m.chat.id, 'Введите название рецепта:')
    bot.register_next_step_handler(m, write_a_recipe)


def write_a_recipe(m):
    recipe_name = m.text
    kb = get_write_a_recipe()
    bot.send_message(m.chat.id, 'Введите рецепт:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Ввести рецепт📝')
def recipe(m):
    recipe = m.text
    bot.register_next_step_handler(m, write)


def write(m):
    bot.send_message(m.chat.id, 'Рецепт добавлен')
    kb = get_selection_of_products()
    # bot.register_next_step_handler(m, метод для создания рецепта)
    bot.send_message(m.chat.id, 'Выберите продукты:', reply_markup=kb)


def selection_of_products_for_the_recipe(m):
    # TODO передавать в метод для создания рецептов
    recipe_name = m.text
    kb = get_selection_of_products()
    bot.send_message(m.chat.id, 'Выберите продукты:', reply_markup=kb)
    # bot.register_next_step_handler(message, метод для создания рецепта)


def selection_of_products(m):
    # TODO передавать в метод для создания рецептов
    kb = get_selection_of_products()
    bot.send_message(m.chat.id, 'Выберите продукты:', reply_markup=kb)
    # bot.register_next_step_handler(message, метод для создания рецепта)


@bot.message_handler(func=lambda message: message.text in products)
def product(message):
    kind = message.text
    if kind == products[0]:
        kb = get_types_of_meat()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[1]:
        kb = get_types_of_vegetables()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[2]:
        kb = get_types_of_milk_and_eggs()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[3]:
        kb = get_mushrooms()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[4]:
        kb = get_nuts()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[5]:
        kb = get_cereals_legumes_and_flour()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[6]:
        kb = get_fruits_and_berries()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)
    elif kind == products[7]:
        kb = get_greenery()
        bot.send_message(message.chat.id, f"Выбрано: {kind} ", reply_markup=kb)


@bot.message_handler(func=lambda message: message.text in com)
def product(message):
    kind = message.text
    print(clear_text(kind))
    DBHelper("recipe.db").insert('selected_ingredients', ['user_id', 'ingredient'], [message.chat.id, clear_text(kind)])
    kb = get_selection_of_products()
    bot.send_message(message.chat.id, f"Выбрано: {kind}")
    bot.send_message(message.chat.id, 'Если нужно, выберите ещё продукт:', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Назад⏮️')
def back1(m):
    kb = get_start_for_user()
    bot.send_message(m.chat.id, 'Вы вернулись назад', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Назад⏪')
def back2(m):
    kb = get_start_for_user()
    bot.send_message(m.chat.id, 'Вы вернулись назад', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Назад◀️')
def back3(m):
    kb = get_selection_of_recipes()
    bot.send_message(m.chat.id, 'Вы вернулись назад', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Назад↩️')
def back4(m):
    kb = get_selection_of_recipes()
    bot.send_message(m.chat.id, 'Вы вернулись назад', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Назад⬅️')
def back5(m):
    kb = get_list_of_recipes()
    bot.send_message(m.chat.id, 'Вы вернулись назад', reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Показать папки🗂️')
def show_folders(m):
    # TODO реализовать показ папок
    bot.send_message(m.chat.id, 'Ваш список папок:')


#  bot.register_next_step_handler(m, show_all_folders)


@bot.message_handler(func=lambda message: message.text == 'Создать папку📁')
def create_a_folder(m):
    # TODO реализовать создание папок по названию
    bot.send_message(m.chat.id, 'Введите название для папки:')
    bot.register_next_step_handler(m, creating_folder)


def creating_folder(m):
    name_folder = m.text
    button = types.KeyboardButton(name_folder)
    bot.send_message(m.chat.id, f"Папка {name_folder} создана", reply_markup=button)


"""def show_all_folders(m):
    folders = get_all_folders()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for folder in folders:
        button = types.KeyboardButton(folder)
        keyboard.add(button)
    bot.send_message(m.chat.id, text="Список папок:", reply_markup=keyboard)


def get_all_folders():
    all_folders = []
    dialogs = bot.get_dialogs()
    for dialog in dialogs:
        folder_name = dialog.title
        all_folders.append(folder_name)
    return all_folders"""

while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)
