from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from .models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework.views import APIView

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # This class is particularly powerful because it
    # handles both GET and POST requests implicitly (and for the same endpoint)
    # And it's in the name "ListCreate"
    # All in 3 lines of code
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


""" 
The above is a combination of the ProductListAPIView and ProductCreateAPIView into one view
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.only('id', 'name', 'price', 'stock')
    # queryset = Product.objects.only('id', 'name', 'price', 'stock').filter(stock__gt=0)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs) 
"""
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all() # This returns a django model
#     serializer = ProductSerializer(products, many=True) # This turns it into a consumable format
#     return Response(serializer.data) # This returns the data as a JSON response

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.only('id', 'name', 'price', 'stock')
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product) # This turns it into a consumable format
#     return Response(serializer.data) # This returns the data as a JSON response

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('order_items__product')
    # This still applies the propagating fetch 
    # (fetching the items (product) related to the related items (order-items) in a single query)
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('order_items__product') # Explanation is above
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('order_items__product') 
#     # The above prefetches the order_items related field because you have to go through it to get its related field "product"
#     serializer = OrderSerializer(orders, many=True) # This turns it into a consumable format
#     return Response(serializer.data) # This returns the data as a JSON response

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)