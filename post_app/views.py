# Create your views here.

from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from rest_framework.renderers import JSONRenderer

from post_app.forms import CustomAuthenticationForm, CustomUserCreationForm, PostForm
from post_app.models import PostRaw

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import PasswordResetCode
from .services.email_service import EmailService

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

@never_cache
def index(request):
    # context = {
    #     'version': datetime.now().strftime('%Y%m%d%H%M%S'),  # Use the current date and time as the version number
    #     'user': request.user
    # }
    # return render(request, 'index.html', context)
    return render(request, 'index.html')

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

# about us page
def about(request):
    return render(request, 'about.html')

#contact us page
def contact(request):
    return render(request, 'contact.html')

#reset password page
def reset(request):
    return render(request, 'reset.html')

# main page after login
@never_cache
@login_required
def main(request):
    context = {
        'version': datetime.now().strftime('%Y%m%d%H%M%S'),  # Use the current date and time as the version number
        'user': request.user
    }
    return render(request, 'main.html', context)
    # return render(request, 'index.html')

# create new post page
# @login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# Display all posts created by user
def blog(request):
    posts = PostRaw.objects.filter(post_type=2).order_by('-created_at')
    return render(request, 'blog.html', {'posts': posts})

# Display all posts created by admin
def articles(request):
    posts = PostRaw.objects.filter(post_type=1).order_by('-created_at')
    return render(request, 'articles.html', {'posts': posts})

#send verification code
def send_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # generate verification code
            code = PasswordResetCode.generate_code()

            # save verification code
            reset_code = PasswordResetCode.objects.create(
                user=user,
                code=code
            )

            # send email
            if EmailService.send_password_reset_code(user, code):
                messages.success(request, 'The verification code has been sent to your email')
                return redirect('verify_reset_code')
            else:
                messages.error(request, 'Failed to send verification code; please try again later')

        except User.DoesNotExist:
            messages.error(request, 'This email is not registered')

    return render(request, 'send_reset_code.html')

#verify reset code
def verify_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).first()

            if reset_code and not reset_code.is_expired():
                # update password
                user.password = make_password(new_password)
                user.save()

                # Mark verification code as used
                reset_code.is_used = True
                reset_code.save()

                messages.success(request, 'Password reset success')
                return redirect('login')
            else:
                messages.error(request, 'The verification code is invalid or expired')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'verify_reset_code.html')