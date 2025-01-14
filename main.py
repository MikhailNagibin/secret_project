from flask import *
from flask import flash
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
def autorisation(): # Для всех
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
def registration(): # Для новых пользователей
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
def inventory_see(): # Для всех
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    inventory_items = get_free_inventory_for_read(cur)
    return render_template(
        "inventory_templates/inventory_see.html",
        user_role=user_role,
        inventory_items=inventory_items,
        active_page="inventory_see",
    )


@app.route("/inventory_add", methods=["GET", "POST"])
def inventory_add(): # Для админа
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    form = InventoryaddForm()
    if request.method == "POST":
        conditions_id = get_condition_id_by_condition(cur, 'Новый')[0][0]
        for _ in range(form.quantity.data):
            add_inventory(conn, form.name.data, conditions_id)
        return redirect('/inventory_add')
    return render_template(
        "inventory_templates/inventory_add.html",
        user_role=user_role,
        form=form,
        active_page="inventory_add",
    )


@app.route("/inventory_see/<int:item_id>", methods=["GET", "POST"])
def inventory_edit(item_id): # Для админа
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
        elif "delete" in request.form:
            delete_inventory_by_name_and_condition_id(conn, inventory_item[0], condition_id)
        return redirect(url_for("inventory_see"))

    return render_template("inventory_templates/inventory_edit.html", form=form,
        user_role=user_role)


@app.route('/create_report', methods=['GET', 'POST'])
def make_report(): # Для админа
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    form = ReportForm()
    if form.validate_on_submit():
        create_report(conn, form.sender_name.data, form.report_content.data)
        return redirect('/inventory_see')
    return render_template('inventory_templates/admin_reports.html', form=form,
        user_role=user_role,
        active_page="create_report")


@app.route('/purchases', methods=['GET', 'POST'])
def add_to_purchase_plan(): # Для админа
    # user_role = get_role_by_id(cur, current_user.role)[0][0]
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    form = PurchasePlanForm()
    if form.validate_on_submit():
        create_plane(conn, (form.item_name.data, form.quantity.data, form.price.data, form.supplier.data))
        return redirect('/inventory_see')
    return render_template('inventory_templates/purchases.html', form=form,
        user_role=user_role,
        active_page="purchases")


@app.route('/inventory_assign', methods=['GET', 'POST'])
def assign_inventory(): # Для админа
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    form = AssignInventoryForm()
    form.item.choices = list(map(lambda x: [x[0], x[0]], get_free_inventory_for_zacrep(cur)))
    form.user_name.choices = list(map(lambda x: [x[0], x[1] + ' ' + x[2]], get_users_id_firstname_and_surname(cur)))
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    assigned_inventory = get_occupied_inventory(cur)
    if form.validate_on_submit():
        user_name = form.user_name.data
        item = form.item.data
        quantity = form.quantity.data
        count = get_count_of_free_inventory_by_name(cur, item)
        # print(count, quantity)
        if count and quantity > count[0][0]:
            flash(f"Ошибка: Запрашиваемое количество {quantity} больше доступного ({count[0][0]}).",
                      "danger")
        else:
            flash(f"Запрос {quantity} шт. '{item}' принят.", "success")
            # print("jr")
            securing_inventory(conn, user_name, item, quantity)
            return redirect('/inventory_assign')
    return render_template('inventory_templates/inventory_assign.html', form=form, assigned_inventory=assigned_inventory,
        user_role=user_role,
        active_page="inventory_assign")


@app.route('/inventory_request', methods=['GET', 'POST'])
def request_inventory(): # ДЛя пользователя
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role == "Администратор":
        return redirect("/inventory_see")
    form = RequestInventoryForm()
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    form.item.choices = get_inventory_and_his_min_id(cur)
    my_requests = get_my_requests(cur, current_user.id)
    if form.validate_on_submit():
        item = form.item.data
        quantity = form.quantity.data
        status = get_status_id_by_status(cur, 'Не рассмотрен')
        print(status)
        add_request(conn, current_user.id, item, quantity, status[0][0])
        return redirect('/inventory_request')
    if request.method == 'POST':

        data = request.form.get('_method').split()
        print(data)
        if data[0] == 'Delete':
            pass
            # print(my_requests[int(data[-1])][0])
            delete_request(conn, my_requests[int(data[-1]) - 1][0])
            return redirect('/inventory_request')
    return render_template('inventory_templates/inventory_request.html', form=form, user_role=user_role,
        active_page="inventory_request", inventory_items=my_requests)


@app.route("/inventory_assign/<int:item_id>", methods=["GET", "POST"])
def inventory_request(item_id): # Для админа
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    data = get_occupied_inventory(cur)[item_id - 1]
    form = ConfirmDetachInventoryForm()
    form.user_name.data = data[0] + ' ' + data[1]
    form.item.data = data[2]
    form.quantity.data = data[3]
    if request.method == 'POST':
        user_id = get_user_id_by_fullname(cur, data[0], data[1])[0][0]
        detaching_inventory(conn, user_id, data[2])
        return redirect("/inventory_assign")
    return render_template("inventory_templates/inventory_assign_confirm.html",
        user_role=user_role, form=form)



@app.route('/application', methods=['GET', "POST"])
def application(): # Для админа
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect("/inventory_see")
    data = get_requests(cur)
    return render_template('inventory_templates/application.html', user_role=user_role,
                           active_page='application',  inventory_items=data)


@app.route('/application/<string:approved>/<int:item_id>', methods=['GET', 'POST'])
def application_approved(approved: str, item_id: int): # Для админа
    approved = approved.lower() == 'true'
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role != "Администратор":
        return redirect('/inventory_see')
    data = get_requests(cur)[item_id  - 1]
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            count = get_count_of_free_inventory_by_name(cur, data[-2])
            # print(count, not count, data[-1], data[-1] > count[0][0], )
            if not count or data[-1] > count[0][0]:
                flash(f"Ошибка: Запрашиваемое количество {data[-1]} больше доступного ({count[0][0]}).",
                      "danger")
                return render_template('inventory_templates/application_confirm.html',
                                       data=data[1:], approved=approved,
                                       message=f"Ошибка: Запрашиваемое количество {data[-1]} больше доступного ({count[0][0]}).")
            else:
                status_id = get_status_id_by_status(cur, 'Одобрен')[0][0]
                change_status_id(conn, data[0], status_id)
                user_id = get_user_id_by_fullname(cur, data[1], data[2])[0][0]
                securing_inventory(conn, user_id, data[-2], data[-1])
                return redirect('/application')
        elif request.form.get('_method') == 'DELETE':
            status_id = get_status_id_by_status(cur, 'Откланен')[0][0]
            change_status_id(conn, data[0],  status_id)
            return redirect('/application')
    return render_template('inventory_templates/application_confirm.html',  data=data[1:], approved=approved, message='')



@app.route('/repair_requests', methods=['GET', "POST"])
def repair_requests(): #Для пользователя
    user_role = get_role_by_id(cur, current_user.role)[0][0]
    if user_role == "Администратор":
        return redirect("/inventory_see")
    form = Repair_Requests()
    form.item.choices = get_inventory_and_his_min_id(cur)
    if form.validate_on_submit():
        data = (form.item.data, form.count.data, form.replace.data)
        add_repair_requests(conn, data)
    return render_template('inventory_templates/repair_requests.html', form=form,
                           active_page='repair_requests', user_role=user_role)


if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()
    app.run(host='0.0.0.0', port=8000, debug=True)
