#!/usr/bin/env python3
"""
Database initialization script for RoomieFlow
This script creates the database tables and sets up the initial schema
"""

import app as app_module
from app_package.models.user import User
from app_package.models.property import Property, PropertyMember
from app_package.models.room import Room
from app_package.models.booking import BookingApplication
from app_package.models.time_allocation import TimeAllocation

def init_db():
    """Initialize the database with tables."""
    app = app_module.create_app()
    db = app_module.db
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Optionally create a default admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@roomieflow.com',
                role='admin'
            )
            admin_user.set_password('admin123')  # Change in production
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("Default admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_db()