#Todo написать бэкенд для  регистрации пользователей

from flask import *
from flask_login import *
from user import User
from forms import *
from our_requests import *
import datetime


app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = "secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: int):
    user = get_user_by_id(cur, user_id)
    if user:
        return User(*user[0])
    return None


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def autorisation():
    if current_user.is_authenticated:
        return redirect('/read')
    form = AutorisationForm()
    if form.validate_on_submit():
        us = get_user_by_email(cur, form.email.data.lower())
        print(generate_password(form.password.data))
        if us and us[0][4] == generate_password(form.password.data):
            user = User(*us[0])
            login_user(user, remember=form.remember_me.data)
            return redirect('read')
        return render_template(
            "login.html",
            title="Авторизация",
            form=form,
            message="Неправильный логин или пароль",
        )
    return render_template("login.html", title="Авторизация", form=form, message="")



@app.route('/read')
def read():
    return  '<a class="navbar-brand" href="/logout">{{ current_user.firstname }}</a>'

if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    app.run(port=8000, host="127.0.0.1")
    redirect('/logout')