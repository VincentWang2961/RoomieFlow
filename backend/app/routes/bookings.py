from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.property import Property, PropertyMember
from app.models.room import Room
from app.models.booking import BookingApplication
from app.models.time_allocation import TimeAllocation
from datetime import datetime, date
from sqlalchemy import and_

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get booking applications for current user."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get filter parameters
    status = request.args.get('status')
    property_id = request.args.get('property_id')
    
    query = BookingApplication.query.filter_by(user_id=current_user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if property_id:
        # Filter by property through room relationship
        query = query.join(Room).filter(Room.property_id == property_id)
    
    bookings = query.order_by(BookingApplication.booking_date.desc()).all()
    
    return jsonify({
        'bookings': [booking.to_dict() for booking in bookings]
    }), 200

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    """Create a new booking application."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    room_id = data.get('room_id')
    booking_date_str = data.get('booking_date')
    session_type = data.get('session_type')
    notes = data.get('notes', '').strip()
    
    if not room_id or not booking_date_str or not session_type:
        return jsonify({'error': 'room_id, booking_date, and session_type are required'}), 400
    
    if session_type not in ['morning', 'midday', 'evening']:
        return jsonify({'error': 'session_type must be morning, midday, or evening'}), 400
    
    # Parse booking date
    try:
        booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Check if booking date is in the future
    if booking_date <= date.today():
        return jsonify({'error': 'Booking date must be in the future'}), 400
    
    # Check if room exists and user has access
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
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
        return jsonify({'error': 'Access denied to this room'}), 403
    
    # Check for existing booking for same room/date/session
    existing_booking = BookingApplication.query.filter(
        and_(
            BookingApplication.room_id == room_id,
            BookingApplication.booking_date == booking_date,
            BookingApplication.session_type == session_type,
            BookingApplication.status.in_(['pending', 'approved'])
        )
    ).first()
    
    if existing_booking:
        return jsonify({'error': 'This time slot is already booked or pending approval'}), 400
    
    # Get duration value from time allocation
    time_allocation = TimeAllocation.query.filter_by(property_id=property_obj.id).first()
    if not time_allocation:
        # Use default values if no time allocation exists
        duration_value = BookingApplication.get_session_duration(session_type)
    else:
        duration_value = time_allocation.get_session_duration(session_type)
    
    # Create booking application
    booking = BookingApplication(
        user_id=current_user_id,
        room_id=room_id,
        booking_date=booking_date,
        session_type=session_type,
        notes=notes,
        duration_value=duration_value
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking application created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create booking application'}), 500

@bookings_bp.route('/<booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get specific booking application by ID."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    booking = BookingApplication.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Check if user has access (booking owner or property admin/owner)
    is_booking_owner = booking.user_id == current_user_id
    property_obj = booking.room.property
    is_property_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_obj.id,
        user_id=current_user_id,
        role='admin',
        invitation_status='accepted'
    ).first() is not None
    
    if not (is_booking_owner or is_property_owner or is_property_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify({'booking': booking.to_dict()}), 200

@bookings_bp.route('/<booking_id>/approve', methods=['PUT'])
@jwt_required()
def approve_booking(booking_id):
    """Approve a booking application."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    booking = BookingApplication.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status != 'pending':
        return jsonify({'error': 'Only pending bookings can be approved'}), 400
    
    # Check if user has admin access to approve
    property_obj = booking.room.property
    is_property_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_obj.id,
        user_id=current_user_id,
        role='admin',
        invitation_status='accepted'
    ).first() is not None
    
    if not (is_property_owner or is_property_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json() or {}
    approval_notes = data.get('approval_notes', '').strip()
    
    # Update booking status
    booking.status = 'approved'
    booking.approved_by = current_user_id
    booking.approval_notes = approval_notes
    booking.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Booking approved successfully',
            'booking': booking.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to approve booking'}), 500

@bookings_bp.route('/<booking_id>/reject', methods=['PUT'])
@jwt_required()
def reject_booking(booking_id):
    """Reject a booking application."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    booking = BookingApplication.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.status != 'pending':
        return jsonify({'error': 'Only pending bookings can be rejected'}), 400
    
    # Check if user has admin access to reject
    property_obj = booking.room.property
    is_property_owner = property_obj.owner_id == current_user_id
    is_property_admin = PropertyMember.query.filter_by(
        property_id=property_obj.id,
        user_id=current_user_id,
        role='admin',
        invitation_status='accepted'
    ).first() is not None
    
    if not (is_property_owner or is_property_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json() or {}
    approval_notes = data.get('approval_notes', '').strip()
    
    # Update booking status
    booking.status = 'rejected'
    booking.approved_by = current_user_id
    booking.approval_notes = approval_notes
    booking.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Booking rejected successfully',
            'booking': booking.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reject booking'}), 500