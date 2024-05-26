from flask_socketio import SocketIO
import firebase_admin
from firebase_admin import firestore

class DataHandler:
    def __init__(self, socketio: SocketIO, db: firestore.Client):
        self.socketio = socketio
        self.db = db

    def save_to_firestore_rfid(self, timestamp, name, tag_id):
        doc_ref = self.db.collection('rfid_tags').document()
        doc_ref.set({
            'timestamp': timestamp,
            'name': name,
            'tag_id': tag_id
        })

    def save_to_firestore_speed(self, timestamp, value):
        doc_ref = self.db.collection('speed_data').document()
        doc_ref.set({
            'timestamp': timestamp,
            'value': value
        })

    def emit_rfid_data(self, timestamp, name, tag_id):
        self.socketio.emit('rfid_data', {'timestamp': timestamp, 'name': name, 'tag_id': tag_id})
        self.save_to_firestore_rfid(timestamp, name, tag_id)

    def emit_speed_data(self, timestamp, value):
        self.socketio.emit('updateSensorData', {'value': value, "date": timestamp})
        self.save_to_firestore_speed(timestamp, value)
