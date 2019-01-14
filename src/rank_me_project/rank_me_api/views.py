import random
from django.db.models import Q
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import PictureItem, GradeItem, UserProfile
from .serializers import PictureItemSerializer, GradeItemSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly, UpdateOwnProfile, UpdateOwnPicture, ReadOnly
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# Viewset req.
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class        = ProfileSerializer
    queryset                = UserProfile.objects.all()

    def get_queryset(self):
        return []


class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    authentication_classes  = []
    permission_classes = []
    # POST Method. We are calling the APIView through the ViewSet.
    def create(self, request):
        response = ObtainAuthToken().post(request)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class ProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class        = ProfileSerializer
    queryset                = UserProfile.objects.all()
    # Authentication stuff.
    authentication_classes  = (TokenAuthentication,)
    permission_classes      = (IsAuthenticated, UpdateOwnProfile,)
    # Searching feature stuff
    filter_backends         = (filters.SearchFilter,)
    search_fields           = ('name', 'email',)


class PictureItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = PictureItemSerializer
    queryset = PictureItem.objects.all()
    permission_classes = (UpdateOwnPicture, IsAuthenticated)

    # Searching feature stuff
    filter_backends = (filters.SearchFilter,)
    search_fields = ('profile__id',)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'http_method': 'DELETE'})


class RandomPictureItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = PictureItemSerializer
    queryset = PictureItem.objects.all()
    permission_classes = (UpdateOwnPicture, IsAuthenticated)

    def get_queryset(self):
        #random_picture = random.choice(self.queryset)
        #return [random_picture]

    def get_queryset(self, user_id):

        random_picture = random.choice(self.queryset)
        if (random_picture.id == user_id) random_picture = get_queryset(self, user_id)
        return [random_picture]


class GradeItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = GradeItemSerializer
    queryset = GradeItem.objects.all()
    permission_classes = (IsAuthenticated, ReadOnly)

    # Searching feature stuff
    filter_backends = (filters.SearchFilter,)
    search_fields = ('picture__profile__id',)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
