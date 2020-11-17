from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class RegistrationTokenGenerator(PasswordResetTokenGenerator):

    def __init__(self, __timeout=300):
        self.__timeout = __timeout
        super().__init__()

    def make_token(self, user):
        return self._make_token_with_timestamp(user, self._num_seconds(self._now()))

    def check_token(self, user, token):
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False
        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            if not constant_time_compare(
                    self._make_token_with_timestamp(user, ts, legacy=True),
                    token,
            ):
                return False
        if (self._num_seconds(self._now()) - ts) > self.__timeout:
            return False

        return True

    def _num_seconds(self, dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    def _now(self):
        return datetime.now()

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(user.email) + str(user.is_active) + str(timestamp)


registration_token_gen = RegistrationTokenGenerator()
