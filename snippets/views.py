from django.shortcuts import render
from .serializers import SnippetSerializer
from .models import Snippet
from rest_framework import viewsets
from rest_framework.response import Response


class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
