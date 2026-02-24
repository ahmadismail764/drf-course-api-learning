from django.db.models import Max
from django.http import JsonResponse
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from .models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all() # This returns a django model
    serializer = ProductSerializer(products, many=True) # This turns it into a consumable format
    return Response(serializer.data) # This returns the data as a JSON response

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product) # This turns it into a consumable format
    return Response(serializer.data) # This returns the data as a JSON response

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('order_items__product') 
    # The above prefetches the order_items related field because you have to go through it to get its related field "product"
    serializer = OrderSerializer(orders, many=True) # This turns it into a consumable format
    return Response(serializer.data) # This returns the data as a JSON response

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)