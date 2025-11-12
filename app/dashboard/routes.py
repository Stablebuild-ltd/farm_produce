from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.models import Product, ProductTracking, Warehouse

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    if current_user.role == 'farmer':
        return farmer_dashboard()
    elif current_user.role == 'plant_manager':
        return plant_manager_dashboard()
    elif current_user.role == 'warehouse_manager':
        return warehouse_manager_dashboard()
    else:
        return render_template('dashboard/admin.html')

def farmer_dashboard():
    """Farmer's dashboard - shows their products and tracking"""
    products = Product.query.filter_by(farmer_id=current_user.id).all()
    recent_trackings = ProductTracking.query.join(Product).filter(
        Product.farmer_id == current_user.id
    ).order_by(ProductTracking.transition_date.desc()).limit(10).all()

    return render_template('dashboard/farmer.html',
                         products=products,
                         recent_trackings=recent_trackings)

def plant_manager_dashboard():
    """Plant manager's dashboard - shows processing operations"""
    warehouses = Warehouse.query.filter_by(type='processing').all()
    processing_products = ProductTracking.query.join(Warehouse).filter(
        Warehouse.type == 'processing'
    ).order_by(ProductTracking.transition_date.desc()).limit(20).all()

    return render_template('dashboard/plant_manager.html',
                         warehouses=warehouses,
                         processing_products=processing_products)

def warehouse_manager_dashboard():
    """Warehouse manager's dashboard - shows warehouse operations"""
    warehouses = Warehouse.query.filter_by(type='warehouse').all()
    stored_products = ProductTracking.query.join(Warehouse).filter(
        Warehouse.type == 'warehouse'
    ).order_by(ProductTracking.transition_date.desc()).limit(20).all()

    return render_template('dashboard/warehouse_manager.html',
                         warehouses=warehouses,
                         stored_products=stored_products)
