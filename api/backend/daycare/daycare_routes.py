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

location = Blueprint("location", __name__)

@location.route("/locations", methods=["GET"])
def get_all_locations():
    try:
        current_app.logger.info('Starting get_all_locations request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

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
        # %s is a placeholder for a string
        # as we're adding a dondition to query statement, we are adding a value to params list (params.append())
        # 
        if country:
            query += " AND country_code = %s"
            params.append(country)
        if city:
            query += " AND city = %s"
            params.append(city)
        if monthly_price:
            query += " AND monthly_price = %s"
            params.append(monthly_price)


        # cursor.execute takes what's in params list and substitutes it in for %s
        # so like params.append(country) would add France to the params list
        # and the query condition would be AND Country = "France"
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        # this is where i ask cursor to give back all rows the query returns
        locations = cursor.fetchall()

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

        current_app.logger.info(f'Successfully retrieved {len(locations)} Locations')
        # taking ngos retreived from cursor and returning it with http code 200
        return the_response

    #nice error message
    except Error as e:
        current_app.logger.error(f'Database error in get_all_locations: {str(e)}')
        return jsonify({"error": str(e)}), 500

#update hours and price of a specific daycare location
@location.route("/locations/<int:daycare_id>", methods=["PUT"])
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
@location.route("/locations", methods=["POST"])
def add_new_location():
    try: 
        data = request.get_json()

        required_fields = ["daycare_id", "opening_time", "closing_time", "monthly_price", "city", "country_code"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO DaycareLocations (daycare_id, opening_time, closing_time, monthly_price, city, country_code)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["daycare_id"],
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
    
# will delete a daycare location
# ngl, i have no idea how to do this
# insert into a deleted locations table
# then delete from daycare locations table
@location.route("/locations/<int:daycare_id>", methods=["DELETE"])
def delete_location(daycare_id):
    try: 
        data = request.get_json()

        cursor = db.get_db().cursor()

        # grabbing the selected daycare
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Daycare not found"}), 404


    except Error as e:
        current_app.logger.error(f'Database error in delete_location: {str(e)}')
        return jsonify({"error": str(e)}), 500