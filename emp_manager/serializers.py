from rest_framework import serializers
from .models import User


class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        default_error_message = {
            "message": "Only Manager is eligible to create an employee"
        }

        def create(self, validated_data):
            if validated_data['is_superuser'] == True and validated_data['is_manager'] == False:
                new_user = User.objects.create_superuser(**validated_data)
                return new_user
            elif validated_data['is_superuser'] == False and validated_data['is_manager'] == True:
                new_user = User.objects.create_manager(**validated_data)
                return new_user
            else:
                self.fail("Not Authorized")


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__fields__'


class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'mob', 'first_name', 'last_name', 'is_superuser', 'is_manager', 'is_employee',
                  'is_staff']


class RegisterEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'mob', 'first_name', 'last_name']

        def create(self, validated_data):
            random_password = User.objects.make_random_password(9)
            print("New Password", random_password)
            new_employee = User.objects.create_employee(**validated_data, password=random_password)
            return new_employee


