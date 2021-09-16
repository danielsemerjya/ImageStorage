from rest_framework import serializers
from .models import Photo, Thumbnail, AccountTier, UserTier

current_address = "0.0.0.0:8000"


class PhotoListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('image_url', )

    def get_image_url(self, photo):
        return f"{current_address}{photo.photo.url}"


class CreatePhotoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('photo', 'user', 'thumb')

    def get_thumb(self, photo):
        thumbs = Thumbnail.objects.filter(photo=photo)
        thumb = ThumbnailSerializer(thumbs, many=True).data
        return thumb

    def to_representation(self, instance):
        output = super(CreatePhotoSerializer, self).to_representation(instance)
        request = self.context.get('request')
        basic_tier = AccountTier.objects.get(name="Basic")
        user_tier = UserTier.objects.filter(user=request.user, account_tier=basic_tier).exists()
        if user_tier:
            output.pop('photo')
        return output


class ThumbnailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thumbnail
        fields = ('url', 'size')

    def get_url(self, thumbnail):
        return f"{current_address}{thumbnail.thumbnail.url}"
