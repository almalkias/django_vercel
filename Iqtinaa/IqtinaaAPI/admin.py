from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Paint, UserProfile, FavouritePaint, Cart

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'telephone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'telephone'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Paint)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(FavouritePaint)