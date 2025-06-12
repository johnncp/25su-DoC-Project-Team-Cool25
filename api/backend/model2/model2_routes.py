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
import pandas as pd
import numpy as np
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

# This blueprint handles some basic routes that you can use for testing
model2_routes = Blueprint("model2_routes", __name__)

# Features used in the recommendation model
FEATURES = ["weekly_hours", "cash_per_capita", "maternity_per_capita", "services_per_capita"]

# Features used in the recommendation model
FEATURES = ["weekly_hours", "cash_per_capita", "maternity_per_capita", "services_per_capita"]

def normalize_user_input(user_input, max_scale=10):
    """Normalize user input from 0-10 scale to 0-1"""
    return np.array([user_input[feature] / max_scale for feature in FEATURES])

def compute_cosine_similarity(user_vec, country_vec):
    """Compute cosine similarity between user preferences and country features"""
    dot = np.dot(user_vec, country_vec)
    norm_user = np.linalg.norm(user_vec)
    norm_country = np.linalg.norm(country_vec)
    if norm_user == 0 or norm_country == 0:
        return 0
    return dot / (norm_user * norm_country)

def get_latest_country_data():
    """Get the latest available data for each country"""
    query = """
    WITH latest_data AS (
        SELECT 
            country_code,
            Country,
            year,
            CAST(weekly_hours AS FLOAT) as weekly_hours,
            CAST(cash_per_capita AS FLOAT) as cash_per_capita,
            CAST(maternity_per_capita AS FLOAT) as maternity_per_capita,
            CAST(services_per_capita AS FLOAT) as services_per_capita,
            CAST(birth_rate_per_thousand AS FLOAT) as birth_rate_per_thousand,
            CAST(price_index AS FLOAT) as price_index,
            ROW_NUMBER() OVER (
                PARTITION BY country_code 
                ORDER BY 
                    CASE 
                        WHEN weekly_hours IS NOT NULL 
                        AND cash_per_capita IS NOT NULL 
                        AND maternity_per_capita IS NOT NULL 
                        AND services_per_capita IS NOT NULL 
                        THEN 1 
                        ELSE 0 
                    END DESC,
                    year DESC
            ) as rn
        FROM eu_family_employment_data
        WHERE country_code != 'EU27'  -- Exclude EU average
    )
    SELECT 
        country_code,
        Country,
        year,
        weekly_hours,
        cash_per_capita,
        maternity_per_capita,
        services_per_capita,
        birth_rate_per_thousand,
        price_index
    FROM latest_data
    WHERE rn = 1
    AND weekly_hours IS NOT NULL
    AND cash_per_capita IS NOT NULL
    AND maternity_per_capita IS NOT NULL
    AND services_per_capita IS NOT NULL
    """
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    # Get column names
    columns = [desc[0] for desc in cursor.description]
    
    # Fetch all results
    results = cursor.fetchall()
    cursor.close()
    
    # Convert to DataFrame and ensure numeric columns are float
    df = pd.DataFrame(results, columns=columns)
    
    # Convert decimal.Decimal to float for numeric columns
    numeric_columns = ['weekly_hours', 'cash_per_capita', 'maternity_per_capita', 
                      'services_per_capita', 'birth_rate_per_thousand', 'price_index']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(float)
    
    return df

def normalize_country_features(df):
    """Normalize country features to 0-1 scale"""
    df_norm = df.copy()
    
    # Normalize features using min-max normalization
    for feature in FEATURES:
        min_val = df[feature].min()
        max_val = df[feature].max()
        if max_val > min_val:
            df_norm[feature] = (df[feature] - min_val) / (max_val - min_val)
        else:
            df_norm[feature] = 0.5  # If all values are the same
    
    return df_norm

@model2_routes.route('/api/countries/data', methods=['GET'])
def get_countries_data():
    """Get all available countries with their latest data"""
    current_app.logger.info("GET /api/countries/data handler")
    
    try:
        df = get_latest_country_data()
        
        # Convert DataFrame to list of dictionaries
        countries = df.to_dict('records')
        
        response = make_response(jsonify({
            "countries": countries,
            "features": FEATURES,
            "total_countries": len(countries)
        }))
        response.status_code = 200
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error fetching countries data: {str(e)}")
        response = make_response(jsonify({
            "error": "Error fetching countries data",
            "message": str(e)
        }))
        response.status_code = 500
        return response

@model2_routes.route('/api/recommend', methods=['POST'])
def recommend_countries():
    """Recommend EU countries based on user preferences"""
    current_app.logger.info("POST /api/recommend handler")
    
    try:
        # Get user input from request body
        user_input = request.json
        
        # Validate input
        for feature in FEATURES:
            if feature not in user_input:
                return make_response(jsonify({
                    "error": f"Missing required field: {feature}"
                })), 400
            
            # Ensure values are between 0 and 10
            if not (0 <= user_input[feature] <= 10):
                return make_response(jsonify({
                    "error": f"{feature} must be between 0 and 10"
                })), 400
        
        # Get latest country data
        df = get_latest_country_data()
        
        if df.empty:
            return make_response(jsonify({
                "error": "No country data available"
            })), 404
        
        # Normalize country features
        df_norm = normalize_country_features(df)
        
        # Normalize user input
        user_vec = normalize_user_input(user_input)
        
        # Compute similarities
        similarities = []
        for _, row in df_norm.iterrows():
            country_vec = row[FEATURES].values
            similarity = compute_cosine_similarity(user_vec, country_vec)
            similarities.append(similarity)
        
        df['similarity_score'] = similarities
        
        # Sort by similarity (highest first)
        df_sorted = df.sort_values('similarity_score', ascending=False)
        
        # Prepare response
        recommendations = []
        for _, row in df_sorted.iterrows():
            recommendations.append({
                "country_code": row['country_code'],
                "country": row['Country'],
                "similarity_score": round(row['similarity_score'], 4),
                "year": int(row['year']),
                "weekly_hours": float(row['weekly_hours']) if row['weekly_hours'] is not None else None,
                "cash_per_capita": float(row['cash_per_capita']) if row['cash_per_capita'] is not None else None,
                "maternity_per_capita": float(row['maternity_per_capita']) if row['maternity_per_capita'] is not None else None,
                "services_per_capita": float(row['services_per_capita']) if row['services_per_capita'] is not None else None,
                "birth_rate_per_thousand": float(row['birth_rate_per_thousand']) if row['birth_rate_per_thousand'] is not None else None,
                "price_index": float(row['price_index']) if row['price_index'] is not None else None
            })
        
        response = make_response(jsonify({
            "user_preferences": user_input,
            "recommendations": recommendations,
            "total_countries": len(recommendations)
        }))
        response.status_code = 200
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error in recommendation: {str(e)}")
        response = make_response(jsonify({
            "error": "Error processing recommendation request",
            "message": str(e)
        }))
        response.status_code = 500
        return response

@model2_routes.route('/api/countries/<country_code>', methods=['GET'])
def get_country_details(country_code):
    """Get detailed information for a specific country"""
    current_app.logger.info(f"GET /api/countries/{country_code} handler")
    
    try:
        query = """
        SELECT 
            country_code,
            Country,
            year,
            birth_rate_per_thousand,
            price_index,
            cash_per_capita,
            maternity_per_capita,
            services_per_capita,
            weekly_hours
        FROM eu_family_employment_data
        WHERE country_code = %s
        ORDER BY year DESC
        """
        
        cursor = db.get_db().cursor()
        cursor.execute(query, (country_code,))
        
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        cursor.close()
        
        if not results:
            return make_response(jsonify({
                "error": f"Country with code '{country_code}' not found"
            })), 404
        
        # Convert to list of dictionaries
        country_data = []
        for row in results:
            country_data.append(dict(zip(columns, row)))
        
        response = make_response(jsonify({
            "country_code": country_code,
            "country_name": country_data[0]['Country'],
            "data": country_data
        }))
        response.status_code = 200
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error fetching country details: {str(e)}")
        response = make_response(jsonify({
            "error": "Error fetching country details",
            "message": str(e)
        }))
        response.status_code = 500
        return response

@model2_routes.route('/api/features/stats', methods=['GET'])
def get_feature_statistics():
    """Get statistics about the features used in recommendations"""
    current_app.logger.info("GET /api/features/stats handler")
    
    try:
        df = get_latest_country_data()
        
        if df.empty:
            return make_response(jsonify({
                "error": "No country data available"
            })), 404
        
        stats = {}
        for feature in FEATURES:
            stats[feature] = {
                "min": float(df[feature].min()),
                "max": float(df[feature].max()),
                "mean": float(df[feature].mean()),
                "median": float(df[feature].median()),
                "std": float(df[feature].std())
            }
        
        response = make_response(jsonify({
            "features": FEATURES,
            "statistics": stats,
            "data_points": len(df)
        }))
        response.status_code = 200
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error calculating statistics: {str(e)}")
        response = make_response(jsonify({
            "error": "Error calculating statistics",
            "message": str(e)
        }))
        response.status_code = 500
        return response