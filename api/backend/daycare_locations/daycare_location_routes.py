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


locations = Blueprint("locations", __name__)

# gets all the locations of daycares for Cara Days business planning page
# right now it has filters but gonna get rid of them once this starts working
@locations.route("/locations", methods=["GET"])
def get_all_locations():
    try:
        current_app.logger.info('Starting get_all_locations request')
        # ask database for a cursor. cursor is object used to ask query against database
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        country = request.args.get("country_code")
        city = request.args.get("city")
        monthly_price = request.args.get("monthly_price")

        current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {city}, founding_year: {monthly_price}')

        # Prepare the Base query
        # how can i construct a query dynamically? 
        # WHERE 1=1 allows you to add on the filters
        ## 1=1 will always be true but primes query for adding on filters
        query = "SELECT * FROM DaycareLocations WHERE 1=1"
        params = []

        # Add filters if provided
        # add additional query arguements onto select statement
        if country:
            query += " AND country_code = %s"
            params.append(country)
        if city:
            query += " AND city = %s"
            params.append(city)
        if monthly_price:
            query += " AND monthly_price = %s"
            params.append(monthly_price)

        # and the query condition would be AND Country = "France"
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        # this is where i ask cursor to give back all rows the query returns
        locations = cursor.fetchall()

        #-----------------------------------------------------------------------------#
        # this beautiful addition is credited to emily moy and her project last year
        # it is necessary because json hates the time data type
        # basically it turns it to a format that json likes 
        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in locations:

            time1 = row['opening_time']
            time2 = row['closing_time']
            #If the time is in a format that isnt jsonifable change the format to the standard time format
            if isinstance(time1, datetime.timedelta):
                jsonifiable_time = (datetime.datetime.min + time1).time()
            else:
                jsonifiable_time = time1
            
            if isinstance(time2, datetime.timedelta):
                jsonifiable_time2 = (datetime.datetime.min + time2).time()
            else:
                jsonifiable_time2 = time2
            
            departure_time = jsonifiable_time
            time_two = jsonifiable_time2

            result = {
                "Daycare ID": row["daycare_id"],
                "Daycare Name": row["daycare_name"],
                "City": row["city"],
                "Country": row["country_code"],
                "Opening Time": departure_time.isoformat(),
                "Closing Time": time_two.isoformat(),
                "Monthly Price": row["monthly_price"]
            }

            results.append(result)

        the_response = make_response(jsonify(results))
        the_response.status_code = 200

        # -------------------------------------------------------#
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(locations)} Locations')
        # taking ngos retreived from cursor and returning it with http code 200
        return the_response

    #nice error message
    except Error as e:
        current_app.logger.error(f'Database error in get_all_locations: {str(e)}')
        return jsonify({"error": str(e)}), 500

#update hours and price of a specific daycare location
@locations.route("/locations/<int:daycare_id>", methods=["PUT"])
def update_location(daycare_id):
    try: 
        data = request.get_json()

        cursor = db.get_db().cursor()

        # grabbing the selected daycare
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Daycare not found"}), 404
        
        update_fields = []
        params = []
        allowed_fields = ["opening_time", "closing_time", "monthly_price"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(daycare_id)
        query = f"UPDATE DaycareLocations SET {', '.join(update_fields)} WHERE daycare_id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Daycare updated successfully"}), 200

    except Error as e:
        current_app.logger.error(f'Database error in update_location: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# add a new daycare location    
@locations.route("/locations", methods=["POST"])
def add_new_location():
    try: 
        data = request.get_json()

        required_fields = ["daycare_id", "daycare_name", "opening_time", "closing_time", "monthly_price", "city", "country_code"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO DaycareLocations (daycare_id, daycare_name, opening_time, closing_time, monthly_price, city, country_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["daycare_id"],
                data["daycare_name"],
                data["opening_time"],
                data["closing_time"],
                data["monthly_price"],
                data["city"],
                data["country_code"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        return (
            jsonify({"message": "Daycare created successfully"}),
            201,
        )

    except Error as e:
        current_app.logger.error(f'Database error in add_new_location: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@locations.route("/locations/<int:daycare_id>", methods=["DELETE"])
def delete_location(daycare_id):
    try:
        cursor = db.get_db().cursor()

        # Fetch daycare details
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        daycare = cursor.fetchone()

        if not daycare:
            return jsonify({"error": "Daycare not found"}), 404

        # Insert into archive table
        archive_query = """
            INSERT INTO DeletedDaycareLocations 
            (daycare_id, daycare_name, opening_time, closing_time, monthly_price, city, country_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        archive_values = (
            daycare["daycare_id"],
            daycare["daycare_name"],
            daycare["opening_time"],
            daycare["closing_time"],
            daycare["monthly_price"],
            daycare["city"],
            daycare["country_code"],
        )

        cursor.execute(archive_query, archive_values)

        # Delete from original table
        cursor.execute("DELETE FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Daycare deleted successfully"}), 200

    except Error as e:
        current_app.logger.error(f'Database error in delete_location: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

@locations.route("/locations/deleted", methods=["GET"])
def get_deleted_locations():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM DeletedDaycareLocations")

        deleted = cursor.fetchall()

        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in deleted:

            time1 = row['opening_time']
            time2 = row['closing_time']
            #If the time is in a format that isnt jsonifable change the format to the standard time format
            if isinstance(time1, datetime.timedelta):
                jsonifiable_time = (datetime.datetime.min + time1).time()
            else:
                jsonifiable_time = time1
            
            if isinstance(time2, datetime.timedelta):
                jsonifiable_time2 = (datetime.datetime.min + time2).time()
            else:
                jsonifiable_time2 = time2
            
            departure_time = jsonifiable_time
            time_two = jsonifiable_time2

            result = {
                "Daycare ID": row["daycare_id"],
                "Daycare Name": row["daycare_name"],
                "City": row["city"],
                "Country": row["country_code"],
                "Opening Time": departure_time.isoformat(),
                "Closing Time": time_two.isoformat(),
                "Monthly Price": row["monthly_price"]
            }

            results.append(result)

        the_response = make_response(jsonify(results))
        the_response.status_code = 200

        cursor.close()

        return the_response
    
    except Error as e:
        current_app.logger.error(f'Error fetching deleted locations: {str(e)}')
        return jsonify({"error": str(e)}), 500