from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, HiddenField, SelectField
from wtforms.validators import URL, Regexp

class InstForm(FlaskForm):
    institution_id = HiddenField()
    provider_id = IntegerField('Provider id')
    provider_code = StringField('Provider code')
    trading_name = StringField('Trading Name')
    name = StringField('Name')
    type = SelectField('Type', choices = [('Government','Government'),('Private','Private')])
    total_capacity = IntegerField('Total Capacity')
    website = StringField('Website',default='http://',validators=[URL(message='Please enter a valid URL')])
    postal_address = TextAreaField('Postal Address')
    locations = StringField('Locations')
    favourite = StringField('Favourite')
    status = StringField('Status')
    submit = SubmitField('Send')

class Institution:
    def __init__(self,inst):
        self.institution_id = inst[0]
        self.provider_id = inst[1]
        self.provider_code = inst[2]
        self.trading_name = inst[3]
        self.name = inst[4]
        self.type = inst[5]
        self.total_capacity = inst[6]
        self.website = inst[7]
        self.postal_address = inst[8]
        self.locations = inst[9]
        self.favourite = inst[10]
        self.status = inst[11]
