from django.contrib import admin
from .models import AccountTier, Photo, TierPhotoSetting, UserTier, Thumbnail, ExpiringLink


class UserTierAdmin(admin.ModelAdmin):
    fields = ["user", "account_tier"]


class PhotoAdmin(admin.ModelAdmin):
    fields = ["user", "photo"]


class ThumbnailAdmin(admin.ModelAdmin):
    readonly_fields = ["photo", "thumbnail", "size"]


class AccountTierAdmin(admin.ModelAdmin):
    fields = ["name", "expiring_links", "original_photos"]


class TierPhotoSettingAdmin(admin.ModelAdmin):
    fields = ["tier", "img_size"]


class ExpiringLinkSettingAdmin(admin.ModelAdmin):
    fields = ["photo", "expiration_date"]


admin.site.register(UserTier, UserTierAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(TierPhotoSetting, TierPhotoSettingAdmin)
admin.site.register(ExpiringLink, ExpiringLinkSettingAdmin)

