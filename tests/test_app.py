import unittest
import json
from app import create_app, db
from app.models import User, Warehouse, Product, ProductTracking

class TestFarmPortal(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Test user creation and password hashing"""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com', role='farmer')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.username, 'testuser')
            self.assertEqual(retrieved_user.email, 'test@example.com')
            self.assertEqual(retrieved_user.role, 'farmer')
            self.assertTrue(retrieved_user.check_password('testpass123'))
            self.assertFalse(retrieved_user.check_password('wrongpass'))

    def test_warehouse_creation(self):
        """Test warehouse/processing plant creation"""
        with self.app.app_context():
            warehouse = Warehouse(
                name='Test Warehouse',
                type='warehouse',
                location='Test Location',
                capacity=1000.0
            )
            db.session.add(warehouse)
            db.session.commit()

            retrieved = Warehouse.query.filter_by(name='Test Warehouse').first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.type, 'warehouse')
            self.assertEqual(retrieved.capacity, 1000.0)
            self.assertEqual(retrieved.current_stock, 0.0)

    def test_product_creation_and_hash(self):
        """Test product creation with unique hash generation"""
        with self.app.app_context():
            # Create a farmer first
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            db.session.add(farmer)
            db.session.commit()

            # Create product
            product = Product(
                farmer_id=farmer.id,
                product_type='tomato',
                variety='Roma',
                quantity=100.0,
                quality_grade='A'
            )
            product.generate_hash()
            db.session.add(product)
            db.session.commit()

            retrieved = Product.query.filter_by(farmer_id=farmer.id).first()
            self.assertIsNotNone(retrieved)
            self.assertIsNotNone(retrieved.unique_hash)
            self.assertEqual(len(retrieved.unique_hash), 64)  # SHA256 hex length
            self.assertEqual(retrieved.product_type, 'tomato')
            self.assertEqual(retrieved.quantity, 100.0)

    def test_product_tracking(self):
        """Test product tracking through the supply chain"""
        with self.app.app_context():
            # Setup users and warehouse
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            manager = User(username='manager', email='manager@test.com', role='plant_manager')
            manager.set_password('pass')

            warehouse = Warehouse(name='Test Plant', type='processing', location='Test', capacity=1000.0)

            db.session.add_all([farmer, manager, warehouse])
            db.session.commit()

            # Create product
            product = Product(farmer_id=farmer.id, product_type='lettuce', quantity=50.0, quality_grade='A')
            product.generate_hash()
            db.session.add(product)
            db.session.commit()

            # Add tracking
            tracking = ProductTracking(
                product_id=product.id,
                warehouse_id=warehouse.id,
                status='received',
                quantity=50.0,
                quality_notes='Fresh product',
                processed_by=manager.id
            )
            db.session.add(tracking)
            db.session.commit()

            # Verify tracking
            retrieved_tracking = ProductTracking.query.filter_by(product_id=product.id).first()
            self.assertIsNotNone(retrieved_tracking)
            self.assertEqual(retrieved_tracking.status, 'received')
            self.assertEqual(retrieved_tracking.quantity, 50.0)
            self.assertEqual(retrieved_tracking.processor.username, 'manager')

            # Check warehouse stock update
            updated_warehouse = Warehouse.query.get(warehouse.id)
            self.assertEqual(updated_warehouse.current_stock, 50.0)

    def test_user_authentication_flow(self):
        """Test login/logout authentication flow"""
        with self.app.app_context():
            # Create test user
            user = User(username='testuser', email='test@example.com', role='farmer')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()

        # Test login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123',
            'remember': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_farmer_product_management(self):
        """Test farmer's ability to manage their products"""
        with self.app.app_context():
            # Create farmer
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            db.session.add(farmer)
            db.session.commit()

            # Login
            self.client.post('/login', data={
                'username': 'farmer',
                'password': 'pass'
            })

            # Create product
            response = self.client.post('/product/new', data={
                'product_type': 'tomato',
                'variety': 'Cherry',
                'quantity': '100.5',
                'quality_grade': 'A'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Product has been added', response.data)

            # Verify product was created
            with self.app.app_context():
                product = Product.query.filter_by(farmer_id=farmer.id).first()
                self.assertIsNotNone(product)
                self.assertEqual(product.product_type, 'tomato')
                self.assertEqual(product.quantity, 100.5)

    def test_role_based_access_control(self):
        """Test that users can only access appropriate features based on role"""
        with self.app.app_context():
            # Create users with different roles
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')

            plant_mgr = User(username='plant_mgr', email='plant@test.com', role='plant_manager')
            plant_mgr.set_password('pass')

            db.session.add_all([farmer, plant_mgr])
            db.session.commit()

        # Test farmer cannot access warehouse management
        self.client.post('/login', data={'username': 'farmer', 'password': 'pass'})
        response = self.client.get('/warehouses', follow_redirects=True)
        self.assertIn(b'Farmers do not have access', response.data)

        # Test plant manager can access warehouse management
        self.client.get('/logout')  # Logout first
        self.client.post('/login', data={'username': 'plant_mgr', 'password': 'pass'})
        response = self.client.get('/warehouses', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses & Processing Plants', response.data)

    def test_product_status_transitions(self):
        """Test valid product status transitions"""
        with self.app.app_context():
            # Setup
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            manager = User(username='manager', email='manager@test.com', role='plant_manager')
            manager.set_password('pass')
            warehouse = Warehouse(name='Test Plant', type='processing', location='Test', capacity=1000.0)

            db.session.add_all([farmer, manager, warehouse])
            db.session.commit()

            product = Product(farmer_id=farmer.id, product_type='potato', quantity=200.0, quality_grade='A')
            product.generate_hash()
            db.session.add(product)
            db.session.commit()

            # Test status progression
            statuses = ['received', 'processing', 'stored', 'shipped']

            for status in statuses:
                tracking = ProductTracking(
                    product_id=product.id,
                    warehouse_id=warehouse.id,
                    status=status,
                    quantity=200.0,
                    processed_by=manager.id
                )
                db.session.add(tracking)
                db.session.commit()

                latest = ProductTracking.query.filter_by(product_id=product.id).order_by(
                    ProductTracking.transition_date.desc()).first()
                self.assertEqual(latest.status, status)

    def test_warehouse_capacity_management(self):
        """Test warehouse capacity and utilization tracking"""
        with self.app.app_context():
            warehouse = Warehouse(
                name='Test Warehouse',
                type='warehouse',
                location='Test Location',
                capacity=1000.0
            )
            db.session.add(warehouse)
            db.session.commit()

            # Test initial state
            self.assertEqual(warehouse.current_stock, 0.0)
            self.assertEqual(warehouse.capacity, 1000.0)

            # Simulate adding stock
            warehouse.current_stock = 750.0
            db.session.commit()

            # Test utilization calculation
            utilization = (warehouse.current_stock / warehouse.capacity) * 100
            self.assertEqual(utilization, 75.0)

            # Test over-capacity scenario
            warehouse.current_stock = 1200.0
            db.session.commit()
            utilization = (warehouse.current_stock / warehouse.capacity) * 100
            self.assertEqual(utilization, 120.0)

    def test_product_quality_grading(self):
        """Test product quality grade validation and tracking"""
        with self.app.app_context():
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            db.session.add(farmer)
            db.session.commit()

            # Test all quality grades
            grades = ['A', 'B', 'C']
            for grade in grades:
                product = Product(
                    farmer_id=farmer.id,
                    product_type='tomato',
                    quantity=100.0,
                    quality_grade=grade
                )
                product.generate_hash()
                db.session.add(product)
                db.session.commit()

                retrieved = Product.query.filter_by(
                    farmer_id=farmer.id,
                    quality_grade=grade
                ).first()
                self.assertIsNotNone(retrieved)
                self.assertEqual(retrieved.quality_grade, grade)

    def test_unique_hash_collision_prevention(self):
        """Test that unique hashes prevent collisions"""
        with self.app.app_context():
            farmer = User(username='farmer', email='farmer@test.com', role='farmer')
            farmer.set_password('pass')
            db.session.add(farmer)
            db.session.commit()

            # Create two products with same data
            product1 = Product(
                farmer_id=farmer.id,
                product_type='tomato',
                quantity=100.0,
                quality_grade='A'
            )
            product1.generate_hash()

            product2 = Product(
                farmer_id=farmer.id,
                product_type='tomato',
                quantity=100.0,
                quality_grade='A'
            )
            product2.generate_hash()

            db.session.add_all([product1, product2])
            db.session.commit()

            # Hashes should be different due to timestamp
            self.assertNotEqual(product1.unique_hash, product2.unique_hash)

if __name__ == '__main__':
    unittest.main()
