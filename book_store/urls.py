from book_store.views import InventoryView, CartView, PurchaseView
from django.urls import re_path
urlpatterns = [
    re_path(r'^inventory/$', InventoryView.as_view()),
    re_path(r'^cart/$', CartView.as_view()),
    re_path(r'^purchase/$', PurchaseView.as_view()),
]
