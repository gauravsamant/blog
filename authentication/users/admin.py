from django.contrib import admin
from .models import User, Email, ContactNumber

# Register your models here.

admin.site.register(User)
admin.site.register(ContactNumber)
admin.site.register(Email)
