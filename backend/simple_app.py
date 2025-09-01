#!/usr/bin/env python3
"""
Simplified RoomieFlow API server for testing
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import bcrypt
import uuid
from datetime import timedelta, datetime
import os

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roomieflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'dev-secret-key-for-testing'

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Simple User model for testing
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'email_verified': self.email_verified
        }

# Routes
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'message': 'RoomieFlow API is running'}

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username_or_email or not password:
        return jsonify({'error': 'Username/email and password are required'}), 400
    
    # Find user by username or email
    user = None
    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email.lower()).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(days=7)
    )
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Check for existing users
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        role='user'
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=7)
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

# Add booking models for the chart feature
class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.String(36), primary_key=True)
    property_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BookingApplication(db.Model):
    __tablename__ = 'booking_applications'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    room_id = db.Column(db.String(36), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    session_type = db.Column(db.String(10), nullable=False)  # morning, midday, evening
    status = db.Column(db.String(10), default='pending', nullable=False)  # pending, approved, rejected
    notes = db.Column(db.Text)
    duration_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.String(36))
    approval_notes = db.Column(db.Text)

@app.route('/api/bookings/weekly', methods=['GET'])
@jwt_required()
def get_weekly_bookings():
    """Get weekly booking data for the visual chart"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get week start date (default to current week Monday)
    from datetime import date, timedelta
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday of current week
    
    week_start_param = request.args.get('week_start')
    if week_start_param:
        try:
            week_start = datetime.strptime(week_start_param, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Generate 7 days from Monday to Sunday
    week_days = []
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        week_days.append({
            'date': current_date.isoformat(),
            'day_name': current_date.strftime('%A'),
            'day_short': current_date.strftime('%a'),
            'is_today': current_date == today
        })
    
    # Get all bookings for this week
    week_end = week_start + timedelta(days=6)
    bookings = db.session.query(BookingApplication).filter(
        BookingApplication.booking_date >= week_start,
        BookingApplication.booking_date <= week_end
    ).all()
    
    # Organize bookings by date and session
    booking_data = {}
    for booking in bookings:
        date_str = booking.booking_date.isoformat()
        if date_str not in booking_data:
            booking_data[date_str] = {
                'morning': [],
                'midday': [],
                'evening': []
            }
        
        # Get user and room info
        booking_user = User.query.get(booking.user_id)
        room = Room.query.get(booking.room_id)
        property_obj = Property.query.get(room.property_id) if room else None
        
        booking_info = {
            'id': booking.id,
            'user': booking_user.username if booking_user else 'Unknown',
            'user_id': booking.user_id,
            'room_name': room.name if room else 'Unknown Room',
            'room_id': booking.room_id,
            'property_name': property_obj.name if property_obj else 'Unknown Property',
            'status': booking.status,
            'notes': booking.notes,
            'duration': booking.duration_value,
            'created_at': booking.created_at.isoformat() if booking.created_at else None,
            'can_modify': booking.user_id == current_user_id or user.role == 'admin'
        }
        
        booking_data[date_str][booking.session_type].append(booking_info)
    
    return jsonify({
        'week_start': week_start.isoformat(),
        'week_days': week_days,
        'bookings': booking_data,
        'session_types': ['morning', 'midday', 'evening'],
        'session_labels': {
            'morning': 'Morning',
            'midday': 'Midday', 
            'evening': 'Evening'
        }
    }), 200

@app.route('/api/properties', methods=['GET'])
@jwt_required()
def get_properties():
    """Get properties for current user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get properties where user is owner or member
    if user.role == 'admin':
        properties = Property.query.filter_by(is_active=True).all()
    else:
        # For regular users, get properties they own or are members of
        owned_properties = Property.query.filter_by(owner_id=current_user_id, is_active=True).all()
        # TODO: Add member properties when PropertyMember model is implemented
        properties = owned_properties
    
    property_data = []
    for prop in properties:
        # Get room count for each property
        room_count = Room.query.filter_by(property_id=prop.id, is_active=True).count()
        
        property_data.append({
            'id': prop.id,
            'name': prop.name,
            'description': prop.description,
            'owner_id': prop.owner_id,
            'room_count': room_count,
            'created_at': prop.created_at.isoformat() if prop.created_at else None,
            'is_owner': prop.owner_id == current_user_id
        })
    
    return jsonify({
        'properties': property_data
    }), 200

@app.route('/api/properties', methods=['POST'])
@jwt_required()
def create_property():
    """Create a new property"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'error': 'Property name is required'}), 400
    
    # Check for duplicate property name for this user
    existing_property = Property.query.filter_by(
        owner_id=current_user_id,
        name=name,
        is_active=True
    ).first()
    
    if existing_property:
        return jsonify({'error': 'Property with this name already exists'}), 400
    
    try:
        property_obj = Property(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            owner_id=current_user_id
        )
        
        db.session.add(property_obj)
        db.session.commit()
        
        return jsonify({
            'message': 'Property created successfully',
            'property': {
                'id': property_obj.id,
                'name': property_obj.name,
                'description': property_obj.description,
                'owner_id': property_obj.owner_id,
                'room_count': 0,
                'created_at': property_obj.created_at.isoformat(),
                'is_owner': True
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create property'}), 500

@app.route('/api/properties/<property_id>', methods=['GET'])
@jwt_required()
def get_property_details(property_id):
    """Get detailed property information"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    property_obj = Property.query.filter_by(id=property_id, is_active=True).first()
    
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    # Check if user has access to this property
    if user.role != 'admin' and property_obj.owner_id != current_user_id:
        # TODO: Check PropertyMember access when implemented
        return jsonify({'error': 'Access denied'}), 403
    
    # Get rooms for this property
    rooms = Room.query.filter_by(property_id=property_id, is_active=True).all()
    room_data = []
    for room in rooms:
        room_data.append({
            'id': room.id,
            'name': room.name,
            'capacity': room.capacity,
            'description': room.description,
            'created_at': room.created_at.isoformat() if room.created_at else None
        })
    
    # Get owner information
    owner = User.query.get(property_obj.owner_id)
    
    return jsonify({
        'property': {
            'id': property_obj.id,
            'name': property_obj.name,
            'description': property_obj.description,
            'owner_id': property_obj.owner_id,
            'owner_username': owner.username if owner else 'Unknown',
            'created_at': property_obj.created_at.isoformat() if property_obj.created_at else None,
            'is_owner': property_obj.owner_id == current_user_id,
            'rooms': room_data
        }
    }), 200

@app.route('/api/properties/<property_id>', methods=['PUT'])
@jwt_required()
def update_property(property_id):
    """Update property information"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    property_obj = Property.query.filter_by(id=property_id, is_active=True).first()
    
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    # Check if user has permission to update
    if user.role != 'admin' and property_obj.owner_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'error': 'Property name is required'}), 400
    
    # Check for duplicate name (excluding current property)
    existing_property = Property.query.filter(
        Property.id != property_id,
        Property.owner_id == property_obj.owner_id,
        Property.name == name,
        Property.is_active == True
    ).first()
    
    if existing_property:
        return jsonify({'error': 'Property with this name already exists'}), 400
    
    try:
        property_obj.name = name
        property_obj.description = description
        
        db.session.commit()
        
        room_count = Room.query.filter_by(property_id=property_id, is_active=True).count()
        
        return jsonify({
            'message': 'Property updated successfully',
            'property': {
                'id': property_obj.id,
                'name': property_obj.name,
                'description': property_obj.description,
                'owner_id': property_obj.owner_id,
                'room_count': room_count,
                'created_at': property_obj.created_at.isoformat() if property_obj.created_at else None,
                'is_owner': property_obj.owner_id == current_user_id
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update property'}), 500

@app.route('/api/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    """Get rooms for a property"""
    property_id = request.args.get('property_id')
    if property_id:
        rooms = Room.query.filter_by(property_id=property_id, is_active=True).all()
    else:
        rooms = Room.query.filter_by(is_active=True).all()
    
    return jsonify({
        'rooms': [{'id': r.id, 'name': r.name, 'property_id': r.property_id} for r in rooms]
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created!")
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                id=str(uuid.uuid4()),
                username='admin',
                email='admin@roomieflow.com',
                role='admin',
                email_verified=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created (username: admin, password: admin123)")
        
        # Create sample data for testing the booking chart
        from datetime import date, timedelta
        
        # Create sample property if it doesn't exist
        sample_property = Property.query.first()
        if not sample_property:
            sample_property = Property(
                id=str(uuid.uuid4()),
                name='Sample House',
                description='A sample property for testing',
                owner_id=admin_user.id
            )
            db.session.add(sample_property)
            db.session.flush()
            
            # Create sample rooms
            room1 = Room(
                id=str(uuid.uuid4()),
                property_id=sample_property.id,
                name='Living Room',
                capacity=4,
                description='Main living area'
            )
            room2 = Room(
                id=str(uuid.uuid4()),
                property_id=sample_property.id,
                name='Kitchen',
                capacity=2,
                description='Kitchen and dining area'
            )
            db.session.add(room1)
            db.session.add(room2)
            db.session.flush()
            
            # Create sample bookings for this week
            today = date.today()
            week_start = today - timedelta(days=today.weekday())  # Monday
            
            # Add some sample bookings
            sample_bookings = [
                # Monday
                {
                    'date': week_start,
                    'session': 'morning',
                    'room_id': room1.id,
                    'status': 'approved',
                    'notes': 'Morning yoga session'
                },
                {
                    'date': week_start,
                    'session': 'evening',
                    'room_id': room2.id,
                    'status': 'pending',
                    'notes': 'Dinner preparation'
                },
                # Tuesday
                {
                    'date': week_start + timedelta(days=1),
                    'session': 'midday',
                    'room_id': room1.id,
                    'status': 'approved',
                    'notes': 'Team meeting'
                },
                # Wednesday
                {
                    'date': week_start + timedelta(days=2),
                    'session': 'morning',
                    'room_id': room2.id,
                    'status': 'rejected',
                    'notes': 'Early breakfast'
                },
                {
                    'date': week_start + timedelta(days=2),
                    'session': 'evening',
                    'room_id': room1.id,
                    'status': 'approved',
                    'notes': 'Movie night'
                },
                # Friday
                {
                    'date': week_start + timedelta(days=4),
                    'session': 'midday',
                    'room_id': room2.id,
                    'status': 'pending',
                    'notes': 'Lunch party'
                },
                # Sunday
                {
                    'date': week_start + timedelta(days=6),
                    'session': 'morning',
                    'room_id': room1.id,
                    'status': 'approved',
                    'notes': 'Sunday cleanup'
                }
            ]
            
            for booking_data in sample_bookings:
                duration_map = {'morning': 0.5, 'midday': 1.0, 'evening': 1.0}
                booking = BookingApplication(
                    id=str(uuid.uuid4()),
                    user_id=admin_user.id,
                    room_id=booking_data['room_id'],
                    booking_date=booking_data['date'],
                    session_type=booking_data['session'],
                    status=booking_data['status'],
                    notes=booking_data['notes'],
                    duration_value=duration_map[booking_data['session']]
                )
                db.session.add(booking)
            
            db.session.commit()
            print("Sample property, rooms, and bookings created!")
    
    print("Starting server on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)