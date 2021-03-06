from django.contrib.auth.models import User
from io import BytesIO
import os
from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import string
import random


class AccountTier(models.Model):
    """
    Model storing all available Tiers
    """
    name = models.CharField(max_length=20, null=False, blank=False, unique=True)
    expiring_links = models.BooleanField(default=False)
    original_photos = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TierPhotoSetting(models.Model):
    """
    Model storing thumbnail img_sizes available for every Tier
    """
    tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    img_size = models.PositiveSmallIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.tier.name} : available thumb size: {self.img_size} "


class UserTier(models.Model):
    """
    Model link user with their tiers
    """
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.user.username}: {self.account_tier}"


@receiver(post_save, sender=User)
def create_tier(sender, instance, created, **kwargs):
    if created:
        tier = AccountTier.objects.get(name="Basic")
        UserTier.objects.create(user=instance, account_tier=tier)


class Photo(models.Model):

    """
    Photo model with automatically generated Thumbnail by TierPhotoSetting of UserTier
    """
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', blank=False, null=False)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(Photo, self).save(*args, **kwargs)
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')

    def make_thumbnail(self):
        # Get user settings
        user_tier = UserTier.objects.get(user=self.user)
        setting = TierPhotoSetting.objects.filter(tier=user_tier.account_tier)

        for size in setting:

            THUMB_SIZE = (size.img_size, size.img_size)

            image = Image.open(self.photo)
            image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

            thumb_name, thumb_extension = os.path.splitext(self.photo.name)
            thumb_extension = thumb_extension.lower()

            thumb_filename = thumb_name + '_thumb' + thumb_extension

            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False    # Unrecognized file type

            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            new_thumbnail = Thumbnail(photo=self, size=size.img_size)
            new_thumbnail.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)

        return True


class Thumbnail(models.Model):
    """
    Thumbnail storing
    """
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, editable=False)
    size = models.PositiveSmallIntegerField(blank=False, null=False, editable=False)
    thumbnail = models.ImageField(upload_to='thumbs', blank=False, null=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def generate_unique_code():
    length=15
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if not ExpiringLink.objects.filter(code=code).exists():
            break
    return code


class ExpiringLink(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=False, blank=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    code = models.CharField(max_length=15, default=generate_unique_code, unique=True)
