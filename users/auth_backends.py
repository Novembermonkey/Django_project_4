from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None

        if self._is_email(username):
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                user = None
        else:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def _is_email(self, value):
        try:
            validate_email(value)
            return True
        except ValidationError:
            return False
