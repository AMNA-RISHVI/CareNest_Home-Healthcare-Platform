from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):

        return str(user.pk) + str(timestamp) + str(user.email_verified)


account_activation_token = EmailVerificationTokenGenerator()


class PasswordResetTokenGeneratorCustom(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):

        return str(user.pk) + str(timestamp) + str(user.password)


password_reset_token = PasswordResetTokenGeneratorCustom()