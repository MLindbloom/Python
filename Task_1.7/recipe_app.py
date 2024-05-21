from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Connecting SQLAlchemy to the database
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Declarative Base Class function
Base = declarative_base()

# Generating a Session
Session = sessionmaker(bind=engine)
session = Session()


# Create Table in database
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(225))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __refr__(self):
        return f"Recipe ID: {self.id}, Name: {self.name}, Difficulty: {self.difficulty}"

    def __str__(self):
        return (
            f"\nRecipe: {self.name}\n"
            f"{30*'='}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time(min): {self.cooking_time}\n"
            f"Difficulty: {self.difficulty}\n"
            f"\n"
        )

    # Calculate Recipe Difficulty
    def calculate_difficulty(self):
        ingredients_len = len(self.ingredients.split(", "))
        self.difficulty = ""
        if self.cooking_time < 10 and ingredients_len < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and ingredients_len >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and ingredients_len < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and ingredients_len >= 4:
            self.difficulty = "Hard"

    # Return the Ingredients as a List
    def return_ingredients_as_list(self):
        return [] if self.ingredients == "" else self.ingredients.split(", ")


# Create tables of all models
Base.metadata.create_all(engine)


# Create Recipe Function
class Menu(Recipe):
    def create_recipe(self):
        name = self.name_input()
        if name is None:
            return
        ingredients = self.ingredients_input()
        if ingredients is None:
            return
        cooking_time = self.cooking_time_input()
        if cooking_time is None:
            return

        recipe_entry = Recipe(
            name=name, ingredients=ingredients, cooking_time=cooking_time
        )
        recipe_entry.calculate_difficulty()
        session.add(recipe_entry)
        session.commit()
        print("Recipe Successfully Added!\n")

    # Recipe Name
    def name_input(self):
        name = input("Enter Recipe Name: ")
        if len(name) > 50:
            print("\nRecipe Name is too long. Limit 50 characters.\n")
            return None
        elif not name.replace(" ", "").isalnum():
            print("Invalid Input. Please enter a valid name or number.\n")
            return None
        else:
            return name

    # Recipe Ingredients
    def ingredients_input(self):
        ingredients = []
        ingredients_number = input("Enter the number of ingredients: ")
        if ingredients_number.isnumeric() == False or int(ingredients_number) <= 0:
            print("\nPlease enter at least one ingredient\n")
            return None
        for _ in range(int(ingredients_number)):
            ingredient = input("Enter an ingredient: ")
            if ingredient != "":
                ingredients.append(ingredient)
            else:
                break
        ingredients = ", ".join(ingredients)
        return ingredients

    # Recipe Cooking Time
    def cooking_time_input(self):
        try:
            cooking_time = int(input("Enter Cooking Time(min): "))
            return cooking_time
        except ValueError:
            print("\nEnter a valid number\n")
            return None

    # View All Recipes
    def view_all_recipes(self):
        all_recipes = session.query(Recipe).all()
        if all_recipes:
            for recipe in all_recipes:
                print(recipe)
        else:
            print("\nNo recipes have been entered\n")
            return None

    # Search by Ingredients
    def search_by_ingredients(self):
        if session.query(Recipe).count() == 0:
            print("\nNo recipes have been entered\n")
            return None

        results = session.query(Recipe.ingredients).all()
        all_ingredients = []

        for result in results:
            ingredients_list = result[0].split(", ")
            for ingredient in ingredients_list:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)

        for position, ingredient in enumerate(all_ingredients):
            print("Ingredient " + str(position) + ": " + ingredient)

        try:
            ingredient_indexes = input(
                "Enter the numbers for the ingredients you would like to search: "
            ).split(" ")
            search_ingredients = []
            for index in ingredient_indexes:
                ingredient_index = int(index)
                search_ingredients.append(all_ingredients[ingredient_index])
        except ValueError:
            print("Invalid Input\n")
            return
        except IndexError:
            print("Entry Not Found\n")
            return
        except:
            print("Unexpected Error\n")

        conditions = []
        for search_ingredient in search_ingredients:
            like_term = f"%{search_ingredient}%"
            conditions.append(Recipe.ingredients.like(like_term))
        filtered_recipes = session.query(Recipe).filter(*conditions).all()
        if len(filtered_recipes) <= 0:
            print("No Recipes Found\n")
        else:
            print("\nRecipe(s) containing the ingredient(s):\n")
            for filtered_recipe in filtered_recipes:
                print(filtered_recipe)

    # Recipe by ID
    def choose_recipe_id(self):
        if session.query(Recipe).count() == 0:
            print("\nNo Recipes have be entered\n")
            return None

        results = session.query(Recipe.id, Recipe.name).all()
        recipe_ids = [result[0] for result in results]

        for result in results:
            print("\nRecipe ID:", result[0], "- Recipe Name:", result[1] + "\n")

        try:
            recipe_id = int(input("Enter the ID for the Recipe you want to choose: "))
        except ValueError:
            print("\nInvalid Input\n")
            return None
        except:
            print("Unexpected Error\n")

        if recipe_id not in recipe_ids:
            print("\nID not found\n")
            return None
        else:
            return recipe_id

    # Edit Recipe
    def edit_recipe(self):
        recipe_id = self.choose_recipe_id()
        if recipe_id is None:
            return

        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        print("Recipe")
        print("-" * 30)
        print("1. Name:", recipe_to_edit.name)
        print("2. Ingredients: ", recipe_to_edit.ingredients)
        print("3. Cooking time: ", recipe_to_edit.cooking_time)

        try:
            attribute = int(
                input("Enter the number of the attribute you would like to update: ")
            )
        except ValueError:
            print("\nInvalid Input\n")
            return
        except:
            print("\nUnexpected Error\n")

        if attribute == 1:
            name_input = self.name_input()
            if name_input is None:
                return
            session.query(Recipe).filter(Recipe.id == recipe_id).update(
                {Recipe.name: name_input}
            )
        elif attribute == 2:
            ingredients_input = self.ingredients_input()
            if ingredients_input is None:
                return
            session.query(Recipe).filter(Recipe.id == recipe_id).update(
                {Recipe.ingredients: ingredients_input}
            )
        elif attribute == 3:
            cooking_time_input = self.cooking_time_input()
            if cooking_time_input is None:
                return
            session.query(Recipe).filter(Recipe.id == recipe_id).update(
                {Recipe.cooking_time: cooking_time_input}
            )
        else:
            print("Invalid Input")
            return None

        if attribute == 2 or attribute == 3:
            recipe_to_edit.calculate_difficulty()
        session.commit()
        print("\nRecipe Updated\n")

    # Delete Recipe
    def delete_recipe(self):
        recipe_id = self.choose_recipe_id()
        if recipe_id is None:
            return

        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        decision = input(
            f"Confirm you want to delete {recipe_to_delete.name}! Type 'yes': "
        )

        if decision.lower() == "yes":
            session.delete(recipe_to_delete)
            session.commit()
            print("\nRecipe Deleted\n")
        else:
            print("\nRecipe was not deleted\n")
            return None

    # Main Menu
    def display_menu(self):
        choice = ""
        while choice != "quit":
            print("\n\n" + 50 * "=")
            print("Welcome to Recipe App!")
            print(50 * "=")
            print("Main Menu")
            print(50 * "=")
            print("Please Choose an Option: \n")
            print("\t1. Create New Recipe")
            print("\t2. View All Recipes")
            print("\t3. Search for Recipes by Ingredients")
            print("\t4. Edit a Recipe")
            print("\t5. Delete a Recipe")
            print("\tType 'quit' to exit the app\n")
            choice = input("Your choice: ")

            if choice == "1":
                self.create_recipe()
            elif choice == "2":
                self.view_all_recipes()
            elif choice == "3":
                self.search_by_ingredients()
            elif choice == "4":
                self.edit_recipe()
            elif choice == "5":
                self.delete_recipe()
            elif choice == "quit":
                print("Thanks for using Recipe App!")
            elif choice != "quit":
                print("Invalid Input")
                session.close()
                engine.dispose()
                break
            else:
                return None


menu = Menu()
menu.display_menu()
