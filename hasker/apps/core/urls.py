from django.urls import path, re_path

from .views import IndexView, AskView, QuestionDetailView, VoteView

urlpatterns = [
    path('?filter', IndexView.as_view(), name='index'),
    path('ask', AskView.as_view(), name='ask'),
    path('vote', VoteView.as_view(), name='vote'),
    path('question/<slug:slug>', QuestionDetailView.as_view(), name='question'),
]
