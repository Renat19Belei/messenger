from django.contrib import admin
from .models import User_Post,Tags,Images

# Register your models here.
admin.site.register(User_Post)
admin.site.register(Tags)
admin.site.register(Images)