from .test_setup import TestSetUp
from ..models import Photo, Thumbnail, AccountTier, UserTier, TierPhotoSetting


class TestView(TestSetUp):

    def test_list_photo_view_GET(self):
        response = self.client.get(self.list_photo)
        self.assertEquals(response.status_code, 200)

    def test_list_photo_view_GET_no_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_photo)
        self.assertEquals(response.status_code, 403)

    def test_add_photo_view_GET(self):
        response = self.client.get(self.add_photo)
        self.assertEquals(response.status_code, 405)

    def test_add_photo_view_POST_auth_basic(self):
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Photo.objects.all().count() == 1, True)
        self.assertEquals(Thumbnail.objects.filter(photo=Photo.objects.first()).count(),
                          TierPhotoSetting.objects.filter(tier__name="Basic").count())

        self.assertEquals(len(response.data['thumb']),
                          TierPhotoSetting.objects.filter(tier__name="Basic").count())

        self.assertEquals(bool(response.data.get('photo')),
                          AccountTier.objects.filter(usertier__user__id=self.user1.id)[0].original_photos)

    def test_add_photo_view_POST_auth_premium(self):
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Premium")).save()
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Photo.objects.all().count() == 1, True)
        self.assertEquals(Thumbnail.objects.filter(photo=Photo.objects.first()).count(),
                          TierPhotoSetting.objects.filter(tier__name="Premium").count())
        self.assertEquals(len(response.data['thumb']),
                          TierPhotoSetting.objects.filter(tier__name="Premium").count())
        self.assertEquals(bool(response.data.get('photo')),
                          AccountTier.objects.filter(usertier__user__id=self.user1.id)[0].original_photos)

    def test_add_photo_view_POST_auth_enterprise(self):
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Photo.objects.all().count() == 1, True)
        self.assertEquals(Thumbnail.objects.filter(photo=Photo.objects.first()).count(),
                          TierPhotoSetting.objects.filter(tier__name="Enterprise").count())
        self.assertEquals(len(response.data['thumb']),
                          TierPhotoSetting.objects.filter(tier__name="Enterprise").count())

        self.assertEquals(bool(response.data.get('photo')),
                          AccountTier.objects.filter(usertier__user__id=self.user1.id)[0].original_photos)

    def test_add_photo_view_POST_no_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 403)

    def test_add_photo_view_POST_wrong_data(self):
        response = self.client.post(self.add_photo, data={'photo': 'uiasdb'})
        self.assertEquals(response.status_code, 400)

    def test_expiring_link_POST(self):
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.client.force_authenticate(user=self.user1)
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        response = self.client.post(self.expiring_links, data={"photo_id": photo.id,
                                                             "expiration_time": 3000})
        self.assertEquals(response.status_code, 201)

    def test_expiring_link_POST_no_auth(self):
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        self.client.force_authenticate(user=None)
        response = self.client.post(self.expiring_links, data={"photo_id": photo.id,
                                                             "expiration_time": 3000})
        self.assertEquals(response.status_code, 401)

    def test_expiring_link_POST_wrong_photo_id(self):
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.client.force_authenticate(user=self.user1)
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        response = self.client.post(self.expiring_links, data={"photo_id": 9999,
                                                             "expiration_time": 3000})
        self.assertEquals(response.status_code, 404)

    def test_expiring_link_POST_wrong_expiration_time(self):
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        self.assertEquals(response.status_code, 201)
        self.client.force_authenticate(user=self.user1)
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        response = self.client.post(self.expiring_links, data={"photo_id": photo.id,
                                                             "expiration_time": 333000})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data, {'expiration_time': '30000>=expiration_time<=300'})

    def test_expiring_link_GET(self):
        response = self.client.get(self.add_photo)
        self.assertEquals(response.status_code, 405)

    def test_image_from_expiring_link_GET(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        response = self.client.post(self.expiring_links, data={"photo_id": photo.id,
                                                             "expiration_time": 3000})
        link_from_response = response.data.get('link')
        response = self.client.get(link_from_response)
        self.assertEquals(response.status_code, 200)

    def test_image_from_expiring_link_GET_no_auth(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.add_photo, data={'photo': self.test_image})
        UserTier(id=1,
                 user=self.user1,
                 account_tier=AccountTier.objects.get(name="Enterprise")).save()
        photo = Photo.objects.first()
        response = self.client.post(self.expiring_links, data={"photo_id": photo.id,
                                                             "expiration_time": 3000})
        link_from_response = response.data.get('link')
        self.client.force_authenticate(user=None)
        response = self.client.get(link_from_response)
        self.assertEquals(response.status_code, 401)