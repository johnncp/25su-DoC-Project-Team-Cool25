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

# Create a Blueprint 
daycare = Blueprint("daycare", __name__)


# Get all daycare data with filtering by monthly price and year
@daycare.route("/data", methods=["GET"])
def get_all_daycare_data():
    try:
        current_app.logger.info('Starting get_all_daycare_data request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering
        monthly_price = request.args.get("monthly_price")
        year = request.args.get("year")


        current_app.logger.debug(f'Query parameters - monthly_price: {monthly_price}, year: {year}')

        # Prepare the Base query
        query = "SELECT * FROM DaycareData WHERE 1=1"
        params = []

        # Add filters if provided
        if monthly_price:
            query += " AND monthly_price = %s"
            params.append(monthly_price)
        if year:
            query += " AND year = %s"
            params.append(year)


        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        daycare = cursor.fetchall()
        cursor.close()

               #-----------------------------------------------------------------------------#
        # this beautiful addition is credited to emily moy and her project last year
        # it is necessary because json hates the time data type
        # basically it turns it to a format that json likes 
        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in daycare:

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

        the_response = make_response(jsonify(results))
        the_response.status_code = 200

        # -------------------------------------------------------#


        current_app.logger.info(f'Successfully retrieved {len(daycare)} Daycare Data')
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_all_daycare_data: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# Get all daycare data for a specific daycare with filtering by pretty much everything
@daycare.route("/daycaredata/<int:daycare_id>", methods=["GET"])
def get_daycare_data(daycare_id):
    try:
        current_app.logger.info('Starting get_all_daycare_data request')
        cursor = db.get_db().cursor()

        # Check if Daycare exists
        cursor.execute("SELECT * FROM DaycareLocations WHERE daycare_id = %s", (daycare_id,))
        if not cursor.fetchone():
            return jsonify({"error": "DaycareLocation not found"}), 404

        # Get query parameters for filtering
        monthly_price = request.args.get("monthly_price")
        year = request.args.get("year")
        enrollment = request.args.get("enrollment")
        staff = request.args.get("staff")
        monthly_budget = request.args.get("monthly_budget")
        percent_budget = request.args.get("percent_budget_used")


        current_app.logger.debug(f'Query parameters - monthly_price: {monthly_price}, year: {year}, enrollment: {enrollment}, staff: {staff}, monthly_budget: {monthly_budget}, percent_budget: {percent_budget}')

        # Prepare the Base query
        query = "SELECT * FROM DaycareData WHERE daycare_id = %s"
        params = []
        params.append(daycare_id)

        # Add filters if provided
        if monthly_price:
            query += " AND monthly_price = %s"
            params.append(monthly_price)
        if year:
            query += " AND year = %s"
            params.append(year)
        if enrollment:
            query += " AND enrollment = %s"
            params.append(enrollment)
        if staff:
            query += " AND staff = %s"
            params.append(staff)
        if monthly_budget:
            query += " AND monthly_budget = %s"
            params.append(monthly_budget)
        if percent_budget:
            query += " AND percent_budget_used = %s"
            params.append(percent_budget)


        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        daycare = cursor.fetchall()
        cursor.close()

        #-----------------------------------------------------------------------------#
        # this beautiful addition is credited to emily moy and her project last year
        # it is necessary because json hates the time data type
        # basically it turns it to a format that json likes 
        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in daycare:

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

        the_response = make_response(jsonify(results))
        the_response.status_code = 200

        # -------------------------------------------------------#


        current_app.logger.info(f'Successfully retrieved {len(daycare)} Daycare Data')
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_daycare_data: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
# Get all daycare data for a specific row 
@daycare.route("/data/<int:id>", methods=["GET"])
def get_data(id):
    try:
        current_app.logger.info('Starting get_all_daycare_data request')
        cursor = db.get_db().cursor()

        # Check if Daycare exists
        cursor.execute("SELECT * FROM DaycareData WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "DaycareData not found"}), 404

        # Get query parameters for filtering
        monthly_price = request.args.get("monthly_price")
        year = request.args.get("year")
        enrollment = request.args.get("enrollment")
        staff = request.args.get("staff")
        monthly_budget = request.args.get("monthly_budget")
        percent_budget = request.args.get("percent_budget_used")


        current_app.logger.debug(f'Query parameters - monthly_price: {monthly_price}, year: {year}, enrollment: {enrollment}, staff: {staff}, monthly_budget: {monthly_budget}, percent_budget: {percent_budget}')

        # Prepare the Base query
        query = "SELECT * FROM DaycareData WHERE id = %s"



        cursor.execute(query, (id,))
        daycare = cursor.fetchall()
        cursor.close()

        #-----------------------------------------------------------------------------#
        # this beautiful addition is credited to emily moy and her project last year
        # it is necessary because json hates the time data type
        # basically it turns it to a format that json likes 
        results = []

        # Groups the date and time so that it is in a jsonifiable format
        for row in daycare:

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

        the_response = make_response(jsonify(results))
        the_response.status_code = 200

        # -------------------------------------------------------#


        current_app.logger.info(f'Successfully retrieved {len(daycare)} Daycare Data')
        return the_response
    except Error as e:
        current_app.logger.error(f'Database error in get_data: {str(e)}')
        return jsonify({"error": str(e)}), 500
    
@daycare.route("/data/<int:daycare_id>", methods=["PUT"])
def update_data(daycare_id):
    try: 
        data = request.get_json()

        cursor = db.get_db().cursor()

        # grabbing the selected daycare
        cursor.execute("SELECT * FROM DaycareData WHERE daycare_id = %s", (daycare_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Daycare Data not found"}), 404
        
        update_fields = []
        params = []
        allowed_fields = ["enrollment", "staff", "monthly_budget", "percent_budget_used", "monthly_price", "opening_time", "closing_time"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(daycare_id)
        query = f"UPDATE DaycareData SET {', '.join(update_fields)} WHERE daycare_id = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Daycare Data updated successfully"}), 200

    except Error as e:
        current_app.logger.error(f'Database error in update_data: {str(e)}')
        return jsonify({"error": str(e)}), 500