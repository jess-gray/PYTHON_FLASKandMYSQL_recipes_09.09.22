from flask_app import app
from flask import Flask, render_template, request, redirect, session 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes/new') #form to create recipe
def create_recipe():
    return render_template("create_recipe.html")

@app.route('/submit_recipe', methods = ['POST']) #this is to create a recipe
def submit_recipe():
    print(request.form)
    if not Recipe.validate_create_recipe(request.form): #validations
        return redirect('/recipes/new') 
    data = {
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
        "user_id" : session['user_id'] #this is coming from login 
    }
    Recipe.create(data) 
    return redirect ('/dashboard')


@app.route('/recipes/<int:id>') #this is to view one user (this doesn't work, missing positional arguemnt)
def view_recipe(id):
    data = { #this is pulling recipe id
        'id' : id
    }
    user_data = { #this is pulling id of user logged in
        'id' : session['user_id'] 
    }
    a_recipe = Recipe.get_one_with_user(data)
    a_user = User.get_by_id(user_data)
    return render_template('read_one.html', one_recipe = a_recipe, active_user = a_user)

@app.route('/delete/<int:id>', methods = ["POST"]) #this is to delete recipe
def delete(id):
    data = {
        'id' : id
    }
    Recipe.delete(data)
    return redirect ('/dashboard')

@app.route('/edit/<int:id>') #this is the edit page/form
def edit(id):
    data = { #this is pulling recipe id
        'id' : id
    }
    user_data = { #this is pulling id of user logged in
        'id' : session['user_id'] 
    }
    a_recipe = Recipe.get_one_with_user(data)
    a_user = User.get_by_id(user_data)
    return render_template('edit_recipe.html', one_recipe = a_recipe, active_user = a_user)

@app.route('/submit_edit/<int:id>', methods = ['POST']) #this is to actually edit the user
def update(id):
    if not Recipe.validate_edit_recipe(request.form): #validations
        return redirect('/recipes/new') 
    data = {
        'id' : id,
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_thirty' : request.form['under_thirty'],
    }
    Recipe.update(data)
    return redirect('/dashboard')