from rank_me_api import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import  (
    password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)

router = DefaultRouter()
router.register('profiles', views.ProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('register', views.RegisterViewSet, base_name='register')
router.register('pictures', views.PictureItemViewSet)
router.register('random_picture', views.RandomPictureItemViewSet)
router.register('grades', views.GradeItemViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^reset-password/$', password_reset, name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'^download/(?P<file_name>.+)$', 'views.download'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
