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


@app.route("/", methods=["GET", "POST"])
def autorisation():
    if current_user.is_authenticated:
        return redirect("/inventory_see")
    form = AutorisationForm()
    if form.validate_on_submit():
        us = get_user_by_email(cur, form.email.data.lower())
        if us and us[0][4] == generate_password(form.password.data):
            user = User(*us[0])
            login_user(user, remember=True)
            return redirect("/inventory_see")
        return render_template(
            "auth_templates/login.html",
            title="Авторизация",
            form=form,
            message="Неправильный логин или пароль",
        )
    return render_template(
        "auth_templates/login.html", title="Авторизация", form=form, message=""
    )


@app.route("/register", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect("/inventory_see")
    form = RegistrationForm()
    if form.validate_on_submit():
        us = get_user_by_email(cur, form.email.data)
        if us:
            return render_template(
                "auth_templates/register.html",
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
        return redirect("/inventory_see")
    return render_template(
        "auth_templates/register.html", title="Регистрация", form=form
    )


@app.route("/inventory_see")
def inventory_see():
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    inventory_items = get_free_inventory_for_read(cur)
    return render_template(
        "inventory_templates/inventory_see.html",
        user_role=user_role,
        inventory_items=inventory_items,
        active_page="inventory_see",
    )


@app.route("/inventory_add", methods=["GET", "POST"])
def inventory_add():
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    form = InventoryaddForm()
    if request.method == "POST":
        conditions_id = get_condition_id_by_condition(cur, 'Новый')
        for _ in range(form.quantity.data):
            add_inventory(conn, form.name.data, conditions_id)
    return render_template(
        "inventory_templates/inventory_add.html",
        user_role=user_role,
        form=form,
        active_page="inventory_add",
    )


@app.route("/inventory_see/<int:item_id>", methods=["GET", "POST"])
def inventory_edit(item_id):
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    inventory_item = get_free_inventory_for_read(cur)[item_id - 1]
    condition_id = get_condition_id_by_condition(cur, inventory_item[2])[0][0]
    form = EditInventoryForm()
    if request.method == "GET":
        form.name.data = inventory_item[0]
        form.quantity.data = inventory_item[1]
        form.status.data = condition_id

    if request.method == "POST":
        if "save" in request.form:
            delete_inventory_by_name_and_condition_id(conn, inventory_item[0], condition_id)
            for _ in range(form.quantity.data):
                add_inventory(conn, form.name.data, form.status.data)
            print(form.name.data, form.status.data)
        elif "delete" in request.form:
            delete_inventory_by_name_and_condition_id(conn, inventory_item[0], condition_id)
        return redirect(url_for("inventory_see"))

    return render_template("inventory_templates/inventory_edit.html", form=form,
        user_role=user_role)


@app.route('/create-report', methods=['GET', 'POST'])
def create_report():
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    form = ReportForm()
    if form.validate_on_submit():
        sender_name = form.sender_name.data
        report_date = form.report_date.data
        report_content = form.report_content.data
        return f'{sender_name, report_content, report_date}'

    return render_template('inventory_templates/admin_reports.html', form=form,
        user_role=user_role,
        active_page="create-report")


if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    app.run(port=8000, host="127.0.0.1", debug=True)
