from django.urls import resolve, reverse


def test_register_ok():
    assert reverse('sign_up') == '/register/'
    assert resolve('/register/').view_name == 'sign_up'


def test_login_ok():
    assert reverse('sign_in') == '/login/'
    assert resolve('/login/').view_name == 'sign_in'


def test_logout_ok():
    assert reverse('sign_out') == '/logout/'
    assert resolve('/logout/').view_name == 'sign_out'


def test_settings_ok():
    assert reverse('settings') == '/settings/'
    assert resolve('/settings/').view_name == 'settings'
