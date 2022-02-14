from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from book_store.models import Inventory, Cart, User
from django.http.response import JsonResponse
from django.db import IntegrityError
from book_store.serializers import InventorySerializer, CartSerializer
import json


class InventoryView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(self, request):
        inventory = Inventory.objects.all()
        inventory_serialized = InventorySerializer(inventory, many=True)
        return JsonResponse(inventory_serialized.data, safe=False)

    @staticmethod
    def post(request):
        req_body = json.loads(request.body)
        seller = request.user.username
        title = req_body['title']
        quantity = req_body['quantity']
        price = req_body['price']
        if price <= 0:
            return JsonResponse({
                'error': 'invalid price number!'
            })
        if quantity <= 0:
            return JsonResponse({
                'error': 'invalid quantity!'
            })

        inventory = Inventory(seller=seller,
                              title=title,
                              quantity=quantity,
                              price=price
                              )
        try:
            inventory.save()
            return JsonResponse({
                'message': f'hey {seller}, new inventory has been added!'
            })
        except IntegrityError:
            return JsonResponse({
                'error': 'could not add inventory item due to database integrity error'
            })


class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(self, request):
        username = request.user.username
        cart = Cart.objects.get(buyer=username)
        cart_serialized = CartSerializer(cart, many=True)
        return JsonResponse(cart_serialized.data, safe=False)

    @staticmethod
    def post(request):
        req_body = json.loads(request.body)
        buyer = request.user.username
        seller = req_body['seller']
        title = req_body['title']
        quantity = req_body['quantity']
        inventory = Inventory.objects.get(seller=seller, title=title)
        if inventory:
            if inventory.quantity < quantity:
                return JsonResponse({
                    'error': 'selected inventory quantity is less than order quantity!'
                })
            total_price = quantity * inventory.price
            cart = Cart(buyer=buyer,
                        seller=seller,
                        title=title,
                        quantity=quantity,
                        total_price=total_price
                        )
            try:
                cart.save()
                return JsonResponse({
                    'message': f'hey {buyer}, your shopping cart has been updated!'
                })
            except IntegrityError:
                return JsonResponse({
                    'error': 'could not update your shopping cart due to integrity errors'
                })
        return JsonResponse({
            'error': 'invalid inventory seller or title'
        })


class PurchaseView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        user = request.user
        cart = Cart.objects.get(buyer=user.username)
        if cart:
            total_price = 0
            for c in cart:
                total_price += c.total_price
            if total_price > user.bank_account:
                return JsonResponse({
                    'error': 'insufficient funds!'
                })
            for c in cart:
                seller = User.objects.get(username=c.seller)
                user.bank_account -= c.total_price
                seller.bank_account += c.total_price
                inventory = Inventory.objects.get(seller=seller.username, title=c.title)
                if inventory.quantity == c.quantity:
                    inventory.delete()
                else:
                    inventory.quantity -= c.quantity
            return JsonResponse({
                'message': f'{user.username} purchase was successful have a nice day!'
            })
        return JsonResponse({
            'error': 'shopping cart is empty!'
        })




