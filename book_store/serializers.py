from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from book_store.models import Inventory, Book, Cart

user = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = user
        fields = ('username',
                  'email',
                  'password')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('seller',
                  'title',
                  'quantity',
                  'price',
                  )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('buyer',
                  'seller',
                  'title',
                  'quantity',
                  'total_price',
                  )
