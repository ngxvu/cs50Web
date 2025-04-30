from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    # api for email
    path("emails", views.compose, name="compose"), # send email
    path("emails/<int:email_id>", views.email, name="email"), # view email
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"), # view mailbox
]
