import http
import os
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, logout_user
from flask_app.forms.login_form import MfaForm, LoginForm
from flask_app.usecase.login import Login
from werkzeug.exceptions import BadRequest
from flask_app.usecase.mfa import Mfa

func_login = Blueprint("func_login", __name__)


@func_login.get("/login")
def get():
    if current_user.is_authenticated:
        return redirect(url_for("func_index.index"))

    return render_template("login.html", form=LoginForm())


@func_login.post("/login")
def login():
    if current_user.is_authenticated:
        return __redirect()
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("login_contents.html", form=form)

    is_mfa = bool(os.getenv("IS_MFA", "False"))

    try:
        mfa_id, mfa_code = Login().execute(form=form, is_mfa=is_mfa)
    except BadRequest as e:
        return render_template("login_contents.html", form=form, message=e.description)

    next_page = request.form.get("next")

    if is_mfa:
        return render_template(
            "mfa.html",
            form=MfaForm(
                login_id=form.login_id.data, mfa_id=mfa_id, next_page=next_page
            ),
        )
    return __redirect(next_page)


@func_login.post("/mfa")
def mfa():
    form = MfaForm()
    try:
        Mfa().execute(
            login_id=form.login_id.data,
            mfa_id=form.mfa_id.data,
            mfa_code=form.mfa_code.data,
        )
    except BadRequest as e:
        return render_template("mfa.html", form=form, message=e.description)

    return __redirect(form.next.data)


@func_login.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("func_login.get"))


def __redirect(next_page=None):
    return (
        "",
        http.HTTPStatus.OK,
        {
            "HX-Redirect": (next_page if next_page else url_for("func_index.index")),
        },
    )
