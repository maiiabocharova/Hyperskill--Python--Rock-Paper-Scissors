import sqlite3
import argparse
INSERT_MEAL = "INSERT INTO meals (meal_name) VALUES (?);"
INSERT_INGREDIENT = "INSERT INTO ingredients (ingredient_name) VALUES (?);"
INSERT_MEASURE = "INSERT INTO measures (measure_name) VALUES (?);"
INSERT_RECIPE = "INSERT INTO recipes (recipe_name, recipe_description) VALUES (?, ?);"
INSERT_QUANTITY ='''INSERT INTO quantity
                    (quantity, recipe_id, measure_id, ingredient_id)
                    VALUES (?, ?, ?, ?)'''
SELECT_MEAL = 'SELECT meal_id FROM meals WHERE meal_name=?'
SELECT_MEASURE = 'SELECT measure_id FROM measures WHERE measure_name LIKE ?'
SELECT_INGREDIENT = 'SELECT ingredient_id FROM ingredients WHERE ingredient_name LIKE ?'
SELECT_RECIPE = 'SELECT recipe_id FROM quantity WHERE ingredient_id=?'
data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
conn = sqlite3.connect('food_blog.db')
cur = conn.cursor()
try:
    parser = argparse.ArgumentParser()
    parser.add_argument('db')
    parser.add_argument("--ingredients", type=str, required = False, help="Ingredients")
    parser.add_argument("--meals", type=str, required = False, help="Meals")
    args = parser.parse_args()
    available_ingredients_names = args.ingredients.split(',')
    meals = args.meals.split(',')
    available_ingredient_ids, meals_ids, recipes_ids, available_recipes = [], [], [], []
    try:
        for ingredient in available_ingredients_names:
            ingredient_id = cur.execute(SELECT_INGREDIENT, (ingredient,)).fetchone()[0]
            available_ingredient_ids.append(ingredient_id)
            recipes = cur.execute(SELECT_RECIPE, (ingredient_id,)).fetchall()
            for recipe_id in recipes:
                recipes_ids.append(recipe_id[0])
        available_ingredient_ids = set(available_ingredient_ids)
        print(f'available_ingredient_ids: {available_ingredient_ids}')
        for meal in meals:
            meal_id = cur.execute(SELECT_MEAL, (meal,)).fetchone()[0]
            meals_ids.append(meal_id)
            print(f'meals_ids: {meals_ids}')
        for recipe_id in set(recipes_ids):
            print(f'check recipe: {recipe_id}')
            ingred_per_recipe = []
            needed_ingredients = cur.execute('SELECT ingredient_id FROM quantity WHERE recipe_id=?', (recipe_id,)).fetchall()
            print(f'needed_ingredients: {needed_ingredients}')
            for ing in needed_ingredients:
                ingred_per_recipe.append(ing[0])
            ingred_per_recipe = set(ingred_per_recipe)
            if available_ingredient_ids.issubset(ingred_per_recipe):
                recipe = cur.execute('SELECT recipe_name FROM recipes WHERE recipe_id=?', (recipe_id,)).fetchone()[0]
                available_recipes.append(recipe)
        if len(available_recipes) != 0:
            print("and ".join(available_recipes))
        else:
            print('no such recipes')
    except:
        print('no such recipes')
except:
    cur.executescript('''
    DROP TABLE IF EXISTS measures;
    DROP TABLE IF EXISTS ingredients;
    DROP TABLE IF EXISTS meals;
    DROP TABLE IF EXISTS recipes;

    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS measures (
        measure_id INTEGER PRIMARY KEY,
        measure_name TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS ingredients (
        ingredient_id INTEGER PRIMARY KEY,
        ingredient_name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS meals (
        meal_id INTEGER PRIMARY KEY,
        meal_name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INTEGER PRIMARY KEY,
        recipe_name TEXT NOT NULL,
        recipe_description TEXT
    );
    CREATE TABLE IF NOT EXISTS serve (
        serve_id INTEGER PRIMARY KEY,
        meal_id INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        FOREIGN KEY(meal_id) REFERENCES meals (meal_id),
        FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id)
    );
    CREATE TABLE IF NOT EXISTS quantity (
        quantity_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL,
        recipe_id INTEGER NOT NULL,
        measure_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        FOREIGN KEY(recipe_id) REFERENCES recipes (recipe_id),
        FOREIGN KEY(measure_id) REFERENCES measures (measure_id),
        FOREIGN KEY(ingredient_id) REFERENCES ingredients (ingredient_id)
    );
''')
    def fill_tables(conn):
        with conn:
            for meal in data['meals']:
                conn.execute(INSERT_MEAL, (meal,))
            for ingredient in data['ingredients']:
                conn.execute(INSERT_INGREDIENT, (ingredient,))
            for measure in data['measures']:
                conn.execute(INSERT_MEASURE, (measure,))
    fill_tables(conn)
    print('Pass the empty recipe name to exit.')
    recipe_name = input('Recipe name:')
    while recipe_name != '':
        description = input('Recipe description:')
        result = cur.execute(INSERT_RECIPE, (recipe_name, description))
        recipe_id = result.lastrowid
        print('1) breakfast  2) brunch  3) lunch  4) supper')
        meal_ids = [int(i) for i in input('When the dish can be served:').split()]
        for meal_id in meal_ids:
            cur.execute('INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?)', (meal_id,recipe_id))
        quantity_and_ingredient = input('Input quantity of ingredient <press enter to stop>:')
        while quantity_and_ingredient != '':
            lst = quantity_and_ingredient.split()
            if len(lst) == 3:
                try:
                    quantity = int(lst[0])
                    measure_name = lst[1]
                    ingredient_name = lst[2]
                    measure_ids = cur.execute(SELECT_MEASURE, (f'{measure_name}%',)).fetchall()
                    ingredient_ids = cur.execute(SELECT_INGREDIENT, (f'{ingredient_name}%',)).fetchall()
                    if len(measure_ids) > 1:
                        print('The measure is not conclusive!')
                    elif len(ingredient_ids) > 1:
                        print('The ingredient is not conclusive!')
                    else:
                        measure_id = measure_ids[0][0]
                        ingredient_id = ingredient_ids[0][0]
                        print(f'ingredient_id: {ingredient_id}')
                        cur.execute(INSERT_QUANTITY, (quantity, recipe_id, measure_id, ingredient_id))
                        print('done!')
                except:
                    pass
            elif len(lst) == 2:
                try:
                    quantity = int(lst[0])
                    measure_name = ''
                    ingredient_name = lst[1]
                    measure_id = cur.execute(SELECT_MEASURE, (measure_name,)).fetchone()[0]
                    ingredient_ids = cur.execute(SELECT_INGREDIENT, (f'%{ingredient_name}%',)).fetchall()
                    if len(ingredient_ids) > 1:
                        print('The measure is not conclusive!')
                    else:
                        ingredient_id = ingredient_ids[0][0]
                        print(f'measure_id {measure_id}')
                        cur.execute(INSERT_QUANTITY, (quantity, recipe_id, measure_id, ingredient_id))
                        print('done!')
                except:
                    pass
            quantity_and_ingredient = input('Input quantity of ingredient <press enter to stop>:')
        recipe_name = input('Recipe name:')
    conn.commit()
conn.commit()
conn.close()

# sql = "INSERT INTO meals (meal_name) VALUES (?)"
# val = list(data["meals"])
# val2 = [[x] for x in val]
# cur.executemany(sql, val2)
#python food_blog.py --ingredients="sugar,milk" --meals="breakfast,brunch"
