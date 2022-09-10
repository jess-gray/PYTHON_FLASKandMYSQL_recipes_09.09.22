from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']    #add additional attributres as needed!!
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None #this is to associate the other table
    
    @classmethod #this is actually adding a new recipe
    def create(cls, data):
        query = 'INSERT INTO recipes (recipe_name, description, instructions, date_made, under_thirty, user_id) VALUES (%(recipe_name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s, %(user_id)s);'
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results
    
    @classmethod  #this is to get information from foreign key
    def get_all_with_user(cls):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id'
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : None,
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_recipe.owner = user_obj
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_one_with_user(cls, data): #to get one recipe info
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'
        results = connectToMySQL('recipes').query_db(query, data)
        one_recipe = cls(results[0])
        user_data = {
                'id': results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : None,
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
        one_recipe.owner = user.User(user_data)    
        print(results)
        return one_recipe
    
    @classmethod #this is to delete recipe
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results

    @classmethod #this is to actually edit the user
    def update(cls, data):
        query = 'UPDATE recipes set recipe_name = %(recipe_name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_thirty = %(under_thirty)s WHERE id = %(id)s;'
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results

    @staticmethod #validations for creating recipe 
    def validate_create_recipe(reqForm):
        is_valid = True
        if len(reqForm['recipe_name']) <3:
            flash ('recipe name must be at least 3 characters!')
            is_valid = False
        if len(reqForm['description']) <3:
            flash ('description must be at least 3 characters!')
            is_valid = False
        if len(reqForm['instructions']) <3:
            flash ('instructions name must be at least 3 characters!')
            is_valid = False
        if len(reqForm['date_made']) < 1:
            flash('Please add date made')
            is_valid = False
        return is_valid
    
    @staticmethod #validations for editing recipe 
    def validate_edit_recipe(reqForm):
        is_valid = True
        if len(reqForm['recipe_name']) <3:
            flash ('recipe name must not be blank!')
            is_valid = False
        if len(reqForm['description']) <3:
            flash ('description must not be blank!')
            is_valid = False
        if len(reqForm['instructions']) <3:
            flash ('instructions name must not be blank!')
            is_valid = False
        if len(reqForm['date_made']) < 1:
            flash('Please add date made')
            is_valid = False
        return is_valid
