from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import MyUser
from users.forms import UserChangeForm, UserCreationForm


@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'nickname', 'is_admin', 'join_date')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'nickname', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'nickname')
    ordering = ('email',)
    filter_horizontal = ()