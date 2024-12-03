from flask import Flask, request, jsonify, render_template, redirect,url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "localhost",
    "port": "8889",
    "user": "root",
    "password": "root",
    "database": "edutrack"
}

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/students', methods=['GET'])
def get_students():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    connection.close()
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
                   (data["name"], data["email"], data["course"]))
    connection.commit()
    connection.close()
    return jsonify({"message": "Student added successfully!"}), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s",
                   (data["name"], data["email"], data["course"], student_id))
    connection.commit()
    connection.close()
    return jsonify({"message": "Student updated successfully!"})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Student deleted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

