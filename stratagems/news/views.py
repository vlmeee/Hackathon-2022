from django.shortcuts import render
from rest_framework import generics, mixins
from .models import News, Role
from .serializers import NewsSerializer, RoleSerializer
from .parser import parse_news, parse_banki_ru, parse_rbc, parse_all
import time
from .process_news import process_news_and_insert
import random


# Create your views here.
class NewsListAPIView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    # temp source

    serializer_class = NewsSerializer

    def get_queryset(self):
        news_cnt = News.objects.count()
        start_num = random.sample(range(1, news_cnt), 1)[0]
        end_num = start_num + 3
        self.queryset = News.objects.all()[start_num:end_num]
        return self.queryset

    def get(self, request, *args, **kwargs):
        # Maybe magic will happen here?

        # parsing_result = parse_news()
        # banki_ru = parse_banki_ru(True)
        # rbc = parse_rbc()
        t0 = time.time()
        # parse_all_res = parse_all()
        # process_news_and_insert()
        # print(parse_all_res)
        # news_count = len(parse_all_res)
        # print('News count: ', news_count)
        t1 = time.time() - t0
        print("Time elapsed, s: ", t1)
        # print('News per time, s: ', t1/news_count)


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
        return News.objects.filter(role=role)
