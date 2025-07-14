# Create your views here.

from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@never_cache
def index(request):
    # context = {
    #     'version': datetime.now().strftime('%Y%m%d%H%M%S'),  # Use the current date and time as the version number
    #     'user': request.user
    # }
    # return render(request, 'index.html', context)
    return render(request, 'index.html')


# register form
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)  # Correctly pass the request and other arguments
        for field_i in self.fields:
            self.fields[field_i].widget.attrs.update({'class': 'large-input'})

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Invalid username or password.')
        else:
            # Access errors only after calling is_valid()
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# register form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_i in self.fields:
            self.fields[field_i].widget.attrs.update({'class': 'large-input'})
        # Remove the password confirmation field
        if 'password2' in self.fields:
            del self.fields['password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

@never_cache
def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #save user record in database
            return redirect("login")  # login
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def reset(request):
    return render(request, 'reset.html')

@never_cache
@login_required
def main(request):
    context = {
        'version': datetime.now().strftime('%Y%m%d%H%M%S'),  # Use the current date and time as the version number
        'user': request.user
    }
    return render(request, 'main.html', context)
    # return render(request, 'index.html')