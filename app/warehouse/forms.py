from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class WarehouseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('processing', 'Processing Plant'),
        ('warehouse', 'Warehouse')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    capacity = FloatField('Capacity (tons)', validators=[DataRequired(), NumberRange(min=0.1)])
    submit = SubmitField('Create Warehouse')
