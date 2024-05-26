from django.urls import path
from  . import views

urlpatterns = [
path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.user_list, name='users'),
  # path('send-email/', views.send_test_email, name='send_test_email'),


]