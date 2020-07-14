from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from hasker.apps.core.models import Question
from .serializers import QuestionSerializer, TrendingSerializer, AnswerSerializer


class IndexAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Question.objects.all()
        if self.request.query_params.get('order_by') == 'hot':
            qs = qs.order_by('-rating', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs


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
