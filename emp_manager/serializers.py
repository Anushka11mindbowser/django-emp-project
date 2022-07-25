from django.utils.encoding import force_bytes
from rest_framework import serializers
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from emp_manager.utils import Util


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator.make_token(user.email)
            link = 'http://127.0.0.1:8000/reset_password_' + uid + '/' + token

            body = 'Click on the below link to reset your password'  + link + 'Link valid only for 10 minutes'
            data = {
                "Subject":"Reset Password",
                "Body" : body,
                "to:" : user.email
            }

            Util.send_email(data)

            return attrs
        else:
            raise ValueError("You are not registered")

