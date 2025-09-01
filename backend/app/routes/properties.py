from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.property import Property, PropertyMember
from app.models.time_allocation import TimeAllocation

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/', methods=['GET'])
@jwt_required()
def get_properties():
    """Get properties for current user."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get properties owned by user or where user is a member
    owned_properties = Property.query.filter_by(owner_id=current_user_id, is_active=True).all()
    member_properties = db.session.query(Property).join(PropertyMember).filter(
        PropertyMember.user_id == current_user_id,
        PropertyMember.invitation_status == 'accepted',
        Property.is_active == True
    ).all()
    
    all_properties = owned_properties + [prop for prop in member_properties if prop not in owned_properties]
    
    return jsonify({
        'properties': [prop.to_dict() for prop in all_properties]
    }), 200

@properties_bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    """Create a new property."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'error': 'Property name is required'}), 400
    
    # Create property
    property_obj = Property(
        name=name,
        description=description,
        owner_id=current_user_id
    )
    
    try:
        db.session.add(property_obj)
        db.session.flush()  # Get the property ID
        
        # Create default time allocation
        time_allocation = TimeAllocation(
            property_id=property_obj.id,
            weekly_limit_days=7.0,
            morning_duration=0.5,
            midday_duration=1.0,
            evening_duration=1.0,
            reset_day_of_week=1  # Monday
        )
        db.session.add(time_allocation)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Property created successfully',
            'property': property_obj.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create property'}), 500

@properties_bp.route('/<property_id>', methods=['GET'])
@jwt_required()
def get_property(property_id):
    """Get specific property by ID."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    property_obj = Property.query.get(property_id)
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    # Check if user has access to this property
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
    
    return jsonify({'property': property_obj.to_dict()}), 200

@properties_bp.route('/<property_id>', methods=['PUT'])
@jwt_required()
def update_property(property_id):
    """Update property information."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    property_obj = Property.query.get(property_id)
    if not property_obj:
        return jsonify({'error': 'Property not found'}), 404
    
    # Check if user is the owner or has admin role in the property
    is_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_id,
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
            return jsonify({'error': 'Property name cannot be empty'}), 400
        property_obj.name = name
    
    if 'description' in data:
        property_obj.description = data['description'].strip()
    
    # Only owners can change active status
    if 'is_active' in data and is_owner:
        property_obj.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Property updated successfully',
            'property': property_obj.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update property'}), 500