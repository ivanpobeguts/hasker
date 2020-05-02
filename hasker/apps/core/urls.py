from django.urls import path

from .views import IndexView, AskView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ask', AskView.as_view(), name='ask'),
]
