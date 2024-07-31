from django.urls import path
from . import views

urlpatterns = [
    path('paints', views.PaintListCreate.as_view(), name='paints'),
    path('paints/<int:pk>', views.PaintDetail.as_view(), name='paint-detail'),

    path('users-profiles/<int:pk>', views.UserProfileDetail.as_view(), name='users-profiles'),

    path('favourite-paints', views.FavouritePaintListCreate.as_view(), name='favourite-paints'),
    path('favourite-paints/delete', views.FavouritePaintDelete.as_view(), name='favourite-paints-delete'),

    path('carts', views.CartListCreate.as_view(), name='carts'),
    path('carts/<int:pk>', views.CartDetail.as_view(), name='cart-detail'),
]
