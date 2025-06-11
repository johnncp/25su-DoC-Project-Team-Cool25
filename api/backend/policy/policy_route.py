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

policy = Blueprint("policy", __name__)

# gets all policies and can filter by country, focus area, and year
@policy.route("/policy", methods=["GET"])
def get_all_policy():
    try:
        current_app.logger.info('Starting get_all_policy request')
        cursor = db.get_db().cursor()

        country = request.args.get("country_code")
        focus_area = request.args.get("focus_area")
        year = request.args.get("year")

        current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {focus_area}, founding_year: {year}')

        query = "SELECT * FROM Policies WHERE 1=1"
        params = []

        if country:
            query += " AND country_code = %s"
            params.append(country)
        if focus_area:
            query += " AND city = %s"
            params.append(focus_area)
        if year:
            query += " AND monthly_price = %s"
            params.append(year)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        policy = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(policy)} NGOs')
        return jsonify(policy), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_policy: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# adds a law
@policy.route("/policy", methods=["POST"])
def add_new_policy():
    try: 
        data = request.get_json()

        required_fields = ["policy_id", "policy_name", "focus_area", "country_code", "year", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO Policies (policy_id, policy_name, focus_area, country_code, year, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["policy_id"],
                data["policy_name"],
                data["focus_area"],
                data["country_code"],
                data["year"],
                data["description"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        return (
            jsonify({"message": "Policy created successfully"}),
            201,
        )

    except Error as e:
        current_app.logger.error(f'Database error in add_new_policy: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

# can get multiple countries? this route is literally so convoluted just so it can use the multiselect feature 
@policy.route("/allpolicy", methods=["GET"])
def get_all_policies():
    try:
        current_app.logger.info('Starting get_all_policies request')
        cursor = db.get_db().cursor()

        country_codes = request.args.get("country_code")  # Could be comma-separated string
        focus_area = request.args.get("focus_area")
        year = request.args.get("year")

        EU_COUNTRIES = [
            'BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY',
            'LV', 'LT', 'LU', 'HU', 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'FI', 'SE'
        ]

        current_app.logger.debug(f'Query parameters - country: {country_codes}, focus_area: {focus_area}, year: {year}')

        query = "SELECT * FROM Policies WHERE 1=1"
        params = []

        if country_codes:
            if country_codes == "EU27_2020" or country_codes == "European Union (27)":
                countries_list = EU_COUNTRIES
            else: 
                countries_list = country_codes.split(",")
            placeholders = ", ".join(["%s"] * len(countries_list))
            query += f" AND country_code IN ({placeholders})"
            params.extend(countries_list)

        if focus_area:
            query += " AND focus_area = %s"
            params.append(focus_area)

        if year:
            query += " AND year = %s"
            params.append(year)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        policies = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(policies)} policies')
        return jsonify(policies), 200

    except Error as e:
        current_app.logger.error(f'Database error in get_all_policies: {str(e)}')
        return jsonify({"error": str(e)}), 500