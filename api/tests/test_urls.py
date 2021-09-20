from django.test import SimpleTestCase
from django.urls import reverse, resolve

from api.tests.test_setup import TestSetUp
from api.views import ListPhotoView, AddPhotoView


class TestUrls(TestSetUp):

    def test_photos_list_url_resolves(self):
        self.assertEquals(resolve(self.list_photo).func.view_class, ListPhotoView)

    def test_add_photo_url_resolves(self):
        self.assertEquals(resolve(self.add_photo).func.view_class, AddPhotoView)
