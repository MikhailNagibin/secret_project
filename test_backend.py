from flask import *
from forms import *
import datetime


app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = "secret_key"


@app.route("/", methods=["GET", "POST"])
def autorisation():
    form = AutorisationForm()
    if form.validate_on_submit():
        return redirect("/inventory")
    return render_template("login.html", title="Авторизация", form=form, message="")


@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect("/inventory")
    return render_template("register.html", title="Регистрация", form=form, message="")


if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1", debug=True)
