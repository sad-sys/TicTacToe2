from django.urls import path
from . import views

urlpatterns = \
[
    path("", views.homePage, name = "home"),
    path("joinAsO", views.joinAsO, name="joinAsO"),
    path("checkGameState", views.checkGameState, name="checkGameState"),
    path("xPlayer/<str:gameCode>/", views.xPlayer, name = "xPlayer"),
    path("updateGameBoard/<str:gameCode>/", views.updateGameBoard, name="updateGameBoard"),
    path('getGameBoard/<str:gameCode>/', views.getGameBoard, name='get-game-board'),
]