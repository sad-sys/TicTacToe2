from django.urls import path
from . import views

urlpatterns = \
[
    path("", views.homePage, name = "home"),
    path("joinAsO", views.joinAsO, name="joinAsO"),
    path("checkGameState", views.checkGameState, name="checkGameState"),
    path("xPlayer", views.xPlayer, name = "xPlayer")
]