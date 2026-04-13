from django.urls import path

from . import views

app_name = "repairs"

urlpatterns = [
    path("", views.services, name="services"),
    path("status/", views.status, name="status"),
    path("book/", views.book, name="book_general"),
    path("book/<slug:slug>/", views.book, name="book"),
    path("confirm/<uuid:reference>/", views.confirm, name="confirm"),
]
