import db

def add_recipe(name, classes, instruction, user_id):
    sql = "INSERT INTO recipes (name, classes, instruction, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [name, classes, instruction, user_id])

def get_recipes():
    sql = "SELECT id, name FROM recipes ORDER BY id DESC"
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT recipes.name,
                    recipes.classes,
                    recipes.instruction,
                    users.username
             FROM recipes, users
             WHERE recipes.user_id = users.id AND
                   recipes.id = ?"""
    return db.query(sql, [recipe_id])[0]
