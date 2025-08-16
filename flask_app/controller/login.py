import http
import os
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, logout_user
from flask_app.forms.login_form import CSRFOnlyForm, LoginForm
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
        return redirect(url_for("func_index.index"))
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    is_mfa = bool(os.getenv("IS_MFA", "False"))

    try:
        mfa_id, mfa_code = Login().execute(form=form, is_mfa=is_mfa)
    except BadRequest as e:
        flash(e.description)
        return "", http.HTTPStatus.OK, {"HX-Refresh": "true"}

    next_page = request.form.get("next")

    if is_mfa:
        return __create_mfa_html(
            login_id=form.login_id.data, mfa_id=mfa_id, next_page=next_page
        )
    else:
        return __redirect(next_page=next_page)


@func_login.post("/mfa")
def mfa():
    form = request.form
    try:
        Mfa().execute(
            login_id=form.get("login_id"),
            mfa_id=form.get("mfa_id"),
            mfa_code=form.get("mfa_code"),
        )
    except BadRequest as e:
        flash(e.description)
        return __redirect(next_page=form.get("next"))

    return __redirect(next_page=form.get("next"))


@func_login.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("func_login.get"))


def __create_mfa_html(login_id, mfa_id, next_page):
    form = CSRFOnlyForm()
    return f'<form method="post" action="{url_for('func_login.mfa')}">\
            <div class="input-group">\
                <label for="mfa_code">認証コード</label>\
                <input type="text" id="mfa_code" name="mfa_code" required>\
            </div>\
            <input type="submit" id="login_button" name="login_button" value="認証"></button>\
            <input type="hidden" name="login_id" value="{login_id}" />\
            <input type="hidden" name="mfa_id" value="{mfa_id}" />\
            <input type="hidden" name="next" value="{next_page}" />\
            <input type="hidden" name="csrf_token" value="{form.csrf_token.data}" />\
        </form>'


def __redirect(next_page=None):
    if next_page:
        return redirect(next_page)
    return redirect(url_for("func_index.index"))
