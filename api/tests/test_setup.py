from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import AccountTier, TierPhotoSetting
from pathlib import Path


class TestSetUp(APITestCase):

    def setUp(self):

        self.tier1 = AccountTier.objects.create(
            name="Basic"
        )
        self.tier2 = AccountTier.objects.create(
            name="Premium",
            original_photos=True
        )
        self.tier3 = AccountTier.objects.create(
            name="Enterprise",
            expiring_links=True,
            original_photos=True
        )

        TierPhotoSetting.objects.create(tier=self.tier1, img_size=200)
        TierPhotoSetting.objects.create(tier=self.tier2, img_size=200)
        TierPhotoSetting.objects.create(tier=self.tier2, img_size=400)
        TierPhotoSetting.objects.create(tier=self.tier3, img_size=200)
        TierPhotoSetting.objects.create(tier=self.tier3, img_size=400)

        self.username = "user123"
        self.password = "password321"

        self.user1 = User.objects.create(
            username=self.username,
            email="user@user.user",
            password=self.password
        )

        self.token = Token.objects.get(user__username=self.username)
        self.api_authentication()

        self.list_photo = reverse('list_photo')
        self.add_photo = reverse('add_photo')
        self.expiring_links = reverse('expiring_links')

        self.test_image = open(Path('api/tests/cat.png'), 'rb')

        return super().setUp()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

