from database_config import get_db_connection
from flask import Flask, request, jsonify
from database_config import get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Empower Women API!"

# Fetch all users
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 400

# Fetch sponsorships
@app.route("/sponsorships", methods=["GET"])
def get_sponsorships():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sponsorship_id, title, description, link, created_at FROM sponsorships")
    sponsorships = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(sponsorships)

# Create sponsorship
@app.route("/sponsorships", methods=["POST"])
def create_sponsorship():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    link = data.get("link")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sponsorships (title, description, link) VALUES (%s, %s, %s)",
            (title, description, link),
        )
        conn.commit()
        sponsorship_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Sponsorship created successfully", "sponsorship_id": sponsorship_id}), 201
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 400

# Delete a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
