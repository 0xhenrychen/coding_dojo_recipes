from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe

@app.route("/recipes")
def recipes_all_page():
    if "first_name" not in session:
        return redirect("/")
    recipes_with_users = recipe.Recipe.connect_users_to_recipes_join()
    return render_template("recipes.html", recipes = recipes_with_users)

@app.route("/recipes/view/<int:recipe_id>")
def recipe_single_page(recipe_id):
    data = {
                "id": recipe_id
    }
    one_recipe_with_user = recipe.Recipe.connect_user_to_recipe_join(data)
    return render_template("recipe_view.html", recipe = one_recipe_with_user)

@app.route("/recipes/new")
def create_recipe_page():
    if "first_name" not in session:
        return redirect("/")
    return render_template("recipe_new.html")

@app.route("/recipes/edit/<int:recipe_id>")
def update_recipe_page(recipe_id):
    if "first_name" not in session:
        return redirect("/")
    data = {
                "id": recipe_id
    }
    one_recipe = recipe.Recipe.get_recipe_by_id(data)
    return render_template("recipe_edit.html", recipe = one_recipe)

@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    data = {
                "id": recipe_id
    }
    recipe.Recipe.delete(data)
    return redirect("/recipes")

@app.route("/create_recipe_form", methods=["POST"])
def create_recipe_form():
    data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date": request.form["date"],
            "under_30_mins": request.form["under_30_mins"]
    }
    if not recipe.Recipe.validate_create_recipe_form(data):
        return redirect("/recipes/new")
    
    email = {
                "email": session["email"]
    }
    
    this_user = user.User.get_user_by_email(email)
    data["user_id"] = this_user["id"]
    recipe.Recipe.save(data)
    return redirect("/recipes")

@app.route("/update_recipe_form", methods=["POST"])
def update_recipe_form():
    data = {
            "id": request.form["id"],
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date": request.form["date"],
            "under_30_mins": request.form["under_30_mins"]
    }
    if not recipe.Recipe.validate_create_recipe_form(data):
        return redirect("/recipes/update")
    recipe.Recipe.edit(data)
    return redirect("/recipes")
