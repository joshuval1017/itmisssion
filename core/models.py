from django.db import models

## core/models.py
from django.db import models

class Role(models.Model):
    RoleID = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=50)

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Mobile = models.CharField(max_length=15)
    Salt = models.CharField(max_length=64)
    PasswordHash = models.CharField(max_length=128)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(auto_now_add=True)

class ServiceRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    ServiceType = models.CharField(max_length=100)
    Description = models.TextField()
    FeeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Action = models.CharField(max_length=255)
    Timestamp = models.DateTimeField(auto_now_add=True)


import hashlib, os
from django.db import models

class Citizen(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    salt = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=64)
    role = models.CharField(max_length=20, default='Citizen')

    def set_password(self, raw_password):
        self.salt = os.urandom(32).hex()
        self.password_hash = hashlib.sha256((self.salt + raw_password).encode()).hexdigest()
