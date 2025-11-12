from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    product_type = SelectField('Product Type', choices=[
        ('tomato', 'Tomato'),
        ('potato', 'Potato'),
        ('carrot', 'Carrot'),
        ('lettuce', 'Lettuce'),
        ('spinach', 'Spinach'),
        ('cucumber', 'Cucumber'),
        ('pepper', 'Pepper'),
        ('onion', 'Onion')
    ], validators=[DataRequired()])
    variety = StringField('Variety')
    quantity = FloatField('Quantity (kg)', validators=[DataRequired(), NumberRange(min=0.1)])
    quality_grade = SelectField('Quality Grade', choices=[
        ('A', 'Grade A - Premium'),
        ('B', 'Grade B - Standard'),
        ('C', 'Grade C - Below Standard')
    ], default='A', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class ProductTrackingForm(FlaskForm):
    warehouse_id = SelectField('Warehouse/Processing Plant', coerce=int, validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('received', 'Received'),
        ('processing', 'Processing'),
        ('stored', 'Stored'),
        ('shipped', 'Shipped'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    quantity = FloatField('Quantity (kg)', validators=[DataRequired(), NumberRange(min=0.1)])
    quality_notes = TextAreaField('Quality Notes/Comments')
    submit = SubmitField('Update Tracking')
