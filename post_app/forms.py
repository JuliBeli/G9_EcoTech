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

class PostForm(forms.ModelForm):
    class Meta:
        model = PostRaw
        fields = ['title', 'content', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'post-title-input',
            'placeholder': 'Enter the title'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'post-content-input',
            'placeholder': 'Share your tips to make life greener'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'post-image-input'
        })

class SearchFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search articles/blogs...',
            'id': 'search',
        }
    ))
    post_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + PostRaw.POST_TYPE_CHOICES,
        widget=forms.Select()
    )

    author = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Author username',
        })
    )

    date_range = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Dates'),
            ('1d', 'Last 24 hours'),
            ('7d', 'Last 7 days'),
            ('1m', 'Last month'),
            ('1y', 'Last year')
        ],
        widget=forms.Select()
    )

    # start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    # end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('recent', "Newest First"),
            ('oldest', "Oldest First"),
            ('likes_desc', "Most Liked"),
            ('likes_asc', "Least Liked"),
        ],
        widget=forms.Select()
    )

    length = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Any Length'),
            ('short', 'Short'),
            ('medium', 'Medium'),
            ('long', 'Long')
        ],
        widget=forms.Select()
    )
