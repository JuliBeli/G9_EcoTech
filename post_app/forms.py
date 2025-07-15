from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import PostRaw

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


# login form
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)  # Correctly pass the request and other arguments
        for field_i in self.fields:
            self.fields[field_i].widget.attrs.update({'class': 'large-input'})

# create new post form
class PostForm(forms.ModelForm):
    class Meta:
        model = PostRaw
        fields = ['title', 'content', 'image']
