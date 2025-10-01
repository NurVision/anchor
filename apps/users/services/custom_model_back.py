class EmailOrUsernameModelBackend:
    """
    Custom authentication backend to allow login with either username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        from django.contrib.auth import get_user_model
        from django.db.models import Q

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        """
        Ensure the user is active and not soft deleted before allowing authentication.
        """
        return getattr(user, 'is_active', False) and not getattr(user, 'is_deleted', False)

    def get_user(self, user_id):
        """
        Retrieve a user by their ID for session-based authentication.
        """
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            if self.user_can_authenticate(user):
                return user
            return None
        except UserModel.DoesNotExist:
            return None



