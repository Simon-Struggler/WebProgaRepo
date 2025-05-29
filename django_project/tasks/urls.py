from django.urls import path
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path("", views.index, name="index"),
    path("breeds/", views.breeds, name="breeds"),
    path("care/", views.care, name="care"),
    path("register/", views.register_view, name="register"),
    path('like_breed/', views.like_breed, name='like_breed'),
    path('get_likes/', views.get_likes, name='get_likes'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
