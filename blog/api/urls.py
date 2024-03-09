from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, UserCreate

router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet, basename='blogposts')

urlpatterns = [
    # auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # application
    path('', include(router.urls)),
    path('api/register/', UserCreate.as_view(), name='user_register'),
]