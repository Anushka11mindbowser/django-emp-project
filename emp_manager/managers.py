from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        return user

    def create_employee(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', False)
        extra_fields.setdefault('is_employee', True)

        return self.create_user(email, password, **extra_fields)

    def create_manager(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_employee', True)

        return self.create_user(email,password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_employee', True)



        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must be active')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be set to True')

        return self.create_user(email, password, **extra_fields)

