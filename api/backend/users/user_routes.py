from flask import (
    Blueprint,
    request,
    jsonify,
    make_response,
    current_app,
    redirect,
    url_for,
)
import json
from backend.db_connection import db
from mysql.connector import Error
import datetime

users = Blueprint("users", __name__)

# get all users with specific role
@users.route("/role/<int:role_id>", methods=["GET"])
def get_users_by_role(role_id):
    try:
        cursor = db.get_db().cursor()
        
        query = """
            SELECT user_id,
            first_name,
            last_name,
            age,
            occupation,
            country_code,
            role_id 
            FROM User
            WHERE role_id = %s
            ORDER BY last_name, first_name;
        """
        
        cursor.execute(query, (role_id,))
        
        users = cursor.fetchall()
        cursor.close()
        
        # Convert to list of dicts
        user_list = []
        for user in users:
            user_dict = {
                'user_id': user['user_id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'age': user['age'],
                'occupation': user['occupation'],
                'country_code': user['country_code'],
                'role_id': user['role_id']
            }
            user_list.append(user_dict)
        
        return jsonify(user_list), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching users by role: {e} ({type(e).__name__})")
        return jsonify({'error': 'Failed to fetch users'}), 500