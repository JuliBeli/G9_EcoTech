"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from post_app import views
from post_app import urls
from django.contrib.staticfiles.views import serve
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('post_app/', include('post_app.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path("register/", views.register_request, name="register"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("create_post/", views.create_post, name="create_post"),
    path("blog/", views.blog, name="blog"),
    path("articles/", views.articles, name="articles"),
    path('send-reset-code/', views.send_reset_code, name='send_reset_code'),
    path('verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('search/', views.search_results, name = "search_results"),
    path('focus/', views.focus, name = "focus"),
    path('like/<int:post_id>/', views.toggle_like, name = "like_post"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
