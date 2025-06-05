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

hours = Blueprint("hours", __name__)

# gets all weekly working hours of full time adults
@hours.route("/hours", methods=["GET"])
def get_all_hours():
    try: 
        cursor = db.get_db().cursor()
        country = request.args.get("country_code")

        query = "SELECT * FROM EUEmployment WHERE 1=1"
        params = []

        if country:
            query += " AND country_code = %s"
            params.append(country)

        cursor.execute(query, params)
        locations = cursor.fetchall()
        cursor.close()

    except Error as e:
        current_app.logger.error(f'Database error in get_all_locations: {str(e)}')
        return jsonify({"error": str(e)}), 500
