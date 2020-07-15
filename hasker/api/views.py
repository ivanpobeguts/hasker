from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from hasker.apps.questions.models import Question
from .serializers import QuestionSerializer, TrendingSerializer, AnswerSerializer

SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="Hasker API",
        default_version='v1',
        description="API documentation for Hasker application",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


class IndexAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Question.objects.all()
        order_by_value = ['-rating', '-created_at'] if self.request.query_params.get('order_by') == 'hot' else [
            '-created_at']
        return qs.order_by(*order_by_value)


class TrendingAPIView(ListAPIView):
    serializer_class = TrendingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Question.trending()


class TextSearchAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Question.find_by_title(self.request.query_params.get('q'))


class TagSearchAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Question.find_by_tag(self.request.query_params.get('q'))


class QuestionDetailAPIView(RetrieveAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
    lookup_field = 'slug'


class AnswersAPIView(ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Question.get_by_slug(slug).answers.all()
