from DBHelper import DBHelper
import random


class Recipe:
    def __init__(self, id_, name, count_portion, cook_time, manual):
        self.id_ = id_
        self.name = name
        self.manual = manual
        self.cook_time = cook_time
        self.count_portion = count_portion
        self.photo = ''
        self.ingredients = []
        self.categories = []
        self.calories = []


def get_photo(id_, link):
    lin = link[int(id_) - 1]
    return lin[2]


def get_calories(id_, calories):
    for cal in calories:
        if id_ == str(cal[0]):
            return [cal[1], cal[2], cal[3], cal[4]]


def get_ingredients(id_, recipe_ingredients, ingredient):
    all_ingredients = []
    for rec_ing in recipe_ingredients:
        if id_ == rec_ing[1]:
            ing = ingredient[int(rec_ing[2]) - 1]
            all_ingredients.append([ing[1], rec_ing[3]])
    return all_ingredients


def get_categories(id_, recipe_categories, category):
    all_categories = []
    for rec_cat in recipe_categories:
        if id_ == rec_cat[1]:
            cat = category[int(rec_cat[2]) - 1]
            all_categories.append(cat[1])
    return all_categories




def print_recipe(recipe):
    print(recipe.name, recipe.count_portion, recipe.cook_time)
    print(recipe.photo)
    for cal in recipe.calories:
        print(cal)
    #print(recipe.manual)

    for cat in recipe.categories:
        print(cat)

    for ing in recipe.ingredients:
        print(ing[0], ing[1])


def get_random_recipe(list_recipe):
    return list_recipe[random.randint(0, len(list_recipe) - 1)]



def find_recipe_with_categories(all_recipe, cats):
    need_recipe = []
    length = len(cats)
    i = 0
    for recipe in all_recipe:
        i = 0
        for c in cats:
            for cat in recipe.categories:
                if c == cat:
                    i += 1
        if length == i:
            need_recipe.append(recipe)
    return need_recipe


def find_recipe_with_ingredients(all_recipe, ings):
    need_recipe = []
    length = len(ings)
    i = 0
    for recipe in all_recipe:
        i = 0
        for ing in ings:
            for ingri in recipe.ingredients:
                if ingri[0] == ing:
                    i += 1
        if length == i:
            need_recipe.append(recipe)
    return need_recipe


def get_recipe(recipes, ids):
    for recipe in recipes:
        if recipe.id_ == ids:
            return recipe


def get_recipe_by_manual(recipes, manual):
    for recipe in recipes:
        if recipe.manual == manual:
            return recipe


def get_all_recipe():
    helper = DBHelper("recipe.db")
    all_recipe = []
    recipe = helper.print_info('recipe')
    for rec in recipe:
        i = str(rec[0])
        #print(i)
        full_recipe = Recipe(i, rec[1], rec[2], rec[3], rec[4])
        full_recipe.photo = helper.get('link', ['id'], [i])[0][2]

        cal = helper.get('calories', ['recipe_id'], [i])
        if len(cal) == 0:
            full_recipe.calories = ['0', '0', '0', '0']
        else:
            full_recipe.calories = [cal[0][1], cal[0][2], cal[0][3], cal[0][4]]

        all_categories = []
        cat = helper.get('recipe_categories', ['recipe_id'], [i])
        for c in cat:
            name = helper.get('category', ['id'], [c[2]])
            all_categories.append(name[0][1])

        full_recipe.categories = all_categories

        all_ingredients = []
        ingredients = helper.get('recipe_ingredients', ['recipe_id'], [i])
        for ing in ingredients:
            name = helper.get('ingredient', ['id'], [ing[2]])
            all_ingredients.append([name[0][1], ing[3]])

        full_recipe.ingredients = all_ingredients
        all_recipe.append(full_recipe)
        #print_recipe(full_recipe)
    return all_recipe


def test(all_recipe):
    recipes = find_recipe_with_categories(all_recipe, ['Завтраки', 'Сырники'])
    for i in range(0, 5):
        print_recipe(recipes[i])
    recipes = find_recipe_with_ingredients(all_recipe, ['Сахар', 'Сливки'])
    for i in range(0, 5):
        print_recipe(recipes[i])


def clear_text(text):
    whitelist = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    answer = ''.join(filter(whitelist.__contains__, text))
    return answer

