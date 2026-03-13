from . import views
from django.urls import path

urlpatterns = [
    path("webhook/", views.webhook, name="webhook"),
    path("health/", views.health)
]