from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('password/', views.password, name='password'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]