from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from alfa_romeo_web.accounts.forms import AlfaRomeoUserCreationForm, AlfaRomeoChangeForm
from alfa_romeo_web.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = AlfaRomeoUserCreationForm
    form = AlfaRomeoChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date_of_birth')
    ordering = ('user_id',)
    search_fields = ('first_name', 'last_name',)
