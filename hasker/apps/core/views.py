from django.views.generic import CreateView, ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail

from .models import Question, Tag, Answer
from .services import vote
from .forms import AskForm, AnswerForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Question
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        if self.request.GET.get('order_by') == 'hot':
            qs = qs.order_by('-rating', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        return context


class AskView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = AskForm
    template_name = 'core/ask.html'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object = None

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.slug = slugify(question.title)[:49]
            question.save()
            tag_names = form.cleaned_data.get('tags')
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            return redirect('index')
        else:
            return self.form_invalid(form)


class QuestionDetailView(DetailView, FormMixin):
    template_name = 'core/question.html'
    model = Question
    context_object_name = 'question'
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        answers = (
            Answer.objects.filter(question=question)
                .order_by('-rating', '-created_at')
        )
        correct_answer = any(answer.is_correct for answer in answers)

        context.update(dict(answers=answers,
                            answer_form=self.form_class(),
                            correct_answer=correct_answer))
        return context

    def form_valid(self, form):
        answer = form.save(commit=False)
        question = self.get_object()
        answer.question = question
        answer.author = self.request.user
        answer.save()

        # doesn't work!
        # link = self.request.build_absolute_uri()
        # send_mail(
        #     'HASKER: You have a new answer!',
        #     f'Check out the new answer to your question: \n {link}',
        #     'from@example.com',
        #     [question.author.email],
        #     fail_silently=False,
        # )

        return redirect('question', slug=self.kwargs['slug'])

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        question = self.get_object()
        self.object = question
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VoteView(LoginRequiredMixin, FormView):
    template_name = 'core/question.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        value = int(request.POST.get('value'))
        entity_id = request.POST.get('entity_id')
        type = request.POST.get('entity_type')
        vote(entity_id, type, request.user, value)
        return redirect(request.META['HTTP_REFERER'])
