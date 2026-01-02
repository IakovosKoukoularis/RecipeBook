import sqlite3
from tkinter import messagebox

class RecipeDB:
    
    def __init__(self, db_name="Recipes.db"):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
       
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Δημιουργει ενα table αμα δεν υπαρχει
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    Name TEXT PRIMARY KEY,
                    Category TEXT NOT NULL,
                    Difficulty TEXT NOT NULL,
                    Time INTEGER NOT NULL,
                    Ingredients TEXT NOT NULL,
                    Steps TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_recipe(self, recipe_data):
       
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO recipes 
                    (Name, Category, Difficulty, Time, Ingredients, Steps)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    recipe_data['Name'],
                    recipe_data['Category'],
                    recipe_data['Difficulty'],
                    int(recipe_data['Time']),
                    ";".join(recipe_data['Ingredients']),  # Μετατρεπει σε string γιατι δεν μπορει να το αποθηκευσει αλλιως
                    str(recipe_data['Steps'])  # Μετατρεπει σε string γιατι δεν μπορει να το αποθηκευσει αλλιως
                ))
                conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save recipe: {str(e)}")
            return False

    def load_recipes(self):
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM recipes")
                recipes = {}
                for row in cursor.fetchall():
                    name, category, difficulty, time, ingredients, steps, _= row
                    recipes[name] = {
                        'Category': category,
                        'Difficulty': difficulty,
                        'Time': time,
                        'Ingredients': ingredients.split(";"),  # Μετατρεπει παλι σε λιστα
                        'Steps': eval(steps)  # Μετατρεπει παλι σε λεξικο 
                    } 
                return recipes
        except sqlite3.Error as e:
            messagebox.showerror(title="Database Error", message=f"Failed to load recipes: {str(e)}")
            return {}

    def delete_recipe(self, recipe_name):
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM recipes WHERE Name = ?", (recipe_name,))
                conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror(title="Database Error", message=f"Failed to delete recipe: {str(e)}")
            return False
        
    def search_recipes(self, query):
        """Searches the database for recipes matching the query in name, category, ingredients, or steps."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Using LIKE for partial matching and case-insensitivity
                # Searching in name, category, ingredients, and steps
                search_term = f"%{query}%"
                cursor.execute("""
                    SELECT name, category, difficulty, time, ingredients, steps FROM recipes 
                    WHERE Name LIKE ? OR Category LIKE ? OR Ingredients LIKE ? OR Steps LIKE ?
                    ORDER BY name
                """, (search_term, search_term, search_term, search_term))

                recipes = []
                for row in cursor.fetchall():
                    # We return the recipe data in a format suitable for the Treeview
                    recipes.append(row) 
                return recipes
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to search recipes: {str(e)}")
            return []

    def filter_recipes(self, category=None, difficulty=None, max_time=None):
        """Filters recipes based on provided criteria."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                query = "SELECT name, category, difficulty, time, ingredients, steps FROM recipes WHERE 1=1"
                params = []

                if category and category != "Any":
                    query += " AND Category = ?"
                    params.append(category)

                if difficulty and difficulty != "Any":
                    query += " AND Difficulty = ?"
                    params.append(difficulty)

                if max_time is not None:
                    query += " AND Time <= ?"
                    params.append(max_time)

                query += " ORDER BY name"

                cursor.execute(query, params)

                recipes = []
                for row in cursor.fetchall():
                    recipes.append(row)
                return recipes

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to filter recipes: {str(e)}")
            return []