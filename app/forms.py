# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired()])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    num_tests = IntegerField('Количество тестов', validators=[DataRequired()])
    correct_solution = TextAreaField('Правильное решение', validators=[DataRequired()])
