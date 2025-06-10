from django.contrib import admin
from .models import User_Post,Tags,Images,Profile,CustomUser
from django.contrib.auth.admin import UserAdmin 

# Register your models here.
admin.site.register(User_Post)
admin.site.register(Tags)
admin.site.register(Images)
admin.site.register(Profile)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass