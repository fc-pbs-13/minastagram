from django.contrib import admin
from users.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'date_joined', 'email', 'is_staff', 'is_active']
    search_fields = ['username', ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'introduce',]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
