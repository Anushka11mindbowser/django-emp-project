from django.urls import path
from emp_manager import views

urlpatterns = [
    path('register', views.RegisterSuperUser.as_view()),
    path('login', views.Login.as_view()),
    path('userlist', views.UserList.as_view())

]