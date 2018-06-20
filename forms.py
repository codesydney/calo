from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, HiddenField, SelectField
from wtforms.validators import URL, Regexp

class InstForm(FlaskForm):
    institution_id = HiddenField()
    provider_id = IntegerField('Provider ID',render_kw={"size":"90"})   
    provider_code = StringField('Provider Code',render_kw={"size":"90"})   
    trading_name = StringField('Trading Name',render_kw={"size":"90"})   
    name = StringField('Name',render_kw={"size":"90"})   
    type = SelectField('Type', choices=[('Government','Government'),('Private','Private')])  
    total_capacity = IntegerField('Total Capacity',render_kw={"size":"90"})   
    website = StringField('Website',default='http://',validators=[URL(message='Please enter a valid URL')],render_kw={"size":"90"})  
    postal_address = StringField('Postal Address',render_kw={"size":"90"})   
    locations = StringField('Locations',render_kw={"size":"90"})   
    favourite = StringField('Favourite',render_kw={"size":"90"})   
    status = StringField('Status',render_kw={"size":"90"})   
    submit = SubmitField('Send',render_kw={"size":"90"})   

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
