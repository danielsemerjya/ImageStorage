from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Photo
from .serializers import PhotoListSerializer, CreatePhotoSerializer
from rest_framework import permissions
from django.http import request


class ListUserPhotoView(generics.ListAPIView):

    serializer_class = PhotoListSerializer
    queryset = Photo.objects.all()


class AddPhotoView(generics.CreateAPIView):
    serializer_class = CreatePhotoSerializer
    queryset = Photo.objects.all()

    # def post(self, request, format=None):
    #     serializer = CreatePhotoSerializer(data=request.data)
    #     queryset = Photo.objects.all()
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
