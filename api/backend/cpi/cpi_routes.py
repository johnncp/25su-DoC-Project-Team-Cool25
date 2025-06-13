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

cpi = Blueprint("cpi", __name__)

# gets all weekly working hours of full time adults
@cpi.route("/cpi", methods=["GET"])
def get_all_cpi():
    try: 
        cursor = db.get_db().cursor()
        country = request.args.get("country_name")
        year = request.args.get("year")

        query = "SELECT * FROM EUCPI WHERE 1=1"
        params = []

        if country:
            query += " AND country_name = %s"
            params.append(country)
        if year: 
            query += " AND year = %s"
            params.append(year)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        item = cursor.fetchall()

        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(item)} CPI')
        return jsonify(item), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_cpi: {str(e)}')
        return jsonify({"error": str(e)}), 500
