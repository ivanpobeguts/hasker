import re

from django.views.generic import CreateView, ListView, DetailView, FormView, RedirectView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .models import Question, Answer, vote
from .forms import AskForm, AnswerForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Question
    paginate_by = settings.PAGE_SIZE

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


class SearchView(ListView):
    template_name = 'core/search.html'
    model = Question
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self, *args, **kwargs):
        return Question.find_by_title(self.request.GET.get('q'))


class TagView(ListView):
    template_name = 'core/search.html'
    model = Question
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return Question.find_by_tag(self.request.GET.get('q'))


class SearchRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        input_string = self.request.GET.get('q')
        parsed_input = re.match(r'tag:(\w+)', input_string)
        if parsed_input:
            tag_name = parsed_input.group(1)
            return f"{reverse('tags')}?q={tag_name}"
        return f"{reverse('search')}?q={input_string}"


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
            question.update_params(request.user, form.cleaned_data.get('tags'))
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
        answers, correct_answer = Answer.get_correct(question)
        context.update(dict(answers=answers,
                            answer_form=self.form_class(),
                            correct_answer=correct_answer))
        return context

    def form_valid(self, form):
        answer = form.save(commit=False)
        question = self.get_object()
        answer.update_params(question, self.request.user)
        self.send_email(question.author.email)

        return redirect('question', slug=self.kwargs['slug'])

    def send_email(self, email_to_send):
        link = self.request.build_absolute_uri()
        send_mail(
            'HASKER: You have a new answer!',
            f'Check out the new answer to your question: \n {link}',
            'from@example.com',
            [email_to_send],
            fail_silently=False,
            html_message=f'<p>Check out the new answer to your question: \n {link}<p>',
        )

    @method_decorator(login_required(login_url='/login/'))
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


class CorrectAnswerView(LoginRequiredMixin, FormView):
    template_name = 'core/question.html'
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        answer_id = request.POST.get('id')
        answer = get_object_or_404(Answer, id=answer_id)
        answer.mark_correct(request.user)
        return redirect(request.META['HTTP_REFERER'])
