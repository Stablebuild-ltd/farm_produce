import hashlib
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # farmer, plant_manager, warehouse_manager
    farm_location = db.Column(db.String(100))  # Only for farmers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship('Product', backref='farmer', lazy=True)

    def set_password(self, password):
        from app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # processing or warehouse
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Float, nullable=False)  # in tons
    current_stock = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product_trackings = db.relationship('ProductTracking', backref='warehouse', lazy=True)

    def __repr__(self):
        return f"Warehouse('{self.name}', '{self.type}', '{self.location}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_hash = db.Column(db.String(64), unique=True, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)  # tomato, potato, etc.
    variety = db.Column(db.String(50))
    quantity = db.Column(db.Float, nullable=False)  # in kg
    quality_grade = db.Column(db.String(20), default='A')  # A, B, C
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    trackings = db.relationship('ProductTracking', backref='product', lazy=True, cascade='all, delete-orphan')

    def generate_hash(self):
        """Generate unique hash based on farmer, type, quantity, and timestamp"""
        hash_input = f"{self.farmer_id}-{self.product_type}-{self.quantity}-{self.created_at}"
        self.unique_hash = hashlib.sha256(hash_input.encode()).hexdigest()

    def __repr__(self):
        return f"Product('{self.unique_hash}', '{self.product_type}', {self.quantity}kg)"

class ProductTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # received, processing, stored, shipped, rejected
    quantity = db.Column(db.Float, nullable=False)
    quality_notes = db.Column(db.Text)
    transition_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    processor = db.relationship('User', backref='processed_trackings', lazy=True)

    def __repr__(self):
        return f"ProductTracking('{self.status}', {self.quantity}kg, '{self.transition_date}')"
