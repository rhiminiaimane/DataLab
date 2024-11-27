from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.page1, name = 'page1'),
    path('home/', views.home_page, name='home'),

    path("accounts/", include("django.contrib.auth.urls")),

    path('signup/', views.authView, name='authView')
]