from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.page1, name = 'page1'),
    path('home/', views.home_page, name='home'),

    path("accounts/", include("django.contrib.auth.urls")),

    path('signup/', views.authView, name='authView'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('upload/', views.upload_file, name='upload_file'),
    path('create/', views.create_dataset, name='create_dataset'),
    path('export/', views.export_dataset, name='export_dataset'),
    path('upload_and_display/', views.upload_and_display, name='upload_and_display'),
]