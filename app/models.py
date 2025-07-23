from extensions import db
from flask_login import UserMixin
from datetime import datetime
import random
import string

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class QueueTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_number = db.Column(db.Integer, nullable=True)
    service_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='waiting')
    temp_id = db.Column(db.String(8), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    called_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Assign queue number
        last = QueueTicket.query.order_by(QueueTicket.queue_number.desc()).first()
        self.queue_number = (last.queue_number + 1) if last else 1

        # Generate temp ID if not passed
        if not self.temp_id:
            self.temp_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
