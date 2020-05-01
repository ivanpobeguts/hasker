from django.urls import path
from hasker.views import SignUpView, IndexView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(template_name='person/sign_in.html'), name='sign_in'),
    path('logout/', LogoutView.as_view(), name='sign_out'),
]