from core.renderers import ConduitJSONRenderer


class ArticleJSONRenderer(ConduitJSONRenderer):
  object_label = 'article'
  # object_label_plural = 'articles'
  pagination_object_label = 'articles'
  pagination_count_label = 'articlesCount'


class CommentJSONRenderer(ConduitJSONRenderer):
  object_label = 'comment'
  # object_label_plural = 'comments'
  pagination_object_label = 'comments'
  pagination_count_label = 'commentsCount'