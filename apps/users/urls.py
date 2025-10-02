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

    # Reset password endpoints
    path("forget-password/", views.RequestPasswordResetAPIView.as_view(), name="logout"),
    path("forget-password/resend-otp/", views.ResendOTPAPIView.as_view(), name="resend-otp"),
    path("forget-password/validate/", views.VerifyOTPAndResetPasswordAPIView.as_view(), name="validate-otp"),

    # Self Profile endpoints
    path('profile/', views.ProfileManageAPIView.as_view(), name="profile-manage"),
]
