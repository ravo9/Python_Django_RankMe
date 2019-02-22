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
from rank_me_project import settings
from wsgiref.util import FileWrapper


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


class ResetPasswordViewSet(viewsets.ViewSet):

    def csrf_exempt(view_func):
        """Marks a view function as being exempt from the CSRF view protection."""
        def wrapped_view(request,*args, **kwargs):
            return view_func(request, *args, **kwargs)
            if request.META.has_key('HTTP_X_SKIP_CSRF'):
                wrapped_view.csrf_exempt = True
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


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
        # Get all grades given by this user.
        pictures_already_graded = GradeItem.objects.all().filter(grading_profile=self.request.user)

        # Filter out own photos.
        filtered_queryset = self.queryset.filter(~Q(profile=self.request.user))

        for grade in pictures_already_graded:
            filtered_queryset = filtered_queryset.filter(~Q(id=grade.picture.id))
            #filtered_queryset = filtered_queryset.filter(~Q(profile=grade.grading_profile))
        #random_picture = random.choice(filtered_queryset)
        #return [random_picture]
        #filtered_queryset_ids = []
        #for picture in filtered_queryset:
            #filtered_queryset_ids.append(picture.id)
        return filtered_queryset


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

def download(request,file_name):
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response
