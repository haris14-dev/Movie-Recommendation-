from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # <-- homepage
    path("suggestions/", views.get_suggestions, name="suggestions"),
    path("recommendations/", views.get_recommendations, name="recommendations"),
    path("poster_status/", views.get_poster_status, name="poster_status"),
]

