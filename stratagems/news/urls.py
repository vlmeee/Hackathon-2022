from django.urls import path
from . import views

app_name = 'news_app'

urlpatterns = [
    path('news/', views.NewsListAPIView.as_view(), name='news_list'),
    path('roles/', views.RoleListAPIView.as_view(), name='roles_list'),
]