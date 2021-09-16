from rest_framework import generics, status
from rest_framework.response import Response

from .models import Photo
from .serializers import PhotoListSerializer, CreatePhotoSerializer


class ListUserPhotoView(generics.ListAPIView):
    serializer_class = PhotoListSerializer

    def get_queryset(self):
        user = self.request.user
        return Photo.objects.filter(user=user)


class AddPhotoView(generics.CreateAPIView):
    serializer_class = CreatePhotoSerializer


