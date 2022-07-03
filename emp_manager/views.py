from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import (GenericAPIView,
                                     CreateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import (RegisterationSerializer,
                          LoginSerializer,
                          BasicSerializer,
                          RegisterEmployeeSerializer)
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .renderers import UserRenderers

# Create your views here.
class RegisterSuperUser(CreateAPIView):
    serializer_class = RegisterationSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        print(request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            response = {
            "message":"Superuser created successfully",
            "Data":serializer.data
            }

            return Response(response, status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

class Login(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        print(request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email,password=password)

            if user is not None:
                response = {
                    "message":"Login Successful",
                    "user":email
                }
                return Response(response, status.HTTP_200_OK)
            else:
                response = {
                    "msg":"Login Unsuccessful"
                }
                return Response(response,status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserList(ListAPIView):
    serializer_class = [BasicSerializer]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_manager==True:
            employees = User.objects.filter(is_staff=True)
            serializer = self.serializer_class(employees, many=True)
            response = {
                "message":"List of employees",
                "Employees":serializer.data
                }
            return Response(response, status.HTTP_200_OK)
        else:
            response = {
                "message":"You are not authorized to see this list"
            }
            return Response(response, status.HTTP_401_UNAUTHORIZED)


class EmployeeProfile(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = BasicSerializer
        return Response(serializer.data, status.HTTP_200_OK)

class EmployeeRegisteration(CreateAPIView):
    serializer_class = RegisterEmployeeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_manager == True:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message":"Employee Registered Successfully",
                    "data": serializer.data
                }
                return Response(response, status.HTTP_201_CREATED)
            else:
                response = {
                    "msg":"Could not register the Employee"
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)


# class ChangePassword(APIView):
#     renderer_classes = [UserRenderers]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, format=None):
#         serializers = serial.ChangedPasswordSerializer(
#             data=request.data, context={'user': request.user})
#         if serializers.is_valid(raise_exception=True):
#             return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
#
#         return Response(serializers.errrors, status=status.HTTP_404_NOT_FOUND)
#
# class ForgotPassword(APIView):
#     renderer_classes = [UserRenderers]
#
#     def post(self, request, format=None):
#         serializers = serializers.ForgotPasswordSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             return Response({'msg': 'Password Reset link sent'}, status=status.HTTP_200_OK)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class ResetPassword(APIView):
#     renderer_classes = [UserRenderers]
#
#     def post(self, request, uid, token, format=None):
#         serializers = serializer.ResetPasswordSerializer(data=request.data, context={
#             'uid': uid, 'token': token})
#         if serializers.is_valid(raise_exception=True):
#             return Response({'msg': 'Password is  Reset successfully'}, status=status.HTTP_200_OK)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
