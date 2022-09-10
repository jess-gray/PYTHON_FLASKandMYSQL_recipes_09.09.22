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
        query = 'INSERT INTO recipes (recipe_name, description, instructions, date_made, under_thirty, user_id) VALUES (%(recipe_name)s, %(description)s, %(instructions)s, %(date_made)s %(under_thirty)s %(user_id)s);'
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results