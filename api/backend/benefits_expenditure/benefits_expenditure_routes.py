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

benefits = Blueprint("benfits", __name__)

# gets all benefit expenditures
@benefits.route("/benefit", methods=["GET"])
def get_all_benefits():
    try: 
        cursor = db.get_db().cursor()
        country = request.args.get("country_code")
        year = request.args.get("year")
        benefit_type = request.args.get("benefit_type")
        target_group = request.args.get("target_group")
        unit_measured = request.args.get("unit_measured")

        query = "SELECT cfb_id, benefit_type, target_group, unit_measured, country_code, year, expenditure FROM Children_FamilyBenefits WHERE 1=1"
        params = []

        if country:
            query += " AND country_code = %s"
            params.append(country)
        if year: 
            query += " AND year = %s"
            params.append(year)
        if benefit_type:
            query += " AND benefit_type = %s"
            params.append(benefit_type)
        if target_group:
            query += " AND target_group = %s"
            params.append(target_group)
        if unit_measured:
            query += " AND unit_measured = %s"
            params.append(unit_measured)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        benefits = cursor.fetchall()

        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(benefits)} Benefits Expenditure')
        return jsonify(benefits), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_benefits: {str(e)}')
        return jsonify({"error": str(e)}), 500