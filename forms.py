from wtforms import *
from flask_wtf import *
from wtforms.validators import *


class AutorisationForm(FlaskForm):
    email = EmailField("Введите Вашу почту", validators=[DataRequired()])
    password = PasswordField("Введите Ваш пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    # conn = get_db_connection()
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
    role = SelectField("Введите Вашу роль", choices=((1, 'Пользователь'), ))
    submit = SubmitField("Зарегистрироваться")
