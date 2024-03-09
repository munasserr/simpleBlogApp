from django.contrib.auth.models import User
from blog.models import BlogPost
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UnicodeUsernameValidator()])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['username', 'password','password2']
        extra_kwargs = {'password': {'write_only': True}, 'password2' : {'write_only' : True}}

    def validate(self, data):
        """Validate custom conditions including password strength."""
        # Check if both passwords match
        if data.get('password') != data.pop('password2', None):
            raise serializers.ValidationError({"password": "Passwords must match."})

        # Validate the password
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']