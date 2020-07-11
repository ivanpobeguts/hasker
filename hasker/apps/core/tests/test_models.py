import pytest

from ..models import Question, Answer, vote


@pytest.mark.django_db
def test_update_question_rating(person, tag):
    new_question = Question(title='Title', body='Where is test?', author=person, slug='title')
    assert new_question.rating == 0
    new_question.save()
    new_question.tags.add(tag)
    new_question.save()

    queried_question = Question.objects.get()
    queried_question.update_rating(1)
    assert queried_question.rating == 1


@pytest.mark.django_db
def test_update_question_params(person, question):
    question.update_params(person, ['tag1', 'tag2'])

    queried_question = Question.objects.get()
    assert queried_question.author.username == 'testuser'
    assert [t.name for t in queried_question.tags.all()] == ['tag1', 'tag2']


@pytest.mark.django_db
def test_get_trending_questions(person):
    question1 = Question(title='Title1', body='Where is test?', author=person, slug='title1', rating=5)
    question1.save()
    question2 = Question(title='Title2', body='Where is test?', author=person, slug='title2', rating=10)
    question2.save()

    questions = Question.trending()
    assert len(questions) == 2
    assert questions[0].rating == 10


@pytest.mark.django_db
def test_find_question_by_title(person):
    question = Question(title='Title1', body='Where is test?', author=person, slug='title1', rating=5)
    question.save()

    questions = Question.find_by_title('Title1')
    assert len(questions) == 1
    assert questions[0].title == 'Title1'


@pytest.mark.django_db
def test_find_question_by_tag(person, tag, question):
    question.tags.add(tag)
    question.save()

    questions = Question.find_by_tag('tag1')
    assert len(questions) == 1
    assert 'tag1' in [t.name for t in questions[0].tags.all()]


@pytest.mark.django_db
def test_update_answer_rating(person, question):
    answer = Answer(body='Answer', author=person, question=question)
    assert answer.rating == 0
    answer.save()

    answer = Answer.objects.get()
    answer.update_rating(1)
    assert answer.rating == 1


@pytest.mark.django_db
def test_update_answer_params(question, person):
    answer = Answer(body='body')
    answer.update_params(question, person)
    answer.save()

    answer = Answer.objects.get()
    assert answer.author.username == 'testuser'
    assert answer.question.title == 'Title1'


@pytest.mark.django_db
def test_mark_answer_as_correct_ok(person, another_person, question):
    answer = Answer(body='Answer', author=person, question=question)
    assert not answer.is_correct
    answer.save()

    answer = Answer.objects.get()
    answer.mark_correct(another_person)
    assert answer.is_correct


@pytest.mark.django_db
def test_mark_answer_as_correct_same_author(person, another_person, question):
    answer = Answer(body='Answer', author=person, question=question)
    assert not answer.is_correct
    answer.save()

    answer = Answer.objects.get()
    answer.mark_correct(person)
    assert not answer.is_correct


@pytest.mark.django_db
def test_vote_ok(question, person):
    vote(question.id, 'question', person, 1)

    updated_question = Question.objects.get(pk=question.id)
    assert updated_question.rating == 1

    vote(question.id, 'question', person, 1)

    updated_question = Question.objects.get(pk=question.id)
    assert updated_question.rating == 0

    vote(question.id, 'question', person, -1)

    updated_question = Question.objects.get(pk=question.id)
    assert updated_question.rating == -1

    vote(question.id, 'question', person, -1)

    updated_question = Question.objects.get(pk=question.id)
    assert updated_question.rating == 0


@pytest.mark.django_db
def test_vote_answer_author(person, question):
    answer = Answer(body='Answer', author=person, question=question)
    answer.save()
    vote(answer.id, 'answer', answer.author, 1)

    updated_answer = Answer.objects.get(pk=answer.id)
    assert updated_answer.rating == 0
