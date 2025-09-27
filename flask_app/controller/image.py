import datetime
import http
from flask import Blueprint, render_template, request
from flask_login import login_required
from flask_login import current_user
from flask_app.forms.image_form import ImageForm, ImageResultForm
from flask_app.models.s3_client import S3Client
from flask_app.usecase.image_conversion import ImageConversion


func_image = Blueprint("func_image", __name__)


@func_image.get("/image")
@login_required
def get():
    return render_template("image.html", form=ImageForm())


@func_image.post("/image")
@login_required
def post():
    form = ImageForm()
    file = form.file.data
    result = ImageConversion().execute(file=file, conversion_type=int(form.type.data))
    result_form = ImageResultForm(encode_string=result, hidden_encode_string=result)
    return render_template("image_result.html", form=result_form)


@func_image.post("/image/s3upload")
@login_required
def s3upload():
    form = ImageResultForm()
    S3Client().upload_file_from_base64_string(
        base64_string=form.hidden_encode_string.data,
        login_id=current_user.login_id,
        service_type="image_conversion",
        filename=f"image_conversion_{current_user.login_id}_{datetime.datetime.now()}.png",
    )

    return "", http.HTTPStatus.OK


@func_image.before_request
def before_request():
    # Flask-Loginのリダイレクト前にhtmxリクエストかをチェック
    if "HX-Request" in request.headers and not current_user.is_authenticated:
        # htmxリクエストで未認証の場合、HX-Refreshでリロードを指示
        return "", 200, {"HX-Refresh": "true"}
