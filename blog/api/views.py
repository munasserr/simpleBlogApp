from blog.models import Post
from .serializers import PostSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                data = serializer.data
                data['token'] = token.key  
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            })
        else:
            return Response({"error": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"detail": "An error occurred."}, status=status.HTTP_400_BAD_REQUEST)