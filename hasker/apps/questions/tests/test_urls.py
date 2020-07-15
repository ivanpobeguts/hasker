from django.urls import resolve, reverse


def test_register_ok():
    assert reverse('index') == '/'
    assert resolve('/').view_name == 'index'


def test_ask_ok():
    assert reverse('ask') == '/ask'
    assert resolve('/ask').view_name == 'ask'


def test_vote_ok():
    assert reverse('vote') == '/vote'
    assert resolve('/vote').view_name == 'vote'


def test_search_ok():
    assert reverse('search') == '/search'
    assert resolve('/search').view_name == 'search'


def test_tags_ok():
    assert reverse('tags') == '/tags'
    assert resolve('/tags').view_name == 'tags'


def test_search_redirect_ok():
    assert reverse('search_redirect') == '/search_redirect'
    assert resolve('/search_redirect').view_name == 'search_redirect'


def test_question_ok():
    assert reverse('question', kwargs={'slug': 'question1'}) == '/question/question1'
    assert resolve('/question/question1').view_name == 'question'
    assert resolve('/question/question1').kwargs == {'slug': 'question1'}


def test_correct_answer_ok():
    assert reverse('correct_answer') == '/correct_answer'
    assert resolve('/correct_answer').view_name == 'correct_answer'
