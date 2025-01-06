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
        return redirect('/inventory_see')
    form = AutorisationForm()
    if form.validate_on_submit():
        us = get_user_by_email(cur, form.email.data.lower())
        if us and us[0][4] == generate_password(form.password.data):
            user = User(*us[0])
            login_user(user, remember=True)
            return redirect('/inventory_see')
        return render_template(
            "login.html",
            title="Авторизация",
            form=form,
            message="Неправильный логин или пароль",
        )
    return render_template("auth_templates/login.html", title="Авторизация", form=form, message="")


@app.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect('/inventory_see')
    form = RegistrationForm()
    if form.validate_on_submit():
        us = get_user_by_email(cur, form.email.data)
        if us:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        data = (
            form.name.data.title(),
            form.surname.data.title(),
            form.email.data.lower(),
            generate_password(form.password.data),
            int(form.role.data),
        )
        add_user(conn, data)
        us = get_user_by_email(cur, form.email.data)
        user = User(*us[0])
        login_user(user)
        return redirect('/inventory_see')
    return render_template("auth_templates/register.html", title="Регистрация", form=form)


@app.route('/inventory_see')
def inventory_see():
    user_role = "admin"
    inventory_items = [
        {"name": "Мяч", "quantity": 10, "status": "Хорошее"},
        {"name": "Ракетка", "quantity": 5, "status": "Используется"},
    ]
    return render_template('inventory_templates/inventory_see.html', user_role=user_role, inventory_items=inventory_items, active_page='inventory')


@app.route('/inventory_add')
def inventory_add():
    user_role = "admin"
    inventory_items = [
        {"name": "Мяч", "quantity": 10, "status": "Хорошее"},
        {"name": "Ракетка", "quantity": 5, "status": "Используется"},
    ]
    return render_template('inventory_templates/inventory_see.html', user_role=user_role, inventory_items=inventory_items, active_page='inventory')



if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    app.run(port=8000, host="127.0.0.1", debug=True)