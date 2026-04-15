from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home, name="home"),
    path('menu/', Menuview, name="menu"),
    path('register/', register_profil, name='register'),
    path('create_order/<int:pk>/', Create_order, name='new_order'),
    path('login/', connexion, name='connect'),
    path('deconnexion/', deconnexion, name='deconnect'),
    path('order/', orderview, name='order'),
    path('about/', aboutview, name="about"),
    path('finish/<int:pk>/', finishOrder, name="finished"),
    path('receive/<int:pk>/', receiveOrder, name="received"),
]

# Serve uploaded media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)