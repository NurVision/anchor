from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, username, password, **extra_fields)

    def get_by_natural_key(self, username):
        """
        Allow authentication with both email and username.
        Since USERNAME_FIELD is 'email', this method is called when authenticating.
        We need to handle cases where username (which could be email or username) is passed.
        """
        try:
            return self.get(email=username)
        except self.model.DoesNotExist:
            return self.get(username=username)
