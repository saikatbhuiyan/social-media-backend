from rest_framework import serializers

from profiles.serializers import ProfileSerializer
from .models import Article, Comment, Tag
from .relations import TagRelatedField

class ArticleSerializer(serializers.ModelSerializer):
  author = ProfileSerializer(read_only=True)
  description = serializers.CharField(required=False)
  slug = serializers.SlugField(required=False)
  tagList = TagRelatedField(many=True, required=False, source='tags')
  # Django REST Framework makes it possible to create a read-only field that
  # gets its value by calling a function. In this case, the client expects
  # `created_at` to be called `createdAt` and `updated_at` to be `updatedAt`.
  # `serializers.SerializerMethodField` is a good way to avoid having the
  # requirements of the client leak into our API.

  createdAt = serializers.SerializerMethodField('get_created_at')
  updatedAt = serializers.SerializerMethodField('get_updated_at')

  favorited = serializers.SerializerMethodField()
  favoritesCount = serializers.SerializerMethodField(
    method_name='get_favorites_count'
  )

  def get_favorited(self, obj):
    request = self.context.get('request', None)

    if request is None:
      return False

    if not request.user.is_authenticated:
      return False

    return request.user.profile.has_favorited(obj)
  
  def get_created_at(self, instance):
    return instance.created_at.isoformat()

  def get_updated_at(self, instance):
    return instance.updated_at.isoformat()

  
  def get_favorites_count(self, instance):
    return instance.favorited_by.count()

  class Meta:
    model = Article
    fields = (
      'author',
      'body',
      'description',
      'favorited',
      'favoritesCount',
      'slug',
      'title',
      'createdAt',
      'updatedAt',
      'tagList',

    )
    
    def create(self, validated_data):
      
      author = self.context.get('author', None)
      tags = validated_data.pop('tags', [])
      
      article = Article.objects.create(author=author, **validated_data)
      
      for tag in tags:
        article.tags.add(tag)
      # return Article.objects.create(author=author, **validated_data)
      return article


class CommentSerializer(serializers.ModelSerializer):
  author = ProfileSerializer(required=False)
  createdAt = serializers.SerializerMethodField(method_name='get_created_at')
  updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
  class Meta:
    model = Comment
    fields = (
      'id',
      'author',
      'body',
      'createdAt',
      'updatedAt',
    )
  def create(self, validated_data):
    article = self.context['article']
    author = self.context['author']

    return Comment.objects.create(
      author=author, article=article, **validated_data
    )

  def get_created_at(self, instance):
    return instance.created_at.isoformat()

  def get_updated_at(self, instance):
    return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):

  class Meta:
    model = Tag
    fields = ('tag',)
    
  def to_representation(self, obj):
    return obj.tag


# @property
# def popularity(self):
#     likes = self.post.count
#     time = #hours since created
#     return likes / time if time > 0 else likes
# then use a generic Field to reference it in your serializer:

# class ListingSerializer(serializers.ModelSerializer):
#     ...
#     popularity = serializers.Field(source='popularity')