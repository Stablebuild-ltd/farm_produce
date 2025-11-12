from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Product, ProductTracking, Warehouse, User
from app.product.forms import ProductForm, ProductTrackingForm
from datetime import datetime

product = Blueprint('product', __name__)

@product.route('/products')
@login_required
def list_products():
    if current_user.role == 'farmer':
        products = Product.query.filter_by(farmer_id=current_user.id).all()
    else:
        products = Product.query.all()

    return render_template('product/list.html', products=products)

@product.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.role != 'farmer':
        flash('Only farmers can add new products.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            farmer_id=current_user.id,
            product_type=form.product_type.data,
            variety=form.variety.data,
            quantity=form.quantity.data,
            quality_grade=form.quality_grade.data
        )
        product.generate_hash()
        db.session.add(product)
        db.session.commit()
        flash('Product has been added successfully!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('product/new.html', title='New Product', form=form)

@product.route('/product/<int:product_id>')
@login_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.role == 'farmer' and product.farmer_id != current_user.id:
        flash('You can only view your own products.', 'danger')
        return redirect(url_for('dashboard.index'))

    trackings = ProductTracking.query.filter_by(product_id=product_id).order_by(
        ProductTracking.transition_date.desc()).all()

    return render_template('product/view.html', product=product, trackings=trackings)

@product.route('/product/<int:product_id>/track', methods=['GET', 'POST'])
@login_required
def track_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Check permissions
    if current_user.role == 'farmer':
        flash('Farmers cannot update product tracking.', 'danger')
        return redirect(url_for('product.view_product', product_id=product_id))

    form = ProductTrackingForm()
    form.warehouse_id.choices = [(w.id, f"{w.name} ({w.type})") for w in Warehouse.query.all()]

    if form.validate_on_submit():
        tracking = ProductTracking(
            product_id=product_id,
            warehouse_id=form.warehouse_id.data,
            status=form.status.data,
            quantity=form.quantity.data,
            quality_notes=form.quality_notes.data,
            processed_by=current_user.id
        )
        db.session.add(tracking)
        db.session.commit()

        # Update warehouse stock
        warehouse = Warehouse.query.get(form.warehouse_id.data)
        if form.status.data in ['stored', 'processing']:
            warehouse.current_stock += form.quantity.data
        elif form.status.data == 'shipped':
            warehouse.current_stock -= form.quantity.data

        db.session.commit()

        flash('Product tracking updated successfully!', 'success')
        return redirect(url_for('product.view_product', product_id=product_id))

    return render_template('product/track.html', title='Track Product', form=form, product=product)
