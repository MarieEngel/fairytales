from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("collection/", views.collection, name="collection"),
    path("collection/<slug>/", views.fairytale, name="fairytale"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add_fairytale/", views.add_fairytale, name="add_fairytale"),
    path("search/", views.search, name="search"),
]
