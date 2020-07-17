import uuid
from django.db import models
from django.utils.text import slugify

from core.models import TimestampedModel
from core.utils import generate_random_string

class Article(TimestampedModel):
  slug = models.SlugField(db_index=True, max_length=255)
  title = models.CharField(db_index=True, max_length=255)
  description = models.TextField()
  body = models.TextField()
  # Every article must have an author. This will answer questions like "Who
  # gets credit for writing this article?" and "Who can edit this article?".
  # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
  # key (or one-to-many) relationship. In this case, one `Profile` can have
  # many `Article`s.
  author = models.ForeignKey(
    'profiles.Profile', on_delete=models.CASCADE, default=1, related_name='articles'
  )

  def save(self, *args, **kwargs):
    uniqe = generate_random_string()
    self.slug = slugify(self.title) + uniqe
    super(Article, self).save(*args, **kwargs)

  def __str__(self):
    return self.title


# class Comment(TimestampedModel):
#   body = models.TextField()
#   article = models.ForeignKey(
#     'articles.Article', related_name='comments', on_delete=models.CASCADE
#   )
#   author = models.ForeignKey(
#     'profiles.Profile', related_name='comments', on_delete=models.CASCADE
#   )
