from django.shortcuts import render
from rest_framework import generics, mixins
from .models import News, Role
from .serializers import NewsSerializer, RoleSerializer
from .parser import parse_news, parse_banki_ru, parse_rbc, parse_all
import time
from .process_news import process_news_and_insert


# Create your views here.
class NewsListAPIView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    # temp source
    queryset = News.objects.all()
    serializer_class = NewsSerializer

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
