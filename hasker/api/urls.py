from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AnswersAPIView,
    IndexAPIView,
    QuestionDetailAPIView,
    TagSearchAPIView,
    TextSearchAPIView,
    TrendingAPIView,
)

app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('index', IndexAPIView.as_view(), name='index'),
    path('trending', TrendingAPIView.as_view(), name='trending'),
    path('search:text', TextSearchAPIView.as_view(), name='text_search'),
    path('search:tag', TagSearchAPIView.as_view(), name='tag_search'),
    path('question/<slug:slug>', QuestionDetailAPIView.as_view(), name='question'),
    path('question/<slug:slug>/answers', AnswersAPIView.as_view(), name='answers'),
]
