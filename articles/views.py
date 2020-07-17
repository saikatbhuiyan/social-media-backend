from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Article
from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer


class ArticleViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

  queryset = Article.objects.select_related('author', 'author__user')
  permission_classes = (IsAuthenticatedOrReadOnly,)
  renderer_classes = (ArticleJSONRenderer,)
  serializer_class = ArticleSerializer

  def create(self, request):
    serializer_context = {'author': request.user.profile}
    serializer_data = request.data.get('article', {})
    serializer = self.serializer_class(
      data=serializer_data, context=serializer_context
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)