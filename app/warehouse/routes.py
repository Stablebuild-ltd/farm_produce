from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Warehouse, ProductTracking
from app.warehouse.forms import WarehouseForm

warehouse = Blueprint('warehouse', __name__)

@warehouse.route('/warehouses')
@login_required
def list_warehouses():
    if current_user.role == 'farmer':
        flash('Farmers do not have access to warehouse management.', 'danger')
        return redirect(url_for('dashboard.index'))

    warehouses = Warehouse.query.all()
    return render_template('warehouse/list.html', warehouses=warehouses)

@warehouse.route('/warehouse/new', methods=['GET', 'POST'])
@login_required
def new_warehouse():
    if current_user.role not in ['plant_manager', 'warehouse_manager']:
        flash('You do not have permission to create warehouses.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = WarehouseForm()
    if form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            type=form.type.data,
            location=form.location.data,
            capacity=form.capacity.data
        )
        db.session.add(warehouse)
        db.session.commit()
        flash('Warehouse/Processing plant has been created successfully!', 'success')
        return redirect(url_for('warehouse.list_warehouses'))
    return render_template('warehouse/new.html', title='New Warehouse', form=form)

@warehouse.route('/warehouse/<int:warehouse_id>')
@login_required
def view_warehouse(warehouse_id):
    if current_user.role == 'farmer':
        flash('Farmers do not have access to warehouse details.', 'danger')
        return redirect(url_for('dashboard.index'))

    warehouse = Warehouse.query.get_or_404(warehouse_id)
    trackings = ProductTracking.query.filter_by(warehouse_id=warehouse_id).order_by(
        ProductTracking.transition_date.desc()).all()

    return render_template('warehouse/view.html', warehouse=warehouse, trackings=trackings)
