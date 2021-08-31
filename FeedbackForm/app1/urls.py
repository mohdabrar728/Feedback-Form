from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view()),
    path("formmaker", views.FormMake.as_view()),
    path("testformmaker", views.add)
]
