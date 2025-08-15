from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
import uuid


def validate_panjang_id_satker(value):
    if len(value) != 15:
        raise ValidationError("id_satker harus tepat 10 karakter.")


class UserManager(BaseUserManager):
    def create_user(self, nip, password=None, **extra_fields):
        if not nip:
            raise ValueError("The NIP field must be set")
        user = self.model(nip=nip, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nip, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(nip, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    id_satker = models.CharField(max_length=15, null=True, blank=True)
    nip = models.CharField(max_length=50, unique=True)
    nama = models.CharField(max_length=100)
    pangkat = models.CharField(max_length=50, null=True, blank=True)
    jabatan = models.CharField(max_length=50, null=True, blank=True)
    anggota = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    mode_ubah_jabatan = models.BooleanField(default=False)
    mode_purnatugas = models.BooleanField(default=False)
    id_satker_tag = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "nip"
    REQUIRED_FIELDS = ["nama", "pangkat", "jabatan"]

    def __str__(self):
        return self.nip

    def get_groups(self):
        return ", ".join([group.name for group in self.groups.all()])
    
    class Meta:
        indexes = [
            models.Index(fields=['id', 'created_at']),
        ]
