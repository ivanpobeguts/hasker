from django.urls import path
from hasker.views import SignUpView, SignInView


urlpatterns = [
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', SignInView.as_view(), name='sign_in'),
]