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
from datetime import datetime
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import model01

# This blueprint handles some basic routes that you can use for testing
notes = Blueprint("notes", __name__)

# -----------------------------------------
# GET /notes/<user_id> — Get a user's note
# -----------------------------------------
@notes.route("/notes/<int:user_id>", methods=["GET"])
def get_note_by_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT note_id, user_id, note_content, 
                   note_date_created, note_date_last_updated
            FROM Notes
            WHERE user_id = %s
            LIMIT 1;
        """, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"message": "No note found for this user."}), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching note: {e}")
        return jsonify({"error": "Failed to retrieve note."}), 500

# -----------------------------------------
# POST /notes — Create or update a note
# -----------------------------------------
@notes.route("/notes", methods=["POST"])
def create_or_update_note():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("note_content")

        if not user_id or content is None:
            return jsonify({"error": "Missing user_id or note_content."}), 400

        now = datetime.now()
        conn = db.get_db()
        cursor = conn.cursor()

        # Check if a note already exists
        cursor.execute("SELECT note_id FROM Notes WHERE user_id = %s LIMIT 1;", (user_id,))
        existing = cursor.fetchone()

        if existing:
            # Update existing note
            cursor.execute("""
                UPDATE Notes
                SET note_content = %s,
                    note_date_last_updated = %s
                WHERE user_id = %s;
            """, (content, now, user_id))
        else:
            # Insert new note
            cursor.execute("""
                INSERT INTO Notes (user_id, note_content, note_date_created, note_date_last_updated)
                VALUES (%s, %s, %s, %s);
            """, (user_id, content, now, now))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Note saved successfully."}), 200

    except Exception as e:
        current_app.logger.error(f"Error saving note: {e}")
        return jsonify({"error": "Failed to save note."}), 500

# -----------------------------------------
# DELETE /notes/<user_id> — Remove user's note
# -----------------------------------------
@notes.route("/notes/<int:user_id>", methods=["DELETE"])
def delete_note(user_id):
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notes WHERE user_id = %s;", (user_id,))
        conn.commit()
        cursor.close()
        return jsonify({"message": f"Note for user {user_id} deleted."}), 200

    except Exception as e:
        current_app.logger.error(f"Error deleting note: {e}")
        return jsonify({"error": "Failed to delete note."}), 500