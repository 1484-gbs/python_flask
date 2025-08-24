from enum import Enum
from wtforms import (
    FileField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    RadioField,
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ImageConversionType(Enum):
    IMREAD_GRAYSCALE = (0, "グレーアウト")
    FACE_CASCADE = (-1, "顔検知")

    def __init__(self, data, title) -> None:
        super().__init__()
        self.data = data
        self.title = title


class ImageForm(FlaskForm):
    file = FileField(
        validators=[FileRequired(), FileAllowed(["jpg", "png", "jpeg"], "Images only!")]
    )
    type = SelectField(
        choices=[(t.data, t.title) for t in ImageConversionType.__members__.values()],
        validators=[DataRequired()],
    )
    send = SubmitField("送信")


class ImageResultForm(FlaskForm):
    encode_string = StringField()
    hidden_encode_string = HiddenField()
    upload = SubmitField("S3 Upload")
