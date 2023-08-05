from django.conf import settings
import requests

from wedge.services.abstract_service import AbstractService


class GoogleRecaptchaService(AbstractService):
    @staticmethod
    def verify_token(recaptcha_token):
        """
        Get Recaptcha V3 score with the front token
        You have to define GOOGLE_RECAPTCHA_SECRET_KEY in settings
        with recaptcha server api key
        """

        recaptcha_data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_token,
        }

        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=recaptcha_data
        )
        result = r.json()

        return result.get("score")
