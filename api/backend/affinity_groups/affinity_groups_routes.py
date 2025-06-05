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

group = Blueprint("group", __name__)

# get affinity group that can be filtered by focus area, country, and resource type
@group.route("/groups", methods=["GET"])
def get_all_groups():
    try: 
        current_app.logger.info('Starting get_all_groups request')
        cursor = db.get_db().cursor()

        country = request.args.get("country_code")
        focus_area = request.args.get("focus_area")
        resource_type = request.args.get("resource_type")

        current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {focus_area}, resource_type: {resource_type}')

        query = "SELECT * FROM AffinityResources WHERE 1=1"
        params = []

        if country:
            query += " AND country_code = %s"
            params.append(country)
        if focus_area:
            query += " AND city = %s"
            params.append(focus_area)
        if resource_type:
            query += " AND monthly_price = %s"
            params.append(resource_type)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)

        groups = cursor.fetchall()

        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(groups)} NGOs')
        return jsonify(groups), 200


    except Error as e:
        current_app.logger.error(f'Database error in get_all_groups: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
#adds a new group
@group.route("/groups", methods=["POST"])
def add_new_group():
    try: 
        data = request.get_json()

        required_fields = ["id", "resource_name", "resource_type", "focus_area", "country_code"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO AffinityResources (id, resource_name, resource_type, focus_area, country_code)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["id"],
                data["resource_name"],
                data["resource_type"],
                data["focus_area"],
                data["country_code"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        return (
            jsonify({"message": "Resource created successfully"}),
            201,
        )

    except Error as e:
        current_app.logger.error(f'Database error in add_new_group: {str(e)}')
        return jsonify({"error": str(e)}), 500