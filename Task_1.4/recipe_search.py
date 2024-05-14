import pickle

def display_recipe(recipe):
  print('Recipe: ', recipe['name'])
  print('Cooking Time(min): ', str(recipe['cooking_time']))
  print('Ingredients: ')
  for ingredient in recipe['ingredients']:
    print(ingredient)
  print('Difficulty: ', recipe['difficulty'])

def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    recipes_list = data['recipes_list']
    for position, ingredient in enumerate(all_ingredients):
        print('Ingredient ' + str(position) + ': ' + ingredient)
    try:
        ingredient_index = int(input('Enter the number of the ingredient you would like to search for: '))
        ingredient_searched = all_ingredients[ingredient_index]
    except ValueError:
        print('One or more of your inputs are not numbers')
    except IndexError:
        print('Number chosen is not on the list')
    except:
        print('Unexpected error occured')
    else:
        for recipe in recipes_list:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

filename = input('Enter the name of the file for your recipe: ')

try: 
  file = open(filename, 'rb')
  data = pickle.load(file)
except FileNotFoundError:
  print('File does not exist')
except: 
  print('Unexpected error occured')
else: 
  file.close()
  search_ingredient(data)