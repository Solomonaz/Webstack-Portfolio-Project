from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.index, name='index'),
    # path('direct-message/<int:user_id>/', views.direct_message_detail, name='direct_message_detail'),
    # path('direct_message/', views.direct_message_detail, name='direct_message_detail'),

]