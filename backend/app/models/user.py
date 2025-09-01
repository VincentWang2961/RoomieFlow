from app import db
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    owned_properties = db.relationship('Property', backref='owner', lazy=True, foreign_keys='Property.owner_id')
    property_memberships = db.relationship('PropertyMember', backref='user', lazy=True)
    booking_applications = db.relationship('BookingApplication', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set the user's password."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self, include_sensitive=False):
        """Convert user object to dictionary."""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'email_verified': self.email_verified
        }
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'