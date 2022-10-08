from django.urls import path, re_path
from . import views

app_name = 'news_app'

urlpatterns = [
    path('news/', views.NewsListAPIView.as_view(), name='news_list'),
    path('roles/', views.RoleListAPIView.as_view(), name='roles_list'),
    re_path('^news/(?P<role>.+)/$', views.GetNewsByRoleAPIView.as_view(), name='news_list_by_role_API_view'),
]