import datetime
from django.db.models import Q
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .models import Photo, ExpiringLink, AccountTier
from .serializers import PhotoListSerializer, CreatePhotoSerializer, ExpiringLinkSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class ListPhotoView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = PhotoListSerializer

    def get_queryset(self):
        user = self.request.user
        return Photo.objects.filter(user=user)


class AddPhotoView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = CreatePhotoSerializer


@api_view(['POST'])
def expiring_links(request):
    acc_tier = get_object_or_404(AccountTier, usertier__user=request.user)
    if acc_tier.expiring_links:
        if request.method == "POST":
            if request.data.get('photo_id') and request.data.get('expiration_time'):
                if 30000 >= int(request.data.get('expiration_time')) >= 3000:
                    pk = request.data.get('photo_id')
                    photo = get_object_or_404(Photo, pk=pk, user=request.user)
                    expiration_time = request.data.get('expiration_time')
                    if expiration_time.isnumeric():
                        if 30000 > int(expiration_time) > 300:
                            expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(expiration_time))
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'expiration_time': '30000>=expiration_time<=300'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'request should include': 'expiration_time, photo_id'})
            expiring_link = ExpiringLink.objects.create(photo=photo, expiration_date=expiration_date)
            serializer = ExpiringLinkSerializer(expiring_link)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def image_from_expiring_link(request, code):
    " Display photo from expiring link"
    if request.method == "GET":
        expiring_link = ExpiringLink.objects.filter(Q(code=code), Q(expiration_date__gte=datetime.datetime.now()))
        if expiring_link.count() > 0:
            response = FileResponse(expiring_link[0].photo.photo)
            return response
    return Response(status=status.HTTP_404_NOT_FOUND)
