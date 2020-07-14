from django.urls import resolve, reverse


def test_index_ok():
    assert reverse('api:index') == '/api/v1/index'
    assert resolve('/api/v1/index').view_name == 'api:index'


def test_trending_ok():
    assert reverse('api:trending') == '/api/v1/trending'
    assert resolve('/api/v1/trending').view_name == 'api:trending'


def test_text_search_ok():
    assert reverse('api:text_search') == '/api/v1/search:text'
    assert resolve('/api/v1/search:text').view_name == 'api:text_search'


def test_tag_search_ok():
    assert reverse('api:tag_search') == '/api/v1/search:tag'
    assert resolve('/api/v1/search:tag').view_name == 'api:tag_search'


def test_question_ok():
    assert reverse('api:question', kwargs={'slug': 'question1'}) == '/api/v1/question/question1'
    assert resolve('/api/v1/question/question1').view_name == 'api:question'
    assert resolve('/api/v1/question/question1').kwargs == {'slug': 'question1'}


def test_answers_ok():
    assert reverse('api:answers', kwargs={'slug': 'question1'}) == '/api/v1/question/question1/answers'
    assert resolve('/api/v1/question/question1/answers').view_name == 'api:answers'
    assert resolve('/api/v1/question/question1/answers').kwargs == {'slug': 'question1'}