from telebot import types

ingredients_selected = False
favorites_selected = False


def print_categories(categories):
    str = ''
    for cat in categories:
        str += cat
    return str


def print_ingredients(ingredients):
    str = ''
    for ing in ingredients:
        str += ing
    return str

'''def get_selection_of_recipes():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Фильтры для блюд🔍')
    bt2 = types.KeyboardButton(text='Список рецептов📃')
    bt3 = types.KeyboardButton(text='✅На основе продуктов на кухне🥡')
    bt4 = types.KeyboardButton(text='✅На основе избранных❤️')
    bt5 = types.KeyboardButton(text='Назад⏮️')
    kb.row(bt1, bt2)
    kb.row(bt3 if is_products_selected() else 'На основе продуктов на кухне🥡',
           bt4 if is_favorites_selected() else 'На основе избранных❤️')
    kb.row(bt5)
    return kb '''


def is_products_selected():
    return True


def is_favorites_selected():
    return True

def get_back():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt1 = types.KeyboardButton(text='Назад⏮️')
    kb.row(bt1)
    return kb

def get_start():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Пользователь👤')
    bt2 = types.KeyboardButton(text='Менеджер💼')
    bt3 = types.KeyboardButton(text='Администратор🔒')
    kb.row(bt1)
    kb.row(bt2)
    kb.row(bt3)
    return kb


def get_start2():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt2 = types.KeyboardButton(text='Менеджер💼')
    bt3 = types.KeyboardButton(text='Администратор🔒')
    kb.row(bt2)
    kb.row(bt3)
    return kb


def get_start_for_user():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Подборка рецептов📃')
    bt2 = types.KeyboardButton(text='Рецепты на день📚️')
    bt3 = types.KeyboardButton(text='Личный кабинет❤️')
    bt4 = types.KeyboardButton(text='Приготовленное🍳')
    bt5 = types.KeyboardButton(text='Продукты на кухне🥡')
    kb.add(bt1, bt2, bt3, bt4, bt5)
    return kb


def get_start_for_manager():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Действие над пользователем👤')
    bt2 = types.KeyboardButton(text='Посмотреть активность📊')
    bt3 = types.KeyboardButton(text='Посмотреть число новых пользователей👥')
    bt4 = types.KeyboardButton(text='Действия пользователя🙋‍♂️')
    kb.row(bt1, bt4)
    kb.row(bt2, bt3)
    return kb


def get_info_get_balance():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt1 = types.KeyboardButton(text='Посмотреть информация📋')
    bt2 = types.KeyboardButton(text='Изменить баланс тоненов💰')
    bt3 = types.KeyboardButton(text='Вернутся в главное меню🏠')
    kb.row(bt1, bt2)
    kb.row(bt3)
    return kb


def get_time_interval():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='1️⃣ день')
    bt2 = types.KeyboardButton(text='1️⃣ неделя')
    bt3 = types.KeyboardButton(text='1️⃣ месяц')
    bt4 = types.KeyboardButton(text='1️⃣ год')
    bt5 = types.KeyboardButton(text='Вернутся в главное меню🏠')
    kb.row(bt1, bt2)
    kb.row(bt3, bt4)
    kb.row(bt5)
    return kb


def get_start_for_admin():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Действие над пользователем👤')
    bt2 = types.KeyboardButton(text='Посмотреть активность📊')
    bt3 = types.KeyboardButton(text='Посмотреть число новых пользователей👥')
    bt4 = types.KeyboardButton(text='Действия пользователя🙋‍♂️')
    bt5 = types.KeyboardButton(text='Обновить данные о рецептах🔄')
    kb.row(bt1, bt4)
    kb.row(bt2, bt3)
    kb.row(bt5)
    return kb


def get_selection_of_recipes():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Фильтры для блюд🔍')
    bt2 = types.KeyboardButton(text='Список рецептов📃')
    bt3 = types.KeyboardButton(text='На основе продуктов на кухне🥡')
    bt4 = types.KeyboardButton(text='На основе избранных❤️')
    bt5 = types.KeyboardButton(text='Назад⏮️')
    kb.row(bt1, bt2)
    kb.row(bt3, bt4)
    kb.row(bt5)
    return kb



"""def get_selection_of_recipes():
    global ingredients_selected, favorites_selected
    keyboard = [
        [
            KeyboardButton(text='Фильтры для блюд🔍'),
            KeyboardButton(text='Список рецептов📃')
        ],
        [
            KeyboardButton(
                text='На основе продуктов на кухне🥡' if not ingredients_selected else '✅ На основе продуктов на кухне🥡'),
            KeyboardButton(text='На основе избранных❤️' if not favorites_selected else '✅На основе избранных❤️')
        ],
        [
            KeyboardButton(text='Назад⏮️')
        ]
    ]
    return keyboard"""


def button_callback(update, context):
    global ingredients_selected, favorites_selected

    query = update.callback_query
    data = query.data

    if data == 'ingredients':
        # Изменяем состояние кнопки "На основе продуктов на кухне"
        ingredients_selected = not ingredients_selected
    elif data == 'favorites':
        # Изменяем состояние кнопки "На основе избранных"
        favorites_selected = not favorites_selected

    # Обновляем клавиатуру
    keyboard = get_selection_of_recipes()
    query.edit_message_text('Выберите действие:', reply_markup=keyboard)


def get_personal_account():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Показать папки🗂️')
    bt2 = types.KeyboardButton(text='Создать папку📁')
    bt3 = types.KeyboardButton(text='Удалить папку🗑️')
    bt4 = types.KeyboardButton(text='Добавить рецепт📝')
    bt5 = types.KeyboardButton(text='Личные рецепты📜')
    bt6 = types.KeyboardButton(text='Избранные рецепты❤️')
    bt7 = types.KeyboardButton(text='Назад⏪')
    kb.row(bt1, bt2, bt3)
    kb.row(bt4, bt5, bt6)
    kb.row(bt7)
    return kb


def get_filters_for_dishes():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Продукты🥩')
    bt2 = types.KeyboardButton(text='Категория🍕')
    bt3 = types.KeyboardButton(text='Меню🍽️')
    bt4 = types.KeyboardButton(text='Калорийность🍔')
    bt5 = types.KeyboardButton(text='Кухня🥐')
    bt6 = types.KeyboardButton(text='Сбросить🔄')
    bt7 = types.KeyboardButton(text='Назад◀️')
    kb.row(bt1, bt2)
    kb.row(bt3, bt4)
    kb.row(bt5, bt6)
    kb.row(bt7)
    return kb


def get_list_of_recipes():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Посмотреть рецепт📜')
    bt2 = types.KeyboardButton(text='Назад↩️')
    kb.row(bt1)
    kb.row(bt2)
    return kb


def get_viewing_a_dish():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Добавить в личный кабинет❤️')
    bt2 = types.KeyboardButton(text='Добавить в приготовленное🍳')
    bt3 = types.KeyboardButton(text='Назад⬅️')
    kb.row(bt1, bt2)
    kb.row(bt3)
    return kb


def personal_and_favorites():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Добавить в избранное❤️')
    bt2 = types.KeyboardButton(text='Добавить в существующую папку🗂️')
    bt3 = types.KeyboardButton(text='Создать папку📁')
    kb.row(bt1)
    kb.row(bt2)
    kb.row(bt3)
    return kb


def get_add_to_the_cooked():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Понравилось👍🏻')
    bt2 = types.KeyboardButton(text='Не понравилось👎🏻')
    kb.row(bt1, bt2)
    return kb


def get_caloricity():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Низкая🍅')
    bt2 = types.KeyboardButton(text='Средняя🍇')
    bt3 = types.KeyboardButton(text='Высокая🌭')
    kb.row(bt1)
    kb.row(bt2)
    kb.row(bt3)
    return kb


def get_category():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Завтраки🥐')
    bt2 = types.KeyboardButton(text='Бульоны🥘')
    bt3 = types.KeyboardButton(text='Закуски🍟')
    bt4 = types.KeyboardButton(text='Напитки🥤')
    bt5 = types.KeyboardButton(text='Ризотто🍛')
    bt6 = types.KeyboardButton(text='Основые блюда🍗')
    bt7 = types.KeyboardButton(text='Паста и пицца🍝')
    bt8 = types.KeyboardButton(text='Салаты🥗')
    bt9 = types.KeyboardButton(text='Соусы и маринады🍯')
    bt10 = types.KeyboardButton(text='Супы🍲')
    bt11 = types.KeyboardButton(text='Сэндвичи🥪')
    bt12 = types.KeyboardButton(text='Выпечка и десерты🍩')
    bt13 = types.KeyboardButton(text='Заготовки🥒')
    kb.row(bt1, bt2)
    kb.row(bt3, bt4)
    kb.row(bt5, bt8)
    kb.row(bt10, bt11)
    kb.row(bt9)
    kb.row(bt6)
    kb.row(bt7)
    kb.row(bt12)
    kb.row(bt13)
    return kb


def get_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Безглютеновая диета🍓')
    bt2 = types.KeyboardButton(text='Вегетарианская еда🥗')
    bt3 = types.KeyboardButton(text='Веганская еда🍚')
    bt4 = types.KeyboardButton(text='Безлактозная диета🐟')
    bt5 = types.KeyboardButton(text='Детское меню🍟')
    bt6 = types.KeyboardButton(text='Постная еда🍪')
    bt7 = types.KeyboardButton(text='Меню при диабете🥑')
    kb.row(bt1)
    kb.row(bt2)
    kb.row(bt3)
    kb.row(bt4)
    kb.row(bt5)
    kb.row(bt6)
    kb.row(bt7)
    return kb


cuisines = [
    "Абхазская🍓",
    "Австралийская🧁",
    "Австрийская🥑",
    "Авторская🥝",
    "Азербайджанская🐟",
    "Американская🥤",
    "Арабская🥘",
    "Аргентинская🍉",
    "Армянская🍚",
    "Афганская🍜",
    "Африканская🥕",
    "Белорусская🥭",
    "Бельгийская🍫",
    "Болгарская🍟",
    "Бразильская🍍",
    "Британская🍶",
    "Венгерская🥗",
    "Восточно-индийская🍎",
    "Вьетнамская🥞",
    "Голландская🥚",
    "Греческая🥥",
    "Грузинская🥓",
    "Дагестанская🥩",
    "Датская🍬",
    "Еврейская🍔",
    "Европейская☕",
    "Индийская🍆",
    "Индонезийская🍱",
    "Ирландская🍵",
    "Исландская🍕",
    "Испанская🍠",
    "Итальянская🍝",
    "Кавказская🍖",
    "Казахская🍌",
    "Канадская🥪",
    "Киргизская🌶️",
    "Китайская🥤",
    "Корейская🍙",
    "Креольская🍦",
    "Кубинская🌮",
    "Латвийская🍹",
    "Латиноамериканская🌭",
    "Ливанская🧀",
    "Литовская🌯",
    "Малайзийская🍓",
    "Марокканская🍜",
    "Мексиканская🍗",
    "Мировая🍄",
    "Молдавская🍖",
    "Немецкая🥭",
    "Норвежская🍲",
    "Одесская🥬",
    "Осетинская🍚",
    "Паназиатская🍿",
    "Персидская🥦",
    "Перуанская🥛",
    "Польская🍰",
    "Португальская🥔",
    "Русская🍇",
    "Сербская🥜",
    "Сингапурская🧅",
    "Сицилийская🍶",
    "Скандинавская🍩",
    "Советская🍅",
    "Средиземноморская🥙",
    "Тайская🍊",
    "Татарская🥧",
    "Турецкая🥩",
    "Туркменская🍖",
    "Узбекская🍠",
    "Украинская🥒",
    "Филиппинская🌽",
    "Финская🥞",
    "Французская🥐",
    "Чеченская🍒",
    "Чешская🍑",
    "Шведская🍟",
    "Швейцарская🥨",
    "Шотландская🍤",
    "Эстонская🥕",
    "Югославская🧀",
    "Японская🍣"
]
arr_category = ['Завтраки🥐', 'Бульоны🥘', 'Закуски🍟',
                'Напитки🥤', 'Основные блюда🍗', 'Паста и пицца🍝',
                'Ризотто🍛', 'Салаты🥗', 'Соусы и маринады🍯', 'Супы🍲',
                'Сэндвичи🥪', 'Выпечка и десерты🍩', 'Заготовки🥒']

arr_menu = [
    "Безглютеновая диета🍓",
    "Вегетарианская еда🥗",
    "Веганская еда🍚",
    "Безлактозная диета🐟",
    "Детское меню🍟",
    "Постная еда🍪",
    "Меню при диабете🥑"
]

kalor = ['Низкая🍅', 'Средняя🍇', 'Высокая🌭']

products = ['Мясо🥩', 'Овощи🥕', 'Молочные продукты и яйца🥛',
            'Грибы🍄', 'Орехи🥜', 'Крупы, бобовые и мука🍚',
            'Фрукты и ягоды🍒', 'Зелень и травы🥬']

types_of_meat = [
    ['Бекон🥓', 'Ветчина🥓'],
    ['Говядина🥩', 'Индейка🦃'],
    ['Колбаса🌭', 'Кролик🐇'],
    ['Курица🍗', 'Печень🍖'],
    ['Сало🥓', 'Сардельки🌭'],
    ['Свинина🐷', 'Сердца❤️'],
    ['Стейк🥩', 'Телятина🐄'],
    ['Утка🦆', 'Фарш🍔']
]
types_of_vegetables = [
    ['Артишоки🌿', 'Баклажаны🍆'],
    ['Брокколи🥦', 'Горошек🌱'],
    ['Гурьба🌿', 'Кабачки 🍆'],
    ['Капуста🥬', 'Картофель🥔'],
    ['Лук🧅', 'Маслины🫒'],
    ['Морковь🥕', 'Огурцы🥒'],
    ['Перец ️', 'Подсолнечник🌻'],
    ['Помидоры🍅', 'Редис🥕'],
    ['Тыква🎃']
]

types_of_milk_and_eggs = [
    ["Йогурт🍨", "Кефир🥛"],
    ["Mаргарин🧈", "Mолоко🥛"],
    ["Mороженое🍦", "Простокваша🍶"],
    ["Ряженка🥛", "Сливки🥛"],
    ["Сливочное масло🧈", "Сыр🧀"],
    ["Сметана🧈", "Творог🧈"],
    ["Творожок🧈", "Яйцо🥚"]
]

mushrooms = [
    ["Белые грибы🍄", "Вешенки🍄"],
    ["Лисички🍄", "Опята🍄"],
    ["Подберезовики🍄", "Рыжики🍄"],
    ["Шампиньоны🍄"]
]

nuts = [
    ["Арахис🥜", "Грецкие орехи🌰"],
    ["Кедровые орехи🌰", "Кешью🌲"],
    ["Кокос🥥", "Макадамия🌴"],
    ["Миндаль🌰", "Мускатный орех🌰"],
    ["Орехи🌰", "Фисташки🌰"],
    ["Фундук🌰"]
]

cereals_legumes_and_flour = [
    ["Бобы🌾", "Булгур🌾"],
    ["Геркулес🌾", "Гранола🌾"],
    ["Гречневая крупа🌾", "Какао☕"],
    ["Кофе☕", "Кускус🌾"],
    ["Манная крупа🌾", "Мука🌾"],
    ["Нут🌾", "Рис🍚"],
    ["Фасоль🌾", "Ячмень🌾"]
]

fruits_and_berries = [
    ["Абрикосы🍑", "Авокадо🥑"],
    ["Айва🍐", "Ананас🍍"],
    ["Апельсины🍊", "Арбуз🍉"],
    ["Бананы🍌", "Брусника🫐"],
    ["Виноград🍇", "Вишня🍒"],
    ["Голубика🫐", "Гранаты🍎"],
    ["Грейпфруты🍊", "Груши🍐"],
    ["Дыня🍈", "Ежевика🫐"],
    ["Земляника🍓", "Клубника🍓"],
    ["Клюква🍒", "Крыжовник🍇"],
    ["Лайм🍋", "Лимон🍋"],
    ["Малина🍓", "Мандарины🍊"],
    ["Манго🥭", "Маракуйя🥭"],
    ["Облепиха🍊", "Папайя🥭"],
    ["Персики🍑", "Помело🍈"],
    ["Сливы🍑", "Смородина🍇"],
    ["Черешня🍒", "Черника🫐"],
    ["Хурма🍐", "Яблоко🍎"]
]

greenery = [
    ['Базилик🍃', 'Зеленый лук🌿'],
    ['Зеленый салат🥬', 'Лавровый лист🍃'],
    ['Укроп🌿', 'Эстрагон🌿'],
    ['Мята🍃', 'Тимьян🌿'],
    ['Петрушка🌿', 'Розмарин🌿'],
    ['Рукола🥬', 'Шалфей🌿']
]


def combine_arrays(*arrays):
    combined_array = []
    for array in arrays:
        combined_array.extend(array)
    return combined_array


combined = combine_arrays(types_of_meat, types_of_vegetables, types_of_milk_and_eggs, mushrooms, nuts,
                          cereals_legumes_and_flour, fruits_and_berries, greenery)


def combine_arrays2(arrays):
    combined_array = []
    for array in arrays:
        combined_array.extend(array)
    return combined_array


com = combine_arrays2(combined)


def get_greenery():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in greenery:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_nuts():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in nuts:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_cereals_legumes_and_flour():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in cereals_legumes_and_flour:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_fruits_and_berries():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in fruits_and_berries:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_mushrooms():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in mushrooms:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_types_of_milk_and_eggs():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_milk_and_eggs:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_types_of_vegetables():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_vegetables:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])

    return keyboard


def get_types_of_meat():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_meat:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])

    return keyboard


def get_cuisines():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in cuisines:
        kb.add(types.KeyboardButton(item))
    return kb


def get_selection_of_products():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Мясо🥩')
    bt2 = types.KeyboardButton(text='Овощи🥕')
    bt3 = types.KeyboardButton(text='Молочные продукты и яйца🥛')
    bt4 = types.KeyboardButton(text='Грибы🍄')
    bt5 = types.KeyboardButton(text='Орехи🥜')
    bt6 = types.KeyboardButton(text='Крупы, бобовые и мука🍚')
    bt7 = types.KeyboardButton(text='Фрукты и ягоды🍒')
    bt8 = types.KeyboardButton(text='Зелень и травы🥬')
    bt9 = types.KeyboardButton(text='Назад◀️')
    kb.row(bt1, bt2)
    kb.row(bt4, bt5)
    kb.row(bt3)
    kb.row(bt6)
    kb.row(bt7)
    kb.row(bt8)
    kb.row(bt9)

    return kb


def get_quantity():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='100 грамм')
    bt2 = types.KeyboardButton(text='200 грамм')
    bt3 = types.KeyboardButton(text='300 грамм')
    bt4 = types.KeyboardButton(text='400 грамм')
    bt5 = types.KeyboardButton(text='500 грамм')
    bt6 = types.KeyboardButton(text='600 грамм')
    bt7 = types.KeyboardButton(text='700 грамм')
    bt8 = types.KeyboardButton(text='800 грамм')
    bt9 = types.KeyboardButton(text='900 грамм')
    bt9 = types.KeyboardButton(text='1 кг')
    kb.row(bt1, bt2)
    kb.row(bt4, bt5)
    kb.row(bt3)
    kb.row(bt6)
    kb.row(bt7)
    kb.row(bt8)
    kb.row(bt9)

    return kb


def get_write_a_recipe():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text='Ввести рецепт📝')
    kb.row(bt1)
    return kb

types_of_meat = [
    ['Бекон🥓', 'Ветчина🥓'],
    ['Говядина🥩', 'Индейка🦃'],
    ['Колбаса🌭', 'Кролик🐇'],
    ['Курица🍗', 'Печень🍖'],
    ['Сало🥓', 'Сардельки🌭'],
    ['Свинина🐷', 'Сердца❤️'],
    ['Стейк🥩', 'Телятина🐄'],
    ['Утка🦆', 'Фарш🍔']
]
types_of_vegetables = [
    ['Артишоки🌿', 'Баклажаны🍆'],
    ['Брокколи🥦', 'Горошек🌱'],
    ['Гурьба🌿', 'Кабачки 🍆'],
    ['Капуста🥬', 'Картофель🥔'],
    ['Лук🧅', 'Маслины🫒'],
    ['Морковь🥕', 'Огурцы🥒'],
    ['Перец ️', 'Подсолнечник🌻'],
    ['Помидоры🍅', 'Редис🥕'],
    ['Тыква🎃']
]

types_of_milk_and_eggs = [
    ["Йогурт🍨", "Кефир🥛"],
    ["Mаргарин🧈", "Mолоко🥛"],
    ["Mороженое🍦", "Простокваша🍶"],
    ["Ряженка🥛", "Сливки🥛"],
    ["Сливочное масло🧈", "Сыр🧀"],
    ["Сметана🧈", "Творог🧈"],
    ["Творожок🧈", "Яйцо🥚"]
]

mushrooms = [
    ["Белые грибы🍄", "Вешенки🍄"],
    ["Лисички🍄", "Опята🍄"],
    ["Подберезовики🍄", "Рыжики🍄"],
    ["Шампиньоны🍄"]
]

nuts = [
    ["Арахис🥜", "Грецкие орехи🌰"],
    ["Кедровые орехи🌰", "Кешью🌲"],
    ["Кокос🥥", "Макадамия🌴"],
    ["Миндаль🌰", "Мускатный орех🌰"],
    ["Орехи🌰", "Фисташки🌰"],
    ["Фундук🌰"]
]

cereals_legumes_and_flour = [
    ["Бобы🌾", "Булгур🌾"],
    ["Геркулес🌾", "Гранола🌾"],
    ["Гречневая крупа🌾", "Какао☕"],
    ["Кофе☕", "Кускус🌾"],
    ["Манная крупа🌾", "Мука🌾"],
    ["Нут🌾", "Рис🍚"],
    ["Фасоль🌾", "Ячмень🌾"]
]

fruits_and_berries = [
    ["Абрикосы🍑", "Авокадо🥑"],
    ["Айва🍐", "Ананас🍍"],
    ["Апельсины🍊", "Арбуз🍉"],
    ["Бананы🍌", "Брусника🫐"],
    ["Виноград🍇", "Вишня🍒"],
    ["Голубика🫐", "Гранаты🍎"],
    ["Грейпфруты🍊", "Груши🍐"],
    ["Дыня🍈", "Ежевика🫐"],
    ["Земляника🍓", "Клубника🍓"],
    ["Клюква🍒", "Крыжовник🍇"],
    ["Лайм🍋", "Лимон🍋"],
    ["Малина🍓", "Мандарины🍊"],
    ["Манго🥭", "Маракуйя🥭"],
    ["Облепиха🍊", "Папайя🥭"],
    ["Персики🍑", "Помело🍈"],
    ["Сливы🍑", "Смородина🍇"],
    ["Черешня🍒", "Черника🫐"],
    ["Хурма🍐", "Яблоко🍎"]
]

greenery = [
    ['Базилик🍃', 'Зеленый лук🌿'],
    ['Зеленый салат🥬', 'Лавровый лист🍃'],
    ['Укроп🌿', 'Эстрагон🌿'],
    ['Мята🍃', 'Тимьян🌿'],
    ['Петрушка🌿', 'Розмарин🌿'],
    ['Рукола🥬', 'Шалфей🌿']
]


def combine_arrays(*arrays):
    combined_array = []
    for array in arrays:
        combined_array.extend(array)
    return combined_array


combined = combine_arrays(types_of_meat, types_of_vegetables, types_of_milk_and_eggs, mushrooms, nuts,
                          cereals_legumes_and_flour, fruits_and_berries, greenery)


def combine_arrays2(arrays):
    combined_array = []
    for array in arrays:
        combined_array.extend(array)
    return combined_array


com = combine_arrays2(combined)


def get_greenery():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in greenery:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_nuts():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in nuts:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_cereals_legumes_and_flour():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in cereals_legumes_and_flour:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_fruits_and_berries():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in fruits_and_berries:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_mushrooms():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in mushrooms:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_types_of_milk_and_eggs():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_milk_and_eggs:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])
    return keyboard


def get_types_of_vegetables():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_vegetables:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])

    return keyboard


def get_types_of_meat():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for row in types_of_meat:
        button_row = []
        for word in row:
            button = types.KeyboardButton(word)
            button_row.append(button)
        buttons.append(button_row)
    keyboard.add(*[button for button_row in buttons for button in button_row])

    return keyboard
