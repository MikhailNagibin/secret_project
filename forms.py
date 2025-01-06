from wtforms import *
from flask_wtf import *
from wtforms.validators import *
from our_requests import *


class AutorisationForm(FlaskForm):
    email = EmailField("Введите Вашу почту", validators=[DataRequired()])
    password = PasswordField("Введите Ваш пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    conn = get_db_connection()
    cur = conn.cursor()
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo('password', message='Пароли должны совпадать.')
        ])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    role = SelectField("Введите Вашу роль", choices=get_roles(cur))
    submit = SubmitField("Зарегистрироваться")


class InventoryaddForm(FlaskForm):
    conn = get_db_connection()
    cur = conn.cursor()
    name = StringField("Название", validators=[DataRequired()])
    quantity = IntegerField("Количество", validators=[DataRequired(), NumberRange(min=1, message="Количество должно быть неотрицательным")])
    submit = SubmitField("Добавить")


class EditInventoryForm(FlaskForm):
    conn = get_db_connection()
    cur = conn.cursor()
    name = StringField('Название', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    status = SelectField('Состояние', choices=get_conditions(cur))