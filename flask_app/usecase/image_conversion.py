import datetime
from flask_app.models.s3_client import S3Client
from flask_app.forms.image_form import ImageConversionType
import pandas as pd
import cv2
import base64
import numpy as np


class ImageConversion:
    def execute(self, file, conversion_type):
        img_array = np.asarray(bytearray(file.read()), dtype=np.uint8)
        decode_type = (
            cv2.IMREAD_UNCHANGED
            if conversion_type != cv2.IMREAD_GRAYSCALE
            else cv2.IMREAD_GRAYSCALE
        )
        img = cv2.imdecode(img_array, decode_type)
        match conversion_type:
            case ImageConversionType.IMREAD_GRAYSCALE.data:
                pass
            case ImageConversionType.FACE_CASCADE.data:
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
                )
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                # 検出された顔を矩形で囲む
                for x, y, w, h in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        _, data = cv2.imencode(".jpg", img)
        return base64.b64encode(data).decode("utf-8")
