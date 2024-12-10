import os
from pprint import pprint

class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def add_ingredient(self, ingredient_name, quantity, unit):
        self.ingredients.append((ingredient_name, quantity, unit))

    def print_recipe(self):
        print(f"{self.name}")
        for ingredient in self.ingredients:
            print(f"{ingredient[0]} | {ingredient[1]} | {ingredient[2]}")


def read_recipes_from_file(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        current_recipe = None
        for line in file:
            if not line.strip():
                continue

            # Если строка содержит название рецепта
            if len(line.split('|')) == 1:
                if current_recipe is not None:
                    recipes.append(current_recipe)

                current_recipe = Recipe(line.strip())
            else:
                parts = line.strip().split('|')
                ingredient_name = parts[0].strip()
                quantity = float(parts[1].strip())
                unit = parts[2].strip()
                current_recipe.add_ingredient(ingredient_name, quantity, unit)

        # Добавляем последний рецепт
        if current_recipe is not None:
            recipes.append(current_recipe)

    return recipes


def save_recipes_to_file(recipes, file_path):
    with open(file_path, 'w') as file:
        for recipe in recipes:
            file.write(recipe.name + '\n')
            for ingredient in recipe.ingredients:
                file.write(f"{ingredient[0]} | {ingredient[1]} | {ingredient[2]}\n")
            file.write('\n')


def create_new_recipe():
    name = input("Введите название рецепта: ")
    num_ingredients = int(input("Сколько ингредиентов в этом рецепте? "))

    new_recipe = Recipe(name)

    for _ in range(num_ingredients):
        ingredient_name = input("Введите название ингредиента: ")
        quantity = float(input("Введите количество: "))
        unit = input("Введите единицу измерения: ")
        new_recipe.add_ingredient(ingredient_name, quantity, unit)

    return new_recipe


def clear_all_recipes(recipes):
    confirmation = input("Вы уверены, что хотите удалить все рецепты? (да/нет): ")
    if confirmation.lower() == 'да':
        recipes.clear()
        print("Все рецепты были удалены.")
    else:
        print("Операция отменена.")


def main():
    file_path = 'recipes.txt'

    if os.path.exists(file_path):
        recipes = read_recipes_from_file(file_path)
    else:
        recipes = []

    while True:
        choice = input("\nВыберите действие:\n"
                      "1. Просмотреть все рецепты\n"
                      "2. Создать новый рецепт\n"
                      "3. Полностью очистить все рецепты\n"
                      "4. Сохранить изменения и выйти\n"
                      "Ваш выбор: ")

        if choice == '1':
            for recipe in recipes:
                recipe.print_recipe()
                print()  # Разделяем рецепты пустой строкой

        elif choice == '2':
            new_recipe = create_new_recipe()
            recipes.append(new_recipe)

        elif choice == '3':
            clear_all_recipes(recipes)

        elif choice == '4':
            save_recipes_to_file(recipes, file_path)
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()


def read_cookbook_from_file(file_path):
    cook_book = {}
    with open(file_path, 'r') as file:
        current_recipe = None
        for line in file:
            if not line.strip():
                continue

            # Если строка содержит название рецепта
            if len(line.split('|')) == 1:
                if current_recipe is not None:
                    cook_book[current_recipe['name']] = current_recipe['ingredients']

                current_recipe = {'name': line.strip(), 'ingredients': []}
            else:
                parts = line.strip().split('|')
                ingredient_name = parts[0].strip()
                quantity = float(parts[1].strip())
                measure = parts[2].strip()
                current_recipe['ingredients'].append({'ingredient_name': ingredient_name, 'quantity': quantity, 'measure': measure})

        # Добавляем последний рецепт
        if current_recipe is not None:
            cook_book[current_recipe['name']] = current_recipe['ingredients']

    return cook_book


def main():
    file_path = 'recipes.txt'

    if os.path.exists(file_path):
        cook_book = read_cookbook_from_file(file_path)
        #pprint(cook_book)
    else:
        print('Файл с рецептами не найден.')


if __name__ == "__main__":
    main()

import os
from pprint import pprint


def read_cookbook_from_file(file_path):
    cook_book = {}
    with open(file_path, 'r') as file:
        current_recipe = None
        for line in file:
            if not line.strip():
                continue

            # Если строка содержит название рецепта
            if len(line.split('|')) == 1:
                if current_recipe is not None:
                    cook_book[current_recipe['name']] = current_recipe['ingredients']

                current_recipe = {'name': line.strip(), 'ingredients': []}
            else:
                parts = line.strip().split('|')
                ingredient_name = parts[0].strip()
                quantity = float(parts[1].strip())
                measure = parts[2].strip()
                current_recipe['ingredients'].append({'ingredient_name': ingredient_name, 'quantity': quantity, 'measure': measure})

        # Добавляем последний рецепт
        if current_recipe is not None:
            cook_book[current_recipe['name']] = current_recipe['ingredients']

    return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    for dish in dishes:
        if dish in cook_book:  # Проверяем, существует ли блюдо в рецептах
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                quantity = ingredient['quantity'] * person_count
                measure = ingredient['measure']

                if name in shop_list:
                    shop_list[name]['quantity'] += quantity
                else:
                    shop_list[name] = {'quantity': quantity, 'measure': measure}

    return shop_list


def main():
    file_path = 'recipes.txt'

    if os.path.exists(file_path):
        global cook_book
        cook_book = read_cookbook_from_file(file_path)
        pprint(cook_book)

        # Запрашиваем количество персон
        person_count = int(input("Введите количество персон: "))

        # Выводим доступные блюда
        print("Доступные блюда:")
        for index, dish in enumerate(cook_book.keys(), start=1):
            print(f"{index}. {dish}")

        # Запрашиваем выбор блюд
        selected_dishes = input("Введите номера блюд, разделенные запятыми: ")
        selected_dishes_indices = [int(i.strip()) for i in selected_dishes.split(',')]
        selected_dishes_names = [list(cook_book.keys())[i - 1] for i in selected_dishes_indices]

        # Получаем список покупок
        shop_list = get_shop_list_by_dishes(selected_dishes_names, person_count)
        pprint(shop_list)
    else:
        print('Файл с рецептами не найден.')


if __name__ == "__main__":
    main()