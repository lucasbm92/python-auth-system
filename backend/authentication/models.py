from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)  # Flask password hashes
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email for login
    REQUIRED_FIELDS = ['username']  # Required for createsuperuser

    class Meta:
        db_table = 'user'  # Use existing Flask table

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        """
        Check password - compatible with both Flask/Werkzeug and Django hashes
        """
        from django.contrib.auth.hashers import check_password as django_check_password
        
        # First try Django's password checking
        if django_check_password(raw_password, self.password):
            return True
        
        # If Django check fails, try Flask/Werkzeug password checking
        try:
            # Flask uses Werkzeug's security functions
            # The hash format is usually: method$salt$hash
            if self.password.startswith('pbkdf2:'):
                # Werkzeug PBKDF2 format
                from werkzeug.security import check_password_hash
                return check_password_hash(self.password, raw_password)
            elif self.password.startswith('scrypt:') or self.password.startswith('sha256:'):
                # Other Werkzeug formats
                from werkzeug.security import check_password_hash
                return check_password_hash(self.password, raw_password)
            else:
                # Fallback: might be a simple hash, try werkzeug anyway
                from werkzeug.security import check_password_hash
                return check_password_hash(self.password, raw_password)
        except ImportError:
            # Werkzeug not available, fall back to simple comparison
            print("⚠️  Werkzeug not available, trying basic comparison")
            return False
        except Exception as e:
            print(f"⚠️  Password verification failed: {e}")
            return False

    def set_password(self, raw_password):
        """Set password using Django's hasher for new passwords"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    # Required methods for Django admin
    def has_perm(self, perm, obj=None):
        return False  # No special permissions for now
    
    def has_module_perms(self, app_label):
        return False  # No special permissions for now
