from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            # 'id',
            'description',
            'name',
            'price',
            'stock'
        )
    
    
    def validate_price(self, value):
        # Ensure the price is strictly greater than zero.
        # The original condition was inverted and rejected valid positive prices.
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price'
    )
    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal'
        )


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    # Read_only fields are not required for read or update or so
    
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, obj):
        order_items = obj.order_items.all()
        return sum(item.item_subtotal for item in order_items)
    
    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'created_at',
            'status',
            'order_items',
            'total_price'
        )

class ProductInfoSerializer(serializers.Serializer):
    # get all products, count of produts, max price
    # this is just to show, don't worry about realistic functionality dude
    products = ProductSerializer(many=True, required=False)
    # The following are just normal fields that you pass
    # And the serializer converts them to json or so...
    count = serializers.IntegerField()
    max_price = serializers.FloatField()