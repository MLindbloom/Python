class ShoppingList(object):
  def __init__(self, list_name):
    self.list_name = list_name
    self.shopping_list = []

  def add_item(self, item):
    self.item = item
    if item not in self.shopping_list:
      self.shopping_list.append(item)
      print(item, 'was added to shopping list')
    else: 
      print(item, 'is already on list')

  def remove_item(self, item):
    self.item = item
    if item in self.shopping_list:
      self.shopping_list.remove(item)
      print(item, 'was removed from list')
    else: 
      print(item, 'is not in shopping list')

  def view_list(self):
      print('\nItems in ' + str(self.list_name) + '\n' + 40*'-')
      for item in self.shopping_list:
        print(' - ' + str(item))

pet_store_list = ShoppingList('Pet Store Shopping List')

pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collar')
pet_store_list.add_item('flea collar')

pet_store_list.remove_item('flea collar')

pet_store_list.add_item('frisbee')

pet_store_list.view_list()