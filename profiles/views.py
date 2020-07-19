from rest_framework import status, serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from .exceptions import ProfileDoesNotExist

class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        # Try to retrieve the requested profile and throw an exception if the
        # profile could not be found.
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            # profile = Profile.objects.select_related('user').get(
            #     user__username=username
            # )
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            # raise ProfileDoesNotExist
            raise NotFound(f'A profile with this {username} does not exist.')

        # serializer = self.serializer_class(profile)
        serializer = self.serializer_class(profile, context={'request': request})
        # In the changes we just made to the serializer, you may have noticed that
        # we’re looking for the request object inside the serializer. This change to
        # ProfileRetrieveAPIView is how we can do that
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def delete(self, request, username=None):
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username=None):
        follower = self.request.user.profile
        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')
        if follower.pk is followee.pk:
            raise serializers.ValidationError('You can not follow yourself.')

        follower.follow(followee)
        serializer = self.serializer_class(followee, context={
            'request': request
        })
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
