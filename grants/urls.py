from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
    path('grant/<int:grant_id>/', views.detail, name='detail'),
] 