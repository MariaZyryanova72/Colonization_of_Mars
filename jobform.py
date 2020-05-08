from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField("Title of activity", validators=[DataRequired()])
    team_leader = IntegerField("Id team leader", validators=[DataRequired()])
    work_size = IntegerField("Work size", validators=[DataRequired()])
    collaborators = StringField("List id of collaborators", validators=[DataRequired()])
    hazard_category = StringField("Hazard category", validators=[DataRequired()])
    is_finished = BooleanField("Is finished?")
    submit = SubmitField('Submit')
