import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=None):
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = False

    if config_class:
        app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.auth.routes import auth
    from app.warehouse.routes import warehouse
    from app.product.routes import product
    from app.dashboard.routes import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(warehouse)
    app.register_blueprint(product)
    app.register_blueprint(dashboard)

    # Create database tables
    with app.app_context():
        db.create_all()
        # Initialize test data
        init_test_data()

    return app

def init_test_data():
    """Initialize test users and sample data"""
    from app.models import User, Warehouse, Product, ProductTracking
    from datetime import datetime, timedelta
    import hashlib

    # Create test users if they don't exist
    if not User.query.filter_by(username='farmer1').first():
        farmer = User(username='farmer1', email='farmer1@example.com',
                     role='farmer', farm_location='Farm A')
        farmer.set_password('password123')
        db.session.add(farmer)

    if not User.query.filter_by(username='farmer2').first():
        farmer2 = User(username='farmer2', email='farmer2@example.com',
                      role='farmer', farm_location='Farm B')
        farmer2.set_password('password123')
        db.session.add(farmer2)

    if not User.query.filter_by(username='plant_manager').first():
        plant_mgr = User(username='plant_manager', email='plant@example.com',
                        role='plant_manager')
        plant_mgr.set_password('password123')
        db.session.add(plant_mgr)

    if not User.query.filter_by(username='warehouse_manager').first():
        warehouse_mgr = User(username='warehouse_manager', email='warehouse@example.com',
                           role='warehouse_manager')
        warehouse_mgr.set_password('password123')
        db.session.add(warehouse_mgr)

    # Create sample warehouses
    if not Warehouse.query.filter_by(name='Main Processing Plant').first():
        plant = Warehouse(name='Main Processing Plant', type='processing',
                         location='Plant Location A', capacity=1000.0)
        db.session.add(plant)

    if not Warehouse.query.filter_by(name='Central Warehouse').first():
        warehouse = Warehouse(name='Central Warehouse', type='warehouse',
                            location='Warehouse Location B', capacity=5000.0)
        db.session.add(warehouse)

    if not Warehouse.query.filter_by(name='Regional Distribution Center').first():
        dist_center = Warehouse(name='Regional Distribution Center', type='warehouse',
                               location='Distribution Location C', capacity=3000.0)
        db.session.add(dist_center)

    db.session.commit()

    # Create sample products with various statuses
    farmer1 = User.query.filter_by(username='farmer1').first()
    farmer2 = User.query.filter_by(username='farmer2').first()
    plant = Warehouse.query.filter_by(name='Main Processing Plant').first()
    warehouse = Warehouse.query.filter_by(name='Central Warehouse').first()
    dist_center = Warehouse.query.filter_by(name='Regional Distribution Center').first()
    plant_mgr = User.query.filter_by(username='plant_manager').first()
    warehouse_mgr = User.query.filter_by(username='warehouse_manager').first()

    if farmer1 and plant and warehouse:
        # Product 1: Tomatoes - fully tracked through the system
        tomato_hash = hashlib.sha256(f"{farmer1.id}-tomato-500.0-{datetime.utcnow()}".encode()).hexdigest()
        if not Product.query.filter_by(unique_hash=tomato_hash).first():
            product1 = Product(
                farmer_id=farmer1.id,
                product_type='tomato',
                variety='Roma',
                quantity=500.0,
                quality_grade='A'
            )
            product1.generate_hash()
            db.session.add(product1)
            db.session.commit()

            # Add tracking history
            tracking1 = ProductTracking(
                product_id=product1.id,
                warehouse_id=plant.id,
                status='received',
                quantity=500.0,
                quality_notes='Fresh tomatoes, good quality',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(days=5)
            )
            db.session.add(tracking1)

            tracking2 = ProductTracking(
                product_id=product1.id,
                warehouse_id=plant.id,
                status='processing',
                quantity=480.0,
                quality_notes='Washed and sorted',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(days=4)
            )
            db.session.add(tracking2)

            tracking3 = ProductTracking(
                product_id=product1.id,
                warehouse_id=warehouse.id,
                status='stored',
                quantity=460.0,
                quality_notes='Ready for distribution',
                processed_by=warehouse_mgr.id,
                transition_date=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(tracking3)

            # Update warehouse stock
            plant.current_stock += 480.0
            warehouse.current_stock += 460.0

        # Product 2: Potatoes - currently processing
        if not Product.query.filter(Product.farmer_id == farmer1.id, Product.product_type == 'potato').first():
            product2 = Product(
                farmer_id=farmer1.id,
                product_type='potato',
                variety='Russet',
                quantity=800.0,
                quality_grade='B'
            )
            product2.generate_hash()
            db.session.add(product2)
            db.session.commit()

            tracking = ProductTracking(
                product_id=product2.id,
                warehouse_id=plant.id,
                status='processing',
                quantity=800.0,
                quality_notes='Currently being washed and graded',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(hours=6)
            )
            db.session.add(tracking)
            plant.current_stock += 800.0

        # Product 3: Lettuce - just received
        if not Product.query.filter(Product.farmer_id == farmer1.id, Product.product_type == 'lettuce').first():
            product3 = Product(
                farmer_id=farmer1.id,
                product_type='lettuce',
                variety='Romaine',
                quantity=200.0,
                quality_grade='A'
            )
            product3.generate_hash()
            db.session.add(product3)
            db.session.commit()

            tracking = ProductTracking(
                product_id=product3.id,
                warehouse_id=plant.id,
                status='received',
                quantity=200.0,
                quality_notes='Fresh harvest, excellent condition',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(hours=2)
            )
            db.session.add(tracking)
            plant.current_stock += 200.0

    if farmer2 and dist_center:
        # Product 4: Carrots - stored and ready for shipping
        if not Product.query.filter(Product.farmer_id == farmer2.id, Product.product_type == 'carrot').first():
            product4 = Product(
                farmer_id=farmer2.id,
                product_type='carrot',
                variety='Nantes',
                quantity=300.0,
                quality_grade='A'
            )
            product4.generate_hash()
            db.session.add(product4)
            db.session.commit()

            tracking1 = ProductTracking(
                product_id=product4.id,
                warehouse_id=plant.id,
                status='received',
                quantity=300.0,
                quality_notes='Clean carrots, good size distribution',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(days=3)
            )
            db.session.add(tracking1)

            tracking2 = ProductTracking(
                product_id=product4.id,
                warehouse_id=dist_center.id,
                status='stored',
                quantity=290.0,
                quality_notes='Washed, trimmed, and packed',
                processed_by=warehouse_mgr.id,
                transition_date=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add(tracking2)

            plant.current_stock += 300.0
            dist_center.current_stock += 290.0

        # Product 5: Peppers - rejected due to quality
        if not Product.query.filter(Product.farmer_id == farmer2.id, Product.product_type == 'pepper').first():
            product5 = Product(
                farmer_id=farmer2.id,
                product_type='pepper',
                variety='Bell',
                quantity=150.0,
                quality_grade='C'
            )
            product5.generate_hash()
            db.session.add(product5)
            db.session.commit()

            tracking = ProductTracking(
                product_id=product5.id,
                warehouse_id=plant.id,
                status='rejected',
                quantity=150.0,
                quality_notes='Quality below standards - soft spots detected',
                processed_by=plant_mgr.id,
                transition_date=datetime.utcnow() - timedelta(hours=12)
            )
            db.session.add(tracking)

    db.session.commit()
