from rest_framework import serializers
from .models import Photo, Thumbnail, AccountTier, ExpiringLink

current_address = "0.0.0.0:8000"


class PhotoListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_id = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['image_url', 'image_id']

    def get_image_url(self, obj):
        return f"{current_address}{obj.photo.url}"

    def get_image_id(self, obj):
        return obj.id


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
        if not AccountTier.objects.filter(usertier__user=request.user)[0].original_photos:
            output.pop('photo')
        return output


class ThumbnailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thumbnail
        fields = ('url', 'size')

    def get_url(self, thumbnail):
        return f"{current_address}{thumbnail.thumbnail.url}"


class ExpiringLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = ExpiringLink
        fields = ('expiration_date', 'link')
        read_only_fields = ('photo', )

    def get_link(self, obj):
        return f"http://{current_address}/api/v1/image/{obj.code}"
