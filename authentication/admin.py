from django.contrib import admin
from authentication.models import User, SecurityQuestion, BackupRestoreBD
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin import actions
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin, SimpleHistoryAdmin):
    readonly_fields = ('email', 'created_at', 'date_joined',
                       'updated_at', 'last_login')
    list_display = ('email', 'name', 'last_name')
    list_filter = ('is_superuser', 'is_active', 'is_staff', 'is_delete')
    empty_value_display = 'No Disponible'
    ordering = ('email',)
    search_fields = ('email', 'ci')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('ci', 'name', 'last_name',)}),
        (_('Permissions'), {
         'fields': ('is_superuser', 'is_active', 'is_staff')}),
        (_('Security'), {'fields': ('uuid', 'change_pass', 'question', 'ip')}),
        (_('Imaginary Elimination'), {'fields': ('is_delete',)}),
        (_('Market Stall'), {'fields': ('role', 'level',)}),
        (_('Join'), {'fields': ('date_joined', 'created_at', 'updated_at')}),
        (_('Login'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('ci', 'name', 'last_name', 'email', 'password1', 'password2')}
         ),
        (_('Market Stall'), {'fields': ('role', 'level',)}),
        (_('Permissions'), {
         'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )


admin.site.register(SecurityQuestion, SimpleHistoryAdmin)
admin.site.register(BackupRestoreBD)
# @admin.register(BackupRestoreBD)
# class DBAdmin(admin.ModelAdmin):
#     actions = ['delete_selected']

#     def has_delete_permission(self, request, obj=None):
        
#         print("hola")
#         return True

#     def delete_selected(self, request, queryset):
#         print("hola")
#         # print("hola")
#         # print("hola")
#         # print("hola")
#         # print("hola")
#         # print("hola")
#         # print("hola")
#         # # Handle this however you like. You could raise PermissionDenied,
#         # # or just remove it, and / or use the messages framework...
#         # queryset = queryset.exclude(pk=1)

#         # actions.delete_selected(self, request, queryset)
#     delete_selected.short_description = "Delete stuff"
# # admin.site.register(BackupRestoreBD)
