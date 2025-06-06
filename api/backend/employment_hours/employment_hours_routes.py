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
@hours.route("/weeklyhours", methods=["GET"])
def get_all_hours():
    try: 
        cursor = db.get_db().cursor()
        country = request.args.get("country_code")
        year = request.args.get("year")
        sex = request.args.get("sex")

        query = "SELECT eue_id, emp_all, country_code, year, sex, age_group FROM EUEmployment WHERE 1=1"
        params = []

        if country:
            query += " AND country_code = %s"
            params.append(country)
        if year: 
            query += " AND year = %s"
            params.append(year)
        if sex:
            query += " AND sex = %s"
            params.append(sex)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        hours = cursor.fetchall()

        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(hours)} Weekly Hours')
        return jsonify(hours), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_hours: {str(e)}')
        return jsonify({"error": str(e)}), 500
