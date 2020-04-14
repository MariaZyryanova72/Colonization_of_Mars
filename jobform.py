from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField("Title of activity", validators=[DataRequired()])
    team_leader = IntegerField("Id team leader", validators=[DataRequired()])
    work_size = IntegerField("Duration", validators=[DataRequired()])
    collaborators = StringField("List id of collaborators", validators=[DataRequired()])
    start_date = DateField("Start date", validators=[DataRequired()])
    end_date = DateField("End date", validators=[DataRequired()])
    is_finished = BooleanField("Is finished", validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])
