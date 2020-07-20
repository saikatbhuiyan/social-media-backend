from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
  ArticleViewSet, 
  ArticlesFavoriteAPIView,
  CommentsListCreateAPIView, 
  CommentsDestroyAPIView,
  TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

app_name = 'articles'

urlpatterns = [
  path('', include(router.urls)),
  path('articles/<slug:article_slug>/favorite', ArticlesFavoriteAPIView.as_view()),
  path('articles/<slug:article_slug>/comments', CommentsListCreateAPIView.as_view()),
  path('articles/<slug:article_slug>/comments/<int:comment_pk>', CommentsDestroyAPIView.as_view()),
  path('tags', TagListAPIView.as_view()),
]