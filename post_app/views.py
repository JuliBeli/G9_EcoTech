# Create your views here.

from datetime import datetime
from idlelib.query import Query

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.db.models.functions import Lower
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from datetime import timedelta
from django.views.decorators.cache import never_cache
from rest_framework.renderers import JSONRenderer

from post_app.forms import CustomAuthenticationForm, CustomUserCreationForm, PostForm, SearchFilterForm
from post_app.models import PostRaw

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import PasswordResetCode, PostRaw
from .services.email_service import EmailService
from django.shortcuts import get_object_or_404
from . import global_trie


@login_required()
def post_detail(request, post_id):
    post = get_object_or_404(PostRaw, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

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
    latest_articles = PostRaw.objects.filter(post_type=1).order_by('-created_at')[:4]  # Get 4 posts created by admin with the latest created time
    featured_articles = PostRaw.objects.filter(post_type=1).order_by('-likes_int')[:4]  # Get 4 posts created by admin with the most likes
    return render(request, 'index.html', {'latest_articles': latest_articles,
                                                    'featured_articles':featured_articles})

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
                return redirect('index')
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

# create new post page
@login_required
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
@login_required
def blog(request):
    posts = PostRaw.objects.filter(post_type=2).order_by('-created_at')
    return render(request, 'blog.html', {'posts': posts})

# Display all posts created by admin
@login_required
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

# View to recommand the articles
def search_suggestions(request):
    query = request.GET.get("q", "").strip().lower()
    if not query:
        return JsonResponse({"suggestions": []})
    matches = global_trie.trie.starts_with(query)
    print("Matches: ", matches)
    posts = PostRaw.objects.annotate(lower_title = Lower("title")).filter(lower_title__in = matches)
    print("Posts: ", posts)
    suggestions = [
        {"id": post.id, "title": post.title}
        for post in posts
    ]

    return JsonResponse({"suggestions": suggestions})

# View to search the Article with filters
def search_results(request):
    if request.method == "GET":
        form = SearchFilterForm(request.GET or None)
        if form.is_valid():
            q = form.cleaned_data["q"] # since the query is a going to be given by the user we are not using .get
            post_type = form.cleaned_data.get("post_type")
            author = form.cleaned_data.get("author")
            date_range = form.cleaned_data.get('date_range')
            # start_date = form.cleaned_data.get('start_date')
            # end_date = form.cleaned_data.get('end_date')
            sort_choice = form.cleaned_data.get('sort')
            length = form.cleaned_data.get('length')
            posts = QuerySet()
            if q:
                title_qs = PostRaw.objects.filter(title__icontains=q)
                content_qs = PostRaw.objects.filter(content__icontains=q)
                print("Title_qs: ", title_qs.values())
                print("content_qs: ", content_qs.values())
                # posts = title_qs.union(content_qs)

                if post_type:
                    title_qs = title_qs.filter(post_type = post_type)
                    content_qs = content_qs.filter(post_type = post_type)

                if author:
                    title_qs = title_qs.filter(author__username__icontains = author)
                    content_qs = content_qs.filter(author__username__icontains = author)

                if date_range:
                    now = timezone.now()
                    date_threshold = None
                    if date_range == "1d":
                        date_threshold = now - timedelta(days = 1)
                    elif date_range == "7d":
                        date_threshold = now - timedelta(days = 7)
                    elif date_range == "1m":
                        date_threshold = now - timedelta(days = 30)
                    elif date_range == "1y":
                        date_threshold = now - timedelta(days = 365)

                    if date_threshold:
                        title_qs = title_qs.filter(created_at__gte = date_threshold)
                        content_qs = content_qs.filter(created_at__gte = date_threshold)

                posts = title_qs.union(content_qs)
                if sort_choice == "recent":
                    posts = posts.order_by("-created_at")
                elif sort_choice == "oldest":
                    posts = posts.order_by("created_at")
                elif sort_choice == "likes_desc":
                    posts = posts.order_by("-likes_int")
                elif sort_choice == "likes_asc":
                    posts = posts.order_by("likes_int")
                if length:
                    def get_length(p):
                        l = len(p.content)
                        if l < 500:
                            return 'short'
                        elif l < 1500:
                            return 'medium'
                        else:
                            return 'long'
                    posts = [p for p in posts if get_length(p) == length]



            return render(request, 'results.html', {"posts": posts, "form":form})
        else:
            form = SearchFilterForm()
            return render(request, "results.html", {"form": form})
    else:
        form = SearchFilterForm()
        return render(request, "results.html", {"form": form})
