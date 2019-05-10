#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

from django.conf.urls import url, include
from app import views


urlpatterns = [
    url(r"^$", views.home, name="home"),
    url(r"app/$", views.app, name="app"),
]
