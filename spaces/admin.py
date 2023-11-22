from django.contrib import admin

# Register your models here.

from .models import Space, File

admin.site.register(Space)
admin.site.register(File)
