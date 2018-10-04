from rank_me_api import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
