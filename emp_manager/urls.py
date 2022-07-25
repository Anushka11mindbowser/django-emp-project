from django.urls import path
from emp_manager import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('userlist', views.ProfileList.as_view()),
    path('user_profile/<pk>', views.RetrieveProfile.as_view()),
    path('changePassword', views.ChangePassword.as_view()),
    path('updateProfile/<pk>', views.UpdateProfile.as_view()),
    path('reset_password', views.SendResetPasswordView.as_view()),
    path('logout', views.UserLogout.as_view())

]