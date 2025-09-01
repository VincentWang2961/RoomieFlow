#!/usr/bin/env python3
"""
Simple database initialization for local development
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Set environment for SQLite (local development)
os.environ['DATABASE_URL'] = 'sqlite:///roomieflow.db'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roomieflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models inline to avoid import issues
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class PropertyMember(db.Model):
    __tablename__ = 'property_members'
    
    id = db.Column(db.String(36), primary_key=True)
    property_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    role = db.Column(db.String(10), default='member', nullable=False)
    invitation_status = db.Column(db.String(10), default='pending', nullable=False)
    joined_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.String(36), primary_key=True)
    property_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class BookingApplication(db.Model):
    __tablename__ = 'booking_applications'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    room_id = db.Column(db.String(36), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    session_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), default='pending', nullable=False)
    notes = db.Column(db.Text)
    duration_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    approved_by = db.Column(db.String(36))
    approval_notes = db.Column(db.Text)

class TimeAllocation(db.Model):
    __tablename__ = 'time_allocations'
    
    id = db.Column(db.String(36), primary_key=True)
    property_id = db.Column(db.String(36), nullable=False, unique=True)
    weekly_limit_days = db.Column(db.Float, nullable=False, default=7.0)
    morning_duration = db.Column(db.Float, nullable=False, default=0.5)
    midday_duration = db.Column(db.Float, nullable=False, default=1.0)
    evening_duration = db.Column(db.Float, nullable=False, default=1.0)
    reset_day_of_week = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create admin user if it doesn't exist
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            import uuid
            admin_id = str(uuid.uuid4())
            
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), salt).decode('utf-8')
            
            admin_user = User(
                id=admin_id,
                username='admin',
                email='admin@roomieflow.com',
                password_hash=password_hash,
                role='admin',
                email_verified=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_db()