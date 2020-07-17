from conduit.apps.profiles.serializers import ProfileSerializer
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
  author = ProfileSerializer(read_only=True)
  description = serializers.CharField(required=False)
  slug = serializers.SlugField(required=False)
  # Django REST Framework makes it possible to create a read-only field that
  # gets its value by calling a function. In this case, the client expects
  # `created_at` to be called `createdAt` and `updated_at` to be `updatedAt`.
  # `serializers.SerializerMethodField` is a good way to avoid having the
  # requirements of the client leak into our API.
  createdAt = serializers.SerializerMethodField(method_name='get_created_at')
  updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

  class Meta:
    model = Article
    fields = (
      'author',
      'body',
      'createdAt',
      'description',
      'slug',
      'title',
      'updatedAt',
    )
    
    def create(self, validated_data):
      author = self.context.get('author', None)
      return Article.objects.create(author=author, **validated_data)

    def get_created_at(self, instance):
      return instance.created_at.isoformat()

    def get_updated_at(self, instance):
      return instance.updated_at.isoformat()