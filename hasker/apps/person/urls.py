from django.urls import path
from .views import SignUpView, SettingsView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('logout/', LogoutView.as_view(), name='sign_out'),
    path('settings/', SettingsView.as_view(), name='settings'),
]