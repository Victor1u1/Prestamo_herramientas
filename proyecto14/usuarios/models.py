from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('El Username es obligatorio')
        if email:
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Administrador'),
        ('vecino', 'Vecino'),
    )
    
    email = models.EmailField(blank=True)  # Email no es único ni obligatorio
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='vecino')
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'  # Login con username
    REQUIRED_FIELDS = ['email']  # Email requerido solo para createsuperuser
    
    objects = UsuarioManager()
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.rol == 'admin':
            self.is_staff = True
            self.is_admin = True
        super().save(*args, **kwargs)