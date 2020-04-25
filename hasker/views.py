from django.shortcuts import render
from .forms import UserForm


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            person = user_form.save()
            if 'avatar' in request.FILES:
                person.avatar = request.FILES['avatar']
                person.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'sign_up.html',
                  {'user_form': user_form})
