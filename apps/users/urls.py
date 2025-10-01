from django.urls import path

from apps.users import views

app_name = "apps.user"

urlpatterns = [
    # auth
    path("auth/send-validation/", views.SendValidationView.as_view(), name="send-validation-endpoint"),
    path("auth/verify-email/", views.VerifyEmailAPIView.as_view(), name="verify-email"),

]
