from django.urls import path, include
from .views import ListPhotoView, AddPhotoView, CustomAuthToken, expiring_links, image_from_expiring_link
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('', get_swagger_view(title="Api v1 view"), name="swagger_view"),
    path('token_auth', CustomAuthToken.as_view(), name='token_auth'),
    path('api_auth', include('rest_framework.urls'), name="login"),
    path('list_photo', ListPhotoView.as_view(), name="list_photo"),
    path('add_photo', AddPhotoView.as_view(), name="add_photo"),
    path('expiring_links', expiring_links, name='expiring_links'),
    path('image/<str:code>', image_from_expiring_link, name='image_from_expiring_link'),
]
