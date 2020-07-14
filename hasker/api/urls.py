from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    AnswersAPIView,
    IndexAPIView,
    QuestionDetailAPIView,
    TagSearchAPIView,
    TextSearchAPIView,
    TrendingAPIView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Hasker API",
      default_version='v1',
      description="API documentation for Hasker application",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
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
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
