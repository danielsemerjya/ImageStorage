from django.contrib import admin

# Register your models here.

from .models import AccountTier, Photo, TierSetting, UserTier, Thumbnail


class UserTierAdmin(admin.ModelAdmin):
    fields = ["user", "account_tier"]


class PhotoAdmin(admin.ModelAdmin):
    fields = ["user", "photo"]


class ThumbnailAdmin(admin.ModelAdmin):
    readonly_fields = ["photo", "thumbnail", "size"]


class AccountTierAdmin(admin.ModelAdmin):
    fields = ["name"]


class TierSettingAdmin(admin.ModelAdmin):
    fields = ["tier", "img_size"]


admin.site.register(UserTier, UserTierAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(TierSetting, TierSettingAdmin)

