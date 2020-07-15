from rest_framework import serializers

from hasker.apps.questions.models import Answer, Question


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, question):
        return [tag.name for tag in question.tags.all()]

    def get_answers(self, question):
        return question.answers.count()

    def get_author(self, question):
        return question.author.username

    class Meta:
        model = Question
        fields = ('title', 'body', 'created_at', 'author', 'tags', 'slug', 'rating', 'answers')


class TrendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'rating')


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, answer):
        return answer.author.username

    class Meta:
        model = Answer
        fields = ('body', 'author', 'created_at', 'author', 'rating', 'is_correct')