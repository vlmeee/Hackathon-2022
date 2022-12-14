from django.shortcuts import render
from rest_framework import generics, mixins
from .models import News, Role
from .serializers import NewsSerializer, RoleSerializer
from .parser import parse_news, parse_banki_ru, parse_rbc, parse_all
import time
from .process_news import process_news_and_insert, determine_role
import random


# Create your views here.
class NewsListAPIView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        news_cnt = News.objects.count()
        start_num = random.sample(range(1, news_cnt), 1)[0]
        end_num = start_num + 3
        self.queryset = News.objects.all()[start_num:end_num]
        return self.queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoleListAPIView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GetNewsByRoleAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        role = self.kwargs['role']

        news_cnt = News.objects.count()
        start_num = random.sample(range(1, news_cnt), 1)[0]
        end_num = start_num + 3

        news_by_role = News.objects.filter(role=role)

        if len(news_by_role) < 3:
            self.queryset = News.objects.all()[start_num:end_num]
        else:
            self.queryset = news_by_role

        return self.queryset
