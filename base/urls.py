from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"), 
    path('login',views.loginpage,name="login"), 
    path('signup',views.register, name = "signup"),
    path('logout', views.logoutpage, name="logout"),
    path('room/<int:pk>/',views.room,name="room"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>/', views.update_room, name="update-room"),
    path('delete-room/<str:pk>/', views.delete_room, name="delete-room"),
]
