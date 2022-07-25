from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(" Valid Email is required")
        if not password:
            raise ValueError("Valid Password is required")

        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_employee", False)

        return self.create_user(email, password, **extra_fields)

    def create_manager(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_manager", True)
        extra_fields.setdefault("is_employee", False)

        return self.create_user(email, password, **extra_fields)

    def create_employee(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_employee", True)

        return self.create_user(email, password, **extra_fields)

