import db

def add_recipe(name, ingredients, instruction, user_id):
    sql = "INSERT INTO recipes (name, ingredients, instruction, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, ingredients, instruction, user_id])

def get_recipes():
    sql = "SELECT id, name FROM recipes ORDER BY id DESC"
    return db.query(sql)

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
    return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, name, ingredients, instruction):
    sql = """UPDATE recipes SET name = ?,
                                ingredients = ?,
                                instruction = ?
                             WHERE id = ?"""
    db.execute(sql, [name, ingredients, instruction, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def search_recipes(query):
    sql = """SELECT id, name
             FROM recipes
             WHERE name LIKE ? OR ingredients LIKE ?
             ORDER BY id DESC"""
    search = "%" + query + "%"
    return db.query(sql, [search, search])
