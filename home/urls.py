from django.urls import path
from . import views
from authentication.views import login_view, logout_view, register_user
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('register/', register_user, name="register"),
    path('sidenavcreate/', views.sidenavcreate, name='sidenavcreate'),
    path('folder/', views.create_folder, name='folder'),
    path('file/', views.create_file, name='file'),

    path('import_data/', views.import_data, name='import_data'),
    path('export_data/', views.export_data, name='export_data'),
    path('add_data/', views.add_data, name='add_data'),

]
