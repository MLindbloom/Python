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
  for ingredient in recipe['ingredients']:
    if not ingredient in ingredients_list: 
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list: 
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4: 
    recipe['difficulty'] = 'Easy'
  elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'Medium'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
    recipe['difficulty'] = 'Intermediate'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'Hard'

for recipe in recipes_list:
  print('Recipe: ', recipe['name'])
  print('Cooking Time (min): ', recipe['cooking_time'])
  print('Ingredients: ')
  for ingredient in recipe['Ingredients']:
    print(ingredient)
  print('Difficulty Level: ', recipe['difficulty'])


def print_ingredients():
  ingredients_list.sort()
  print('Ingredients Available for All Recipes')
  print('------------------------------')
  for ingredient in ingredients_list:
    print(ingredient)

print_ingredients()