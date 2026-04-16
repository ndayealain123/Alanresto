from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Home, name="home"),
    path('menu/', Menuview, name="menu"),
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', decrease_quantity, name='decrease_quantity'),
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