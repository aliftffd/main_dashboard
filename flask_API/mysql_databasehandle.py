from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import firebase_admin
import mysql.connector
# from firebase_admin import credentials, firestore
from random import random
from threading import Lock
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ATP2023!'

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5175"}})

thread = None
thread_lock = Lock()

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread():
    print("Generating random sensor values")

    # MySQL connection
    conn = mysql.connector.connect(
        user='username',
        password='password',
        host='localhost',
        database='database name'
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iot_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            value FLOAT,
            date VARCHAR(255)
        )
    ''')
    conn.commit()

    while True:
        dummy_sensor_value = round(random() * 100, 3)
        date_time = get_current_datetime()
        socketio.emit('sensorData', {'value': dummy_sensor_value, 'date': date_time})

        try:
            # Insert data into MySQL database
            cursor.execute('''
                INSERT INTO iot_data (value, date) VALUES (%s, %s)
            ''', (dummy_sensor_value, date_time))
            conn.commit()
        except Exception as e:
            print(f"Error inserting data into MySQL: {e}")
            conn.rollback()

        socketio.sleep(10)

    # Close the connection when the thread is done (this will not be reached in an infinite loop)
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return "Data endpoint"

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
