from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DepartamentsForm(FlaskForm):
    title = StringField("Title of departament", validators=[DataRequired()])
    chief = IntegerField("Id Chief", validators=[DataRequired()])
    members = IntegerField("Members", validators=[DataRequired()])
    email = StringField("Departament Email", validators=[DataRequired()])
    submit = SubmitField('Submit')
