from django.contrib import admin
from .models import *

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]
    search_fields = [field.name for field in UserProfile._meta.fields]
    list_filter = [field.name for field in UserProfile._meta.fields]

admin.site.register(UserProfile, UserProfileAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Role._meta.fields]
    search_fields = [field.name for field in Role._meta.fields]
    list_filter = [field.name for field in Role._meta.fields]

admin.site.register(Role, RoleAdmin)


class NetworkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Network._meta.fields]
    search_fields = [field.name for field in Network._meta.fields]
    list_filter = [field.name for field in Network._meta.fields]

admin.site.register(Network, NetworkAdmin)


class DeviceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Device._meta.fields]
    search_fields = [field.name for field in Device._meta.fields]
    list_filter = [field.name for field in Device._meta.fields]

admin.site.register(Device, DeviceAdmin)


class IssueLogMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IssueLogMessage._meta.fields]
    search_fields = [field.name for field in IssueLogMessage._meta.fields]
    list_filter = [field.name for field in IssueLogMessage._meta.fields]

admin.site.register(IssueLogMessage, IssueLogMessageAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]
    search_fields = [field.name for field in Status._meta.fields]
    list_filter = [field.name for field in Status._meta.fields]

admin.site.register(Status, StatusAdmin)

class NetTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NetType._meta.fields]
    search_fields = [field.name for field in NetType._meta.fields]
    list_filter = [field.name for field in NetType._meta.fields]

admin.site.register(NetType, NetTypeAdmin)

class IssueTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IssueType._meta.fields]
    search_fields = [field.name for field in IssueType._meta.fields]
    list_filter = [field.name for field in IssueType._meta.fields]

admin.site.register(IssueType, IssueTypeAdmin)


