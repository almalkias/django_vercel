from rest_framework import serializers
from .models import Paint, UserProfile, FavouritePaint, Cart
from django.contrib.auth import get_user_model


User = get_user_model()

class PaintSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
    pdf_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Paint
        fields = ['id', 'title', 'artist', 'description', 'price', 'width', 'height', 'user', 'publish', 'date', 'image1', 'image2', 'image3', 'image4', 'image5', 'pdf_file']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    telephone = serializers.CharField(source='user.telephone', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'telephone', 'username', 'image', 'first_name',
                  'last_name', 'country', 'city', 'birth_date']
        

class FavouritePaintSerializer(serializers.ModelSerializer):
    paints = PaintSerializer(many=True, read_only=True)

    class Meta:
        model = FavouritePaint
        fields = ['paints']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    paint_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Paint.objects.all())
    paint = PaintSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'paint', 'paint_id', 'quantity']