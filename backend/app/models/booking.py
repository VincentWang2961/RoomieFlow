from app import db
import uuid
from datetime import datetime

class BookingApplication(db.Model):
    __tablename__ = 'booking_applications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    session_type = db.Column(db.Enum('morning', 'midday', 'evening', name='session_types'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='booking_status'), 
                      default='pending', nullable=False)
    notes = db.Column(db.Text)
    duration_value = db.Column(db.Float, nullable=False)  # 0.5 for morning, 1.0 for midday/evening
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    approval_notes = db.Column(db.Text)
    
    # Relationships
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_bookings')
    
    # Unique constraint to prevent duplicate bookings for same room/date/session
    __table_args__ = (db.UniqueConstraint('room_id', 'booking_date', 'session_type'),)
    
    def to_dict(self):
        """Convert booking application object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'session_type': self.session_type,
            'status': self.status,
            'notes': self.notes,
            'duration_value': self.duration_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'approved_by': self.approved_by,
            'approval_notes': self.approval_notes,
            'user': self.user.to_dict() if self.user else None,
            'room': self.room.to_dict() if self.room else None
        }
    
    @staticmethod
    def get_session_duration(session_type):
        """Get the duration value for a session type."""
        duration_map = {
            'morning': 0.5,
            'midday': 1.0,
            'evening': 1.0
        }
        return duration_map.get(session_type, 0.0)
    
    def __repr__(self):
        return f'<BookingApplication {self.user_id} - {self.room_id} - {self.booking_date} - {self.session_type}>'