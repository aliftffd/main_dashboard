from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from rfid_reader import RFIDReader
from speed_reader import SpeedDetect
from data_handler import DataHandler
from threading import Lock

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ATP2023!'

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/home/dartvader/main_project/real_project/main_dashboard/flask_API/projecttest-17ae4-firebase-adminsdk-bzp5z-ba840dff8a.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5175"}})

thread = None
thread_lock = Lock()

# Initialize DataHandler
data_handler = DataHandler(socketio, db)

# Initialize RFID reader
rfid_reader = RFIDReader("", 115200, data_handler.emit_rfid_data)

# Initialize SpeedDetect reader
speed_detect = SpeedDetect("", 9600, data_handler.emit_speed_data)

@app.route('/')
def index():
    return "Data endpoint"

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(rfid_reader.start)
            socketio.start_background_task(speed_detect.start)

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    try:
        socketio.run(app, host='localhost', port=5001)
    except KeyboardInterrupt:
        rfid_reader.stop()
        speed_detect.stop()
