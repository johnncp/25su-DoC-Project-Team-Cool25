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
        owner_id = request.args.get("owner_id")
        #monthly_price = request.args.get("monthly_price")

        current_app.logger.debug(f'Query parameters - country: {country}, city: {city}, owner: {owner_id}')

        # Prepare the Base query
        # how can i construct a query dynamically? 
        # WHERE 1=1 allows you to add on the filters
        ## 1=1 will always be true but primes query for adding on filters
        query = "SELECT * FROM DaycareLocations WHERE inactive = FALSE"
        params = []

        # Add filters if provided
        # add additional query arguements onto select statement
        if country:
            query += " AND country_code = %s"
            params.append(country)
        if city:
            query += " AND city = %s"
            params.append(city)
        if owner_id:
            query += " AND owner_id = %s"
            params.append(owner_id)

        # and the query condition would be AND Country = "France"
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        # this is where i ask cursor to give back all rows the query returns
        locations = cursor.fetchall()


        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(locations)} Locations')
        # taking ngos retreived from cursor and returning it with http code 200
        return jsonify(locations), 200

    #nice error message
    except Error as e:
        current_app.logger.error(f'Database error in get_all_locations: {str(e)}')
        return jsonify({"error": str(e)}), 500

#update hours and price of a specific daycare location
# i don't think this route is necessary anymore but will keep for reference for now
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
# need to figure out how to make it this user's owner_id!!! (might need to be done on page)
@locations.route("/locations", methods=["POST"])
def add_new_location():
    try: 
        data = request.get_json()

        required_fields = ["daycare_name", "city", "country_code", "owner_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO DaycareLocations (daycare_name, city, country_code, owner_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["daycare_name"],
                data["city"],
                data["country_code"],
                data["owner_id"],
            ),
        )

        db.get_db().commit()
        new_daycare_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "Daycare created successfully", "daycare_id": new_daycare_id}),
            201,
        )

    except Error as e:
        current_app.logger.error(f'Database error in add_new_location: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# deletes daycare by setting it as inactive
@locations.route("/locations/<int:daycare_id>", methods=["DELETE"])
def delete_location(daycare_id):
    try:
        cursor = db.get_db().cursor()

        # Fetch daycare details
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        daycare = cursor.fetchone()

        if not daycare:
            return jsonify({"error": "Daycare not found"}), 404

        
        # Delete from original table
        cursor.execute("UPDATE DaycareLocations SET inactive = true WHERE daycare_id = %s", (daycare_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Daycare deleted successfully"}), 200

    except Error as e:
        current_app.logger.error(f'Database error in delete_location: {str(e)}')
        return jsonify({"error": str(e)}), 500
    

#this is be obsolete but leaving for now just in case
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

# gets all info for a certain location including data in other table
@locations.route("/locations/<int:daycare_id>", methods=["GET"])
def get_location_data(daycare_id):
    try:
        cursor = db.get_db().cursor()

        # Get NGO details
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        loc = cursor.fetchone()

        if not loc:
            return jsonify({"error": "Location not found"}), 404

        # Get associated data
        query = "SELECT * FROM DaycareData WHERE daycare_id = %s"
        params = []
        params.append(daycare_id)
        year = request.args.get("year")
        monthly_price = request.args.get("monthly_price")
        if year:
            query += " AND year = %s"
            params.append(year)
        if monthly_price:
            query += " AND monthly_price = %s"
            params.append(monthly_price)

        cursor.execute(query, params)

        daycare_data = cursor.fetchall()
               #-----------------------------------------------------------------------------#
        # this beautiful addition is credited to emily moy and her project last year
        # it is necessary because json hates the time data type
        # basically it turns it to a format that json likes 
        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in daycare_data:

            time1 = row['opening_time']
            time2 = row['closing_time']
            year1 = row['year']
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
                "ID": row["id"],
                "Daycare ID": row["daycare_id"],
                "Enrollment": row["enrollment"],
                "Year": row["year"],
                "Staff": row["staff"],
                "Monthly Budget": row["monthly_budget"],
                "Percent Budget Used": row["percent_budget_used"],
                "Monthly Price": row["monthly_price"],
                "Opening Time": departure_time.isoformat(),
                "Closing Time": time_two.isoformat()
            }

            results.append(result)

        # Combine data from multiple related queries into one object to return (after jsonify)
        loc["data"] = results

        cursor.close()
        return jsonify(loc), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500