import pickle

def take_recipe():
  name = input('Enter recipe name: ')
  cooking_time = int(input('Enter the cooking time(min): '))
  ingredients = input('Enter ingredients (separated by a comma): ').split(', ')
  difficulty = calc_difficulty(cooking_time, ingredients)
  recipe = {
    'name': name, 
    'cooking_time': cooking_time,
    'ingredients': ingredients,
    'difficulty': difficulty,
  }
  return recipe

def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = 'Easy'
  elif cooking_time < 10 and len(ingredients) >= 4: 
    difficulty = 'Medium'
  elif cooking_time >= 10 and len(ingredients) < 4: 
    difficulty = 'Intermediate'
  elif cooking_time > 10 and len(ingredients) >= 4: 
    difficulty = 'Hard'

  return difficulty

filename = input('Enter the name of the file for your recipe: ')

try: 
  file = open(filename, 'rb')
  data = pickle.load(file)
  print('File load successful')
except FileNotFoundError:
  print('File does not exist')
  data = {
    'recipes_list': [],
    'all_ingredients': [],
  }
except: 
  print('Unexpected Error. Try again')
  data = {
    'recipes_list': [],
    'all_ingredients': [],
  }
else: 
  file.close()
finally: 
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']

n = int(input('How many recipes would you like to enter?: '))

for i in range(n): 
  recipe = take_recipe()
  recipes_list.append(recipe)
  for ingredient in recipe['ingredients']:
    if ingredient not in all_ingredients: 
      all_ingredients.append(ingredient)
  print('Recipe added')

data = {
  'recipes_list': recipes_list,
  'all_ingredients': all_ingredients 
}

with open(filename, 'wb') as file: 
  pickle.dump(data, file)