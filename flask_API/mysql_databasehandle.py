from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import firebase_admin
import mysql.connector
# from firebase_admin import credentials, firestore (optional code for firebase handling) 
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
    print("Reading sensor values and calculating distance")

    # MySQL connection
    conn = mysql.connector.connect(
        user='',
        password='',
        host='',
        database=''
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iot_data3 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            speed FLOAT,
            distance FLOAT,
            date VARCHAR(255)
        )
    ''')
    conn.commit()

    previous_time = datetime.now()
    total_distance = 0.0

    while True:
        current_time = datetime.now()
        time_interval = (current_time - previous_time).total_seconds()
        previous_time = current_time

        # Replace this with actual sensor reading logic
        speed = round(random() * 100, 3)

        distance = speed * time_interval
        total_distance += distance
        date_time = current_time.strftime("%m/%d/%Y %H:%M:%S")

        data = {'speed': speed, 'distance': total_distance, 'date': date_time}
        socketio.emit('sensorData', data)

        try:
            # Insert data into MySQL database
            cursor.execute('''
                INSERT INTO iot_data3 (speed, distance, date) VALUES (%s, %s, %s)
            ''', (speed, total_distance, date_time))
            conn.commit()
        except Exception as e:
            print(f"Error inserting data into MySQL: {e}")
            conn.rollback()

        socketio.sleep(10)

    # Close the connection when the thread is done (this will not be reached in an infinite loop)
    cursor.close()
    conn.close()

def read_speed_from_sensor():
    # Dummy implementation, replace with actual sensor reading code
    return round(random() * 100, 3)


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