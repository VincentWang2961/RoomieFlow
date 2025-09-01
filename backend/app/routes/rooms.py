from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.property import Property, PropertyMember
from app.models.room import Room

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/', methods=['GET'])
@jwt_required()
def get_rooms():
    """Get rooms for a specific property."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    property_id = request.args.get('property_id')
    if not property_id:
        return jsonify({'error': 'property_id parameter is required'}), 400
    
    # Check if user has access to this property
    property_obj = Property.query.get(property_id)
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    has_access = (
        property_obj.owner_id == current_user_id or
        PropertyMember.query.filter_by(
            property_id=property_id,
            user_id=current_user_id,
            invitation_status='accepted'
        ).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'Access denied'}), 403
    
    rooms = Room.query.filter_by(property_id=property_id, is_active=True).all()
    
    return jsonify({
        'rooms': [room.to_dict() for room in rooms]
    }), 200

@rooms_bp.route('/', methods=['POST'])
@jwt_required()
def create_room():
    """Create a new room."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    property_id = data.get('property_id')
    name = data.get('name', '').strip()
    capacity = data.get('capacity', 1)
    description = data.get('description', '').strip()
    
    if not property_id:
        return jsonify({'error': 'property_id is required'}), 400
    
    if not name:
        return jsonify({'error': 'Room name is required'}), 400
    
    try:
        capacity = int(capacity)
        if capacity < 1:
            return jsonify({'error': 'Capacity must be at least 1'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid capacity value'}), 400
    
    # Check if user has access to create rooms in this property
    property_obj = Property.query.get(property_id)
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    is_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_id,
        user_id=current_user_id,
        role='admin',
        invitation_status='accepted'
    ).first() is not None
    
    if not (is_owner or is_property_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    # Create room
    room = Room(
        property_id=property_id,
        name=name,
        capacity=capacity,
        description=description
    )
    
    try:
        db.session.add(room)
        db.session.commit()
        
        return jsonify({
            'message': 'Room created successfully',
            'room': room.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create room'}), 500

@rooms_bp.route('/<room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    """Get specific room by ID."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    # Check if user has access to this room's property
    property_obj = room.property
    has_access = (
        property_obj.owner_id == current_user_id or
        PropertyMember.query.filter_by(
            property_id=property_obj.id,
            user_id=current_user_id,
            invitation_status='accepted'
        ).first() is not None
    )
    
    if not has_access:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'room': room.to_dict()}), 200

@rooms_bp.route('/<room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    """Update room information."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    # Check if user has admin access to this room's property
    property_obj = room.property
    is_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_obj.id,
        user_id=current_user_id,
        role='admin',
        invitation_status='accepted'
    ).first() is not None
    
    if not (is_owner or is_property_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update allowed fields
    if 'name' in data:
        name = data['name'].strip()
        if not name:
            return jsonify({'error': 'Room name cannot be empty'}), 400
        room.name = name
    
    if 'description' in data:
        room.description = data['description'].strip()
    
    if 'capacity' in data:
        try:
            capacity = int(data['capacity'])
            if capacity < 1:
                return jsonify({'error': 'Capacity must be at least 1'}), 400
            room.capacity = capacity
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid capacity value'}), 400
    
    if 'is_active' in data:
        room.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Room updated successfully',
            'room': room.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update room'}), 500