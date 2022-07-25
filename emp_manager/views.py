from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (GenericAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework.permissions import (
                                        IsAuthenticated,
                                        AllowAny
                                        )
from .serializers import (RegisterSerializer,
                          LoginSerializer,
                          PasswordSerializer,
                          SendEmailSerializer
                          )
from rest_framework import status
from .models import User




# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),

    }

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            response = {
                'token':token,
                'message':'User Registered Successfully',
                'data': serializer.data
            }
            return Response(response, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is None:
                token = get_tokens_for_user(user)

                response = {
                    "token": token,
                    "message": "Login Successful",
                    "data": serializer.data
                    }

                return Response(response, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class EmployeeRegister(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_manager == True or user.is_superuser == True:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message":"Employee created",
                    "data": serializer.data
                }
                return Response(response, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response("You are not authorized to create an employee", status.HTTP_401_UNAUTHORIZED)


class UpdateProfile(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_object(self,pk):
        return User.objects.get(pk=pk)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"Profile Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
class RetrieveProfile(RetrieveAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self, pk):
        return User.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        profile = self.get_object(pk)
        serializer = RegisterSerializer(profile, many=False)
        response = {
            "message": "Profile",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

#

class ProfileList(ListAPIView):
    model = User
    serializer_class = RegisterSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = RegisterSerializer(users, many=True)
        response = {
            "message": "Profile List",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

class ChangePassword(UpdateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]


    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = request.user.id
            user = User.objects.get(id=id)
            user.set_password(request.data['password'])
            user.save()
            response = {
                "message": "Password Changed Successfully",
                "changedPassword": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendResetPasswordView(GenericAPIView):
    serializer_class = SendEmailSerializer
    permission_classes = []
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {
                "message":"Email Sent"
            }
            return Response(response, status.HTTP_200_OK)
        else:
            return (serializer.errors, status.HTTP_400_BAD_REQUEST)

class UserLogout(GenericAPIView):


    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"Success"
        }
        return response









