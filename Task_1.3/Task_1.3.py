recipes_list = []

ingredients_list = []

def take_recipe():
  name = input('Name: ')
  cooking_time = int(input('Cooking Time(min): '))
  ingredients = input('Ingredients: ').split(', ')
  recipe = {
    'Name': name,
    'Cooking Time': cooking_time,
    'Ingredients': ingredients
  }

  return recipe

n = int(input('How many recipes would you like to enter?: '))

for i in range(n):
  recipe = take_recipe()
  for ingredient in recipe['Ingredients']:
    if not ingredient in ingredients_list: 
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list: 
  if recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) < 4: 
    recipe['difficulty'] = 'Easy'
  elif recipe['Cooking Time'] < 10 and len(recipe['Ingredients']) >= 4:
    recipe['difficulty'] = 'Medium'
  elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) < 4:
    recipe['difficulty'] = 'Intermediate'
  elif recipe['Cooking Time'] >= 10 and len(recipe['Ingredients']) >= 4:
    recipe['difficulty'] = 'Hard'

for recipe in recipes_list:
  print('Recipe: ', recipe['Name'])
  print('Cooking Time (min): ', recipe['Cooking Time'])
  print('Ingredients: ')
  for ingredient in recipe['ngredients']:
    print(ingredient)
  print('Difficulty Level: ', recipe['difficulty'])


def print_ingredients():
  ingredients_list.sort()
  print('Ingredients Available for All Recipes')
  print('------------------------------')
  for ingredient in ingredients_list:
    print(ingredient)

print_ingredients()