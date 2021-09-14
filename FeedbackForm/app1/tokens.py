import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime


class TokenGenerator(PasswordResetTokenGenerator):
    '''to generate a token for account activation'''

    def _make_hash_value(self, email, timestamp):
        '''to generate token'''
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        print(timestamp)
        # return (six.text_type(user.pk) + six.text_type(timestamp) +        six.text_type(user.is_active))
        return (six.text_type(email) + six.text_type(timestamp))


account_activation_token = TokenGenerator()
