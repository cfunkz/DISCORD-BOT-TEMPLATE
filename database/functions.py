import datetime
import json
from .database import execute_query, fetch_all, fetch_one

class User:
    
    # Functio to add user
    @classmethod
    def add_user(cls, id: int):
        default_inventory = json.dumps({'apple': 1, 'orange': 2})
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = """
        INSERT INTO users (id, xp, bank, inventory, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        execute_query(query, (id, 0, 5000, default_inventory, created_at))

    # Function to get user information by ID
    @classmethod
    def get_user(cls, user_id: int):
        query = "SELECT * FROM users WHERE id = ?"
        return fetch_one(query, (user_id,))

    # Function to update inventory in the database
    @classmethod
    def update_inventory(cls, user_id: int, new_inventory: str):
        query = "UPDATE users SET inventory = ? WHERE id = ?"
        execute_query(query, (new_inventory, user_id))

    # Function to add XP to a user
    @classmethod
    def add_xp(cls, user_id: int, amount: int):
        query = "UPDATE users SET xp = xp + ? WHERE id = ?"
        execute_query(query, (amount, user_id))

# Function to get all users
def get_all_users():
    query = "SELECT * FROM users"
    return fetch_all(query)
