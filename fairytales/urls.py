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
    path("profile/",views.profile, name="profile" ),
    path("add_category/", views.add_category, name="add_category"),
    path("category/<str:cats>/",views.CategoryView, name="category"),
]
