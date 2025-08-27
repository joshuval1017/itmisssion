from django.contrib import admin
from django.contrib import admin
from .models import User, Role, ServiceRequest, AuditLog

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(ServiceRequest)
admin.site.register(AuditLog)
