# Import flask and other models.
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

#MySQL database.
database = "recipes"

class Recipe:
    def __init__(self, data):
        self.id = data["id"] # Right side is the name of the MySQL column.
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date = data["date"]
        self.under_30_mins = data["under_30_mins"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        
    @classmethod
    def get_all(cls):
        query = '''
                    SELECT * FROM recipes;
                '''
        results = connectToMySQL(database).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def save(cls, data):
        query = '''
                    INSERT INTO recipes (name, description, instructions, date, under_30_mins, users_id)
                    VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30_mins)s, %(user_id)s);
                '''
        connectToMySQL(database).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = ''' UPDATE recipes
                    SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, under_30_mins = %(under_30_mins)s
                    WHERE ID = %(id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, data):
        query = ''' DELETE FROM recipes
            WHERE ID = %(id)s;
        '''
        connectToMySQL(database).query_db(query, data)
        
    @classmethod
    def get_recipe_by_id(cls, data):
        query = ''' SELECT * FROM recipes
                    WHERE ID = %(id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results[0]
    
    # @classmethod
    # def get_only_unselected_books(cls, data):
    #     query = '''
    #                 SELECT * FROM books
    #                 WHERE books.id NOT IN
    #                 (SELECT book_id FROM favorites
    #                 WHERE author_id = %(author_id)s);
    #             '''
    #     results = connectToMySQL(database).query_db(query, data)
    #     books = []
    #     for book in results:
    #         books.append(cls(book))
    #     return books
    
    # @classmethod
    # def save_book_to_author(cls, data):
    #     query = '''
    #                 INSERT INTO favorites (book_id, author_id)
    #                 VALUES (%(id)s, %(author_id)s);
    #             '''
    #     connectToMySQL(database).query_db(query, data)
    
    @classmethod
    def connect_users_to_recipes_join(cls):
        query = '''
                    SELECT * FROM recipes
                    JOIN users ON users.id = recipes.users_id
                '''
        results = connectToMySQL(database).query_db(query)
        return results
    
    @classmethod
    def connect_user_to_recipe_join(cls, data):
        query = '''
                    SELECT * FROM users
                    JOIN recipes ON users.id = recipes.users_id
                    WHERE recipes.id = %(id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results[0]
    
    # @classmethod
    # def get_all_recipes_by_user_join(cls, data):
    #     query = '''
    #                 SELECT * FROM recipes
    #                 JOIN users ON users.id = recipes.users_id
    #                 WHERE recipes.users_id = %(id)s;
    #             '''
    #     results = connectToMySQL(database).query_db(query, data)
    #     output = []
    #     for row in results:
    #         this_recipe = cls(row)
            
    #         user_data = {
    #             "id": row["users.id"],
    #             "first_name": row["first_name"],
    #             "last_name": row["last_name"],
    #             "email": row["email"],
    #             "created_at": row["users.created_at"],
    #             "updated_at": row["users.updated_at"]
    #         }
            
    #         this_recipe.creator = user.User(user_data)
    #         output.append(this_recipe)
    #     return output
    
    # Validate create recipe form.
    @staticmethod
    def validate_create_recipe_form(recipe):
        is_valid = True
        
        if len(recipe["name"]) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        return is_valid