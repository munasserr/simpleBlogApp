from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import LogoutView, LoginView, PostViewSet, UserCreate

router = DefaultRouter()
router.register(r'blogposts', PostViewSet, basename='blogposts')

urlpatterns = [
    # auth
    path('api/login/', LoginView.as_view(), name='login'),


    # application
    path('', include(router.urls)),
    path('api/register/', UserCreate.as_view(), name='user_register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]