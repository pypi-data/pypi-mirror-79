# -*- coding: utf-8 -*-

"""
pages url config
"""

from django.urls import path

from . import views


app_name = "discordpingformatter"

urlpatterns = [
    path("", views.index, name="index"),
]
