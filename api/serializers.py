from rest_framework import serializers

from .models import Photo, Thumbnail
from django.contrib.sites.shortcuts import get_current_site

current_address = "0.0.0.0:8000"


class PhotoListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('image_url', )

    def get_image_url(self, photo):

        return f"{current_address}{photo.photo.url}"


class CreatePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('photo', )

    def create(self, validated_data):
        response = []
        photo = Photo(
            photo=validated_data['photo'],
            user=self.context['request'].user
        )

        return photo


class ThumbnailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Thumbnail
        fields = ('image_url',)

    def get_image_url(self, photo):
        return f"{current_address}{photo.photo.url}"