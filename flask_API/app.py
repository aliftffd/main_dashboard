from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from random import random
from threading import Lock
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ATP2023!'

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/home/dartvader/main_project/real_project/main_dashboard/flask_API/projecttest-17ae4-firebase-adminsdk-bzp5z-ba840dff8a.json') # input JSON path for firebase database; 
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('sensorData', {'value': dummy_sensor_value, 'date': get_current_datetime()})

        try:
            # Store data in Firebase Firestore
            data = {
                'value': dummy_sensor_value,
                'date': get_current_datetime()
            }
            db.collection('iot_data').add(data)
        except Exception as e:
            print(f"Error inserting data into Firebase: {e}")

        socketio.sleep(10)

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
