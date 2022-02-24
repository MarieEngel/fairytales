from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("collection/", views.collection, name="collection"),
    path("collection/<slug>/", views.fairytale, name="fairytale"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add_fairytale/", views.add_fairytale, name="add_fairytale"),
    path("search/", views.search, name="search"),
    path("profile/", views.profile, name="profile"),
    path("add_category/", views.add_category, name="add_category"),
    path("category/<str:cats>/", views.CategoryView, name="category"),
    path("collection/edit/<int:id>/", views.update_fairytale, name="update_fairytale"),
    path("collection/<int:id>/delete", views.delete_fairytale, name="delete_fairytale"),
    path("collection/<int:pk>/comment/", views.add_comment, name="add_comment"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
