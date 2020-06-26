from django.urls import path
from BasicFunc import views

urlpatterns = [
	path('login/', views.user_login),
]