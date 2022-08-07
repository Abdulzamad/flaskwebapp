from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql.expression import func
from app import app, db
from app.forms import AddRecipieForm
from app.models import User, Recipe
from werkzeug.urls import url_parse
import random
import re

@app.route('/')
@app.route('/index')
def index():
    random_recipes =  Recipe.query.order_by(func.rand()).all()[:3]
    print(random_recipes)
    return render_template('index.html' ,random_recipes=random_recipes, user=current_user)

@app.route('/recipes')
def recipes():
    query = request.args.get("query" , "")
    recipes = Recipe.query.filter(Recipe.title.like("%"+query+"%")).all()
    
    return render_template('recipes.html', recipes=recipes , query=query , user=current_user)


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return render_template('recipe.html', recipe=recipe , user=current_user)
    # return recipe.title


@login_required
@app.route('/my-recipes')
def myRecipes():
    query = request.args.get("query" , "")
    recipes = Recipe.query.filter(Recipe.title.like("%"+query+"%") ,Recipe.user_id==current_user.id  ).all()
    
    return render_template('my-recipies.html', recipes=recipes , query=query , user=current_user)

@login_required
@app.route('/add-new',  methods=['GET', 'POST'])
def newRecipes():
    form = AddRecipieForm()
    if form.validate_on_submit():
        s=","
        user = Recipe(title=form.title.data, description=form.description.data, ingredients=form.ingredients.data, instructions=form.instructions.data , user_id=current_user.id)
        user.tags = s.join(re.split('[, \s]', form.tags.data))
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Please login below.')
        return redirect('/my-recipes')
    return render_template('new-recipie.html', recipes=recipes , form=form , user=current_user)

@login_required
@app.route('/edit/<recipe_id>',  methods=['GET', 'POST'])
def editPost(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id , user_id=current_user.id).first_or_404()
    form = AddRecipieForm()
    if form.validate_on_submit():
        s=","
        
        recipe.title=form.title.data
        recipe.description=form.description.data 
        recipe.ingredients=form.ingredients.data
        recipe.instructions=form.instructions.data 
        recipe.user_id=current_user.id
        recipe.tags = s.join(re.split('[, \s]', form.tags.data))
        db.session.commit()
        db.session.flush()
    form.title.data = recipe.title
    form.tags.data = recipe.tags
    form.description.data = recipe.description
    form.ingredients.data = recipe.ingredients
    form.instructions.data = recipe.instructions

    return render_template('edit-recipie.html', recipe=recipe , form=form , user=current_user)
@login_required
@app.route('/delete/<recipe_id>',  methods=['GET', 'DELETE'])
def deletePost(recipe_id):

    recipe = Recipe.query.filter_by(id=recipe_id , user_id=current_user.id).first_or_404()
    if request.method == "DELETE":
        
        db.session.delete(recipe)
        db.session.commit()
        db.session.flush()
        return "ok"
    return render_template('delete-recipie.html', recipe=recipe  , user=current_user)
