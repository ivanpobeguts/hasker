from django.urls import path

from .views import (
    IndexView,
    AskView,
    QuestionDetailView,
    VoteView,
    SearchView,
    TagView,
    SearchRedirectView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ask', AskView.as_view(), name='ask'),
    path('vote', VoteView.as_view(), name='vote'),
    path('search', SearchView.as_view(), name='search'),
    path('tags', TagView.as_view(), name='tags'),
    path('search_redirect', SearchRedirectView.as_view(), name='search_redirect'),
    path('question/<slug:slug>', QuestionDetailView.as_view(), name='question'),
]
