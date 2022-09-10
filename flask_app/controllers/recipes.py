from flask_app import app
from flask import Flask, render_template, request, redirect, session 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes/new')
def create_recipe():
    return render_template("create_recipe.html")

@app.route('/submit_recipe', methods = ['POST'])
def submit_recipe():
#add in valadations 
    data = {
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
        "user_id" : session['user_id']
    }
    Recipe.create(data)
    return redirect ('/dashboard')