from app import db
import uuid
from datetime import datetime

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    rooms = db.relationship('Room', backref='property', lazy=True, cascade='all, delete-orphan')
    members = db.relationship('PropertyMember', backref='property', lazy=True, cascade='all, delete-orphan')
    time_allocation = db.relationship('TimeAllocation', backref='property', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert property object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'room_count': len(self.rooms)
        }
    
    def __repr__(self):
        return f'<Property {self.name}>'

class PropertyMember(db.Model):
    __tablename__ = 'property_members'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = db.Column(db.String(36), db.ForeignKey('properties.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.Enum('member', 'admin', name='member_roles'), default='member', nullable=False)
    invitation_status = db.Column(db.Enum('pending', 'accepted', 'rejected', name='invitation_status'), 
                                 default='pending', nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint to prevent duplicate memberships
    __table_args__ = (db.UniqueConstraint('property_id', 'user_id'),)
    
    def to_dict(self):
        """Convert property member object to dictionary."""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'user_id': self.user_id,
            'role': self.role,
            'invitation_status': self.invitation_status,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'user': self.user.to_dict() if self.user else None
        }
    
    def __repr__(self):
        return f'<PropertyMember {self.user_id} in {self.property_id}>'