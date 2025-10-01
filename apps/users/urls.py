from django.urls import path

from apps.users import views

app_name = "apps.user"

urlpatterns = [
    # Email verification endpoints
    path("auth/send-validation/", views.SendValidationView.as_view(), name="send-validation-endpoint"),
    path("auth/verify-email/", views.VerifyEmailAPIView.as_view(), name="verify-email"),

    # Authentication endpoints
    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    path("auth/logout/", views.LogoutAPIView.as_view(), name="logout"),
]
