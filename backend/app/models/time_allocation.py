from app import db
import uuid
from datetime import datetime

class TimeAllocation(db.Model):
    __tablename__ = 'time_allocations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = db.Column(db.String(36), db.ForeignKey('properties.id'), nullable=False, unique=True)
    weekly_limit_days = db.Column(db.Float, nullable=False, default=7.0)  # Total days per week
    morning_duration = db.Column(db.Float, nullable=False, default=0.5)   # Morning session duration
    midday_duration = db.Column(db.Float, nullable=False, default=1.0)    # Midday session duration
    evening_duration = db.Column(db.Float, nullable=False, default=1.0)   # Evening session duration
    reset_day_of_week = db.Column(db.Integer, nullable=False, default=1)  # Monday = 1, Sunday = 7
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert time allocation object to dictionary."""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'weekly_limit_days': self.weekly_limit_days,
            'session_durations': {
                'morning': self.morning_duration,
                'midday': self.midday_duration,
                'evening': self.evening_duration
            },
            'reset_day_of_week': self.reset_day_of_week,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_session_duration(self, session_type):
        """Get the duration for a specific session type."""
        duration_map = {
            'morning': self.morning_duration,
            'midday': self.midday_duration,
            'evening': self.evening_duration
        }
        return duration_map.get(session_type, 0.0)
    
    def __repr__(self):
        return f'<TimeAllocation {self.property_id} - {self.weekly_limit_days} days/week>'