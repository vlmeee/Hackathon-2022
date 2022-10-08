from django.shortcuts import render
from rest_framework import generics, mixins
from .models import News, Role
from .serializers import NewsSerializer, RoleSerializer
from .parser import parse_news, parse_banki_ru, parse_rbc


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
        rbc = parse_rbc()

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
