from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, logout_user
from flask_app.forms.login_form import LoginForm
from flask_app.usecase.login import Login
from werkzeug.exceptions import BadRequest

func_login = Blueprint("func_login", __name__)


@func_login.get("/login")
def get():
    if current_user.is_authenticated:
        return redirect(url_for("func_index.index"))

    return render_template("login.html", form=LoginForm())


@func_login.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("func_index.index"))
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    try:
        Login().execute(form=form)
    except BadRequest as e:
        flash(e.description)
        return render_template("login.html", form=form)

    next_page = request.form.get("next")
    if next_page:
        return redirect(next_page)
    return redirect(url_for("func_index.index"))


@func_login.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("func_login.get"))
