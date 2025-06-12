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

apis = Blueprint("apis", __name__)

# Get model 1 routes
@apis.route("/m1weights", methods=["GET"])
def get_model_1_weights():
    try:
        current_app.logger.info("Fetching Model 1 Weights")

        cursor = db.get_db().cursor()
        query = "SELECT * FROM Model1Weights"
        cursor.execute(query)
        weights = cursor.fetchall()
        cursor.close()

        return jsonify(weights), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_model_1_weights: {str(e)}")
        return jsonify({"error": str(e)}), 500