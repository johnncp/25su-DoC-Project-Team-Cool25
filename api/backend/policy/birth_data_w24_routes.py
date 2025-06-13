from flask import Blueprint, request, jsonify, make_response, current_app
import pandas as pd
from backend.db_connection import db

# Blueprint for birth data routes
birth_data_routes = Blueprint('birth_data_routes', __name__)

@birth_data_routes.route('/api/birth-rates', methods=['GET'])
def get_birth_rates():
    current_app.logger.info("GET /api/birth-rates handler")
    try:
        query = """
        SELECT 
            country,
            year,
            birth_rate_per_thousand,
            live_births
        FROM EUBirthData_With2024
        WHERE birth_rate_per_thousand IS NOT NULL
        ORDER BY country, year
        """

        cursor = db.get_db().cursor()
        cursor.execute(query)
        
        # Fetch all results
        results = cursor.fetchall()
        cursor.close()

        return jsonify(results), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching birth data: {str(e)}")
        current_app.logger.error(f"Error type: {type(e)}")
        response = make_response(jsonify({
            "error": "Error fetching birth data",
            "message": str(e)
        }))
        response.status_code = 500
        return response