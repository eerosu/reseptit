import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import recipes
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    classes = recipes.get_classes(recipe_id)
    ratings = recipes.get_ratings(recipe_id)
    average = recipes.get_average_rating(recipe_id)
    return render_template("show_recipe.html", recipe=recipe, classes=classes, ratings=ratings, average=average)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)


@app.route("/add_recipe")
def add_recipe():
    require_login()
    classes = recipes.get_all_classes()
    return render_template("add_recipe.html", classes=classes)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()

    name = request.form["name"]
    if not name or len(name) > 60:
        abort(403)
    ingredients = request.form["ingredients"]
    if not ingredients or len(ingredients) > 1000:
        abort(403)
    instruction = request.form["instruction"]
    if not instruction or len(instruction) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = recipes.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes:
                abort(403)
            if entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    recipes.add_recipe(name, ingredients, instruction, user_id, classes)
    return redirect("/")

@app.route("/create_rating", methods=["POST"])
def create_rating():
    require_login()

    recipe_id = request.form["recipe_id"]
    if not recipe_id:
        abort(403)

    user_id = session["user_id"]

    stars = request.form["rating"]
    comment = request.form["comment"]

    recipes.add_rating(recipe_id, user_id, stars, comment)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)
    classes = recipes.get_all_classes()
    selected = {}
    for selection in classes:
        selected[selection] = ""
    for entry in recipes.get_classes(recipe_id):
        selected[entry["title"]] = entry["value"]
    return render_template("edit_recipe.html", recipe=recipe, classes=classes, selected=selected)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    recipe_id = request.form["recipe_id"]
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    name = request.form["name"]
    if not name or len(name) > 60:
        abort(403)
    ingredients = request.form["ingredients"]
    if not ingredients or len(ingredients) > 1000:
        abort(403)
    instruction = request.form["instruction"]
    if not instruction or len(instruction) > 1000:
        abort(403)

    all_classes = recipes.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            entry_title, entry_value = entry.split(":")
            if entry_title not in all_classes:
                abort(403)
            if entry_value not in all_classes[entry_title]:
                abort(403)
            classes.append((entry_title, entry_value))

    recipes.update_recipe(recipe_id, name, ingredients, instruction, classes)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/search_recipes")
def search_recipes():
    query = request.args.get("query")
    if query:
        search_results = recipes.search_recipes(query)
    else:
        query = ""
        search_results = []
    return render_template("search_recipes.html", query=query, search_results=search_results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")
