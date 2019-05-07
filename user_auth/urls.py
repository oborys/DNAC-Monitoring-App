from django.conf.urls import url
from user_auth import views


urlpatterns = [
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^registration/$", views.registration, name="registration"),
]