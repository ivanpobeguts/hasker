from django.urls import path
from hasker.views import register


urlpatterns = [
    path('register/', register, name='sign_up'),
]