import json
from rest_framework.renderers import JSONRenderer


# class UserJSONRenderer(JSONRenderer):
  # charset = 'utf-8'

  # def render(self, data, media_type=None, renderer_context=None):
  #   # If the view throws an error (such as the user can't be authenticated
  #   # or something similar), `data` will contain an `errors` key. We want
  #   # the default JSONRenderer to handle rendering errors, so we need to
  #   # check for this case.
  #   errors = data.get('errors', None)
  #   # If we receive a `token` key in the response, it will be a
  #   # byte object. Byte objects don't serializer well, so we need to
  #   # decode it before rendering the User object.
  #   token = data.get('token', None)

  #   if errors is not None:
  #     # As mentioned above, we will let the default JSONRenderer handle
  #     # rendering errors.
  #     return super(UserJSONRenderer, self).render(data)

  #   if token is not None and isinstance(token, bytes):
  #     # We will decode `token` if it is of type
  #     # bytes.
  #     data['token'] = token.decode('utf-8')
  #   # Finally, we can render our data under the "user" namespace.
  #   return json.dumps({
  #   'user': data
  #   })


from core.renderers import ConduitJSONRenderer


class UserJSONRenderer(ConduitJSONRenderer):
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_count_label = 'usersCount'

    def render(self, data, media_type=None, renderer_context=None):

        # If we recieve a `token` key as part of the response, it will be a
        # byte object. Byte objects don't serializer well, so we need to
        # decode it before rendering the User object.
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # Also as mentioned above, we will decode `token` if it is of type
            # bytes.
            data['token'] = token.decode('utf-8')


        return super(UserJSONRenderer, self).render(data)