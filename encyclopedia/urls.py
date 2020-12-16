from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),
    path("wiki/<str:articletitle>", views.article, name='articlepage'),
    path("edit/<str:articletitle>", views.editpage, name='editpage'),
]
