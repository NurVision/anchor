from django.urls import path

from apps.users import views

app_name = "apps.user"

urlpatterns = [
    # Email verification endpoints
    path("auth/send-validation/", views.SendValidationView.as_view(), name="send-validation-endpoint"),
    path("auth/verify-email/", views.VerifyEmailAPIView.as_view(), name="verify-email"),
    path("auth/cancel-account/", views.CancelAccountAPIView.as_view(), name="cancel-account"),  # Add this

    # Authentication endpoints
    path("auth/login/", views.LoginAPIView.as_view(), name="login"),
    # path("auth/logout/", views.LogoutAPIView.as_view(), name="logout"),

    # Reset password endpoints
    path("forget-password/", views.RequestPasswordResetAPIView.as_view(), name="request-password-reset"),
    path("forget-password/reset/", views.ResetPasswordAPIView.as_view(), name="reset-password"),

    # Self Profile endpoints
    path('profile/', views.ProfileManageAPIView.as_view(), name="profile-manage"),
    path('profile/avatar/upload/', views.UploadAvatarAPIView.as_view(), name='upload-avatar'),
    path('profile/avatar/delete/', views.DeleteAvatarAPIView.as_view(), name='delete-avatar'),
]
