from django.http import JsonResponse
from api.serializers import ProductSerializer
from .models import Product
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