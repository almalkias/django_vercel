from rest_framework import generics, status, filters
from .models import Paint, UserProfile, FavouritePaint, Cart
from .serlizers import PaintSerializer, UserProfileSerializer, FavouritePaintSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class PaintListCreate(generics.ListCreateAPIView):
    queryset = Paint.objects.all()
    serializer_class = PaintSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaintDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paint.objects.all()
    serializer_class = PaintSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class FavouritePaintListCreate(generics.ListCreateAPIView):
    serializer_class = FavouritePaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavouritePaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_favourite_paint, created = FavouritePaint.objects.get_or_create(
            user=self.request.user)
        paint_id = self.request.data.get('paint_id')
        if paint_id:
            try:
                paint = Paint.objects.get(id=paint_id)
                user_favourite_paint.paints.add(paint)
                user_favourite_paint.save()
            except Paint.DoesNotExist:
                raise serializer.ValidationError({'error': 'Paint not found'})
        # Associate the instance with the authenticated user
        serializer.instance = user_favourite_paint


class FavouritePaintDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        paint_id = request.data.get('paint_id')
        try:
            favourite_paint = FavouritePaint.objects.get(user=request.user)
            paint = Paint.objects.get(id=paint_id)
            favourite_paint.paints.remove(paint)
            response_data = FavouritePaintSerializer(
                favourite_paint, context={'request': request}).data
            return Response(response_data, status=status.HTTP_200_OK)
        except FavouritePaint.DoesNotExist:
            return Response({'error': 'FavouritePaint not found'}, status=status.HTTP_404_NOT_FOUND)
        except Paint.DoesNotExist:
            return Response({'error': 'Paint not found'}, status=status.HTTP_404_NOT_FOUND)


class CartListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(
            cart_items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        paint_id = request.data.get('paint_id')
        paint = get_object_or_404(Paint, id=paint_id)

        cart_item, created = Cart.objects.get_or_create(user=user, paint=paint)

        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1

        cart_item.save()

        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(
            cart_items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk)
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            cart_item.save()
            serializer = CartSerializer(
                cart_item, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart_item = get_object_or_404(Cart, pk=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)