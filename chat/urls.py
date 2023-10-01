from django.urls import path
from . import views
from authentication.views import login_view, logout_view, register_user, profile
urlpatterns = [
    path('chat', views.index, name='index'),
]