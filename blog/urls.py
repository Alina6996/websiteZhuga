from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('post/<slug:slug>', views.post, name="post"),
    path('category/<slug:slug>/', views.category, name="category"),
    path('search/', views.search, name="search"),
    path('create/', views.create, name="create"),
    path('login/', LoginView.as_view(), name='blog_login'),
    path('logout/', LogoutView.as_view(next_page='blog_login'), name='blog_logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
