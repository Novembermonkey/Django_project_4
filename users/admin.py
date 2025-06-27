from django.contrib import admin

# Register your models here.
from django.contrib import admin
from users.models import CustomUser, Role
from django.contrib.auth.admin import UserAdmin
from .forms import  CustomUserChangeForm, CustomUserCreationForm


# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_count']

    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'




class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_staff', 'is_superuser']

    fieldsets = [
        (None, {'fields': ('email', 'username', 'password')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
        ('Profile Picture', {'fields': ('profile_pic',)})
    ]
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'role')}
        ),
    ]
    search_fields = ['email', 'username',]
    ordering = ['email',]

admin.site.register(CustomUser, CustomUserAdmin)