
from django.urls import path, include

from .views import ListUserPhotoView, AddPhotoView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('photos_list/', ListUserPhotoView.as_view()),
    path('add_photo/', AddPhotoView.as_view()),
]
