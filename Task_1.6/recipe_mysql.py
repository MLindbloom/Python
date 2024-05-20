import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_database')
cursor.execute('USE task_database')

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ''
    while choice != 'quit':
        print('RECIPE APP')
        print(40 * '=')
        print('MAIN MENU')
        print('What would you like to do? Pick a Choice!:')
        print('1. Create a new recipe')
        print('2. Search for Recipe by Ingredient')
        print('3. Update an Existing Recipe')
        print('4. Delete a Recipe')
        print("Type 'quit' to exit the program.")
        choice = input('\nYour choice: ')

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == 'quit':
            print('Quitting')
            print('\nThanks for Using Recipe App!')
        else:
            print("Please choose a number or type 'quit'")

def create_recipe(conn, cursor):
    name = input('Enter Name of the Recipe: ')
    cooking_time = int(input('Enter the cooking time(min): '))
    ingredients = input('Enter ingredients (separated by a comma): ').split(', ')
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_string = ', '.join(ingredients)
    insert_query = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    cursor.execute(insert_query, (name, ingredients_string, cooking_time, difficulty))
    conn.commit()
    print('Recipe Added\n')

def calculate_difficulty(cooking_time, ingredients):
    ingredients_len = len(ingredients)
    if cooking_time < 10 and ingredients_len < 4:
        return 'Easy'
    elif cooking_time < 10 and ingredients_len >= 4:
        return 'Medium'
    elif cooking_time >= 10 and ingredients_len < 4:
        return 'Intermediate'
    elif cooking_time >= 10 and ingredients_len >= 4:
        return 'Hard'
    else:
        print('Unable to calculate difficulty')

def display_recipe(cursor):
    cursor.execute('SELECT * FROM Recipes')
    results = cursor.fetchall()
    if len(results) == 0:
        print('No Recipes Have Been Entered\n')
        return

    for row in results:
        print('ID: ', row[0])
        print('Name: ', row[1])
        print('Ingredients: ', row[2])
        print('Cooking Time: ', row[3])
        print('Difficulty: ', row[4] + '\n')

def search_recipe(conn, cursor):
    cursor.execute('SELECT ingredients FROM Recipes')
    results = cursor.fetchall()
    if len(results) == 0:
        print('No Recipes Have Been Entered\n')
        return

    all_ingredients = []

    for result in results:
        ingredients = result[0].split(', ')
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
    for position, ingredient in enumerate(all_ingredients):
        print(f'Ingredient {position}: {ingredient}')

    try:
        ingredient_indexes = input('Enter the number of the ingredients you would like to search for (separated by commas): ').split(', ')
        search_ingredient = []
        for index in ingredient_indexes:
            ingredient_index = int(index)
            if ingredient_index < len(all_ingredients):
                search_ingredient.append(all_ingredients[ingredient_index])
    except ValueError:
        print('Invalid Input. Please select another number\n')
        return
    except IndexError:
        print('The number you have chosen is not listed\n')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}\n')
        return

    for ingredient in search_ingredient:
        cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE %s', ('%' + ingredient + '%',))
        result = cursor.fetchall()
        print(f'Recipes with {ingredient}')
        print(40 * '=')
        for row in result:
            print('Recipe: ', row[1])
            print('Ingredients: ', row[2])
            print('Cooking Time(min): ', row[3])
            print('Difficulty: ', row[4])

def update_recipe(conn, cursor):
    display_recipe(cursor)

    try:
        recipe_id = int(input('What recipe would you like to update?: '))
        column = input('Enter column to be updated: ')
        valid_columns = ['name', 'cooking_time', 'ingredients']
        if column not in valid_columns:
            print("Please choose either 'name', 'cooking_time', or 'ingredients'\n")
            return
        update_value = input(f'Enter updated value for {column}: ')
    except ValueError:
        print('Incorrect input, please try again\n')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return

    try:
        cursor.execute(f'UPDATE Recipes SET {column} = %s WHERE id = %s', (update_value, recipe_id))
        difficulty_query = 'UPDATE Recipes SET difficulty = %s WHERE id = %s'
        if column == 'cooking_time':
            cursor.execute('SELECT ingredients FROM Recipes WHERE id = %s', (recipe_id,))
            result = cursor.fetchone()
            ingredients = result[0]
            cursor.execute(difficulty_query, (calculate_difficulty(int(update_value), ingredients.split(', ')), recipe_id))
        elif column == 'ingredients':
            cursor.execute('SELECT cooking_time FROM Recipes WHERE id = %s', (recipe_id,))
            result = cursor.fetchone()
            cooking_time = result[0]
            cursor.execute(difficulty_query, (calculate_difficulty(cooking_time, update_value.split(', ')), recipe_id))
        conn.commit()
        print('Updated Recipe\n')
    except Exception as e:
        print(f'Unexpected Error: {e}')

def delete_recipe(conn, cursor):
    display_recipe(cursor)

    try:
        recipe_id = int(input('What recipe would you like to delete?: '))
    except ValueError:
        print('Enter a valid number')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return

    cursor.execute('DELETE FROM Recipes WHERE id = %s', (recipe_id,))
    conn.commit()
    print('Deleted Recipe\n')

if __name__ == "__main__":
    try:
        main_menu(conn, cursor)
    finally:
        cursor.close()
        conn.close()
