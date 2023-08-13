from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.models import Session
from django.utils import timezone
from account_app.forms import UserChangeForm, UserCreationForm
from account_app.models import Ban, User, Otp


@admin.action(description='مسدود سازی کاربر')
def ban_user(modeladmin, request, queryset):
    for user in queryset:
        if user.is_authenticated:
            for session in Session.objects.filter(
                    expire_date__gte=timezone.now()
            ):
                session_data = session.get_decoded()
                auth_user_id = session_data.get('_auth_user_id')
                if auth_user_id and user.id == int(auth_user_id):
                    session.delete()

        Ban.objects.create(user=user)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "email", "is_admin", "fullname", "created_at", "is_active"]
    list_filter = ["is_admin", "phone"]
    actions = [ban_user, ]
    fieldsets = [
        (None, {"fields": ["email", "password", 'phone', 'image', 'birthday', 'sex']}),
        ("اطلاعات کاربری", {"fields": ["fullname"]}),
        ("دسترسی ها", {"fields": ["is_admin", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", 'phone', "fullname", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", ]
    ordering = ["email", ]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.register(Ban)
admin.site.register(Otp)
