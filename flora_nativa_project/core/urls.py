from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("planta/<int:pk>/", views.detalle_planta, name="detalle_planta"),
    path("registro/", views.registro_usuario, name="registro"),
    path("login/", views.login_usuario, name="login"),
    path("logout/", views.logout_usuario, name="logout"),
]
