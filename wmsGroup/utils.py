from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, phone, timestamp):
        return (text_type(phone)+text_type(timestamp))

token_generator = AppTokenGenerator()