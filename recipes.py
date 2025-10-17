import db

def add_recipe(name, ingredients, instruction, user_id, classes):
    sql = "INSERT INTO recipes (name, ingredients, instruction, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, ingredients, instruction, user_id])

    recipe_id = db.last_insert_id()

    sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [recipe_id, title, value])


def get_recipes():
    sql = "SELECT id, name FROM recipes ORDER BY id DESC"
    return db.query(sql)

def get_classes(recipe_id):
    sql = "SELECT title, value FROM recipe_classes WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    query = db.query(sql)

    classes = {}
    for title, value in query:
        classes[title] = []
    for title, value in query:
        classes[title].append(value)
    return classes

def get_recipe(recipe_id):
    sql = """SELECT recipes.name,
                    recipes.id,
                    recipes.ingredients,
                    recipes.instruction,
                    users.username,
                    users.id user_id
             FROM recipes, users
             WHERE recipes.user_id = users.id AND
                   recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def update_recipe(recipe_id, name, ingredients, instruction, classes):
    sql = """UPDATE recipes SET name = ?,
                                ingredients = ?,
                                instruction = ?
                             WHERE id = ?"""
    db.execute(sql, [name, ingredients, instruction, recipe_id])

    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO recipe_classes (recipe_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [recipe_id, title, value])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def search_recipes(query):
    sql = """SELECT id, name
             FROM recipes
             WHERE name LIKE ? OR ingredients LIKE ?
             ORDER BY id DESC"""
    search = "%" + query + "%"
    return db.query(sql, [search, search])
