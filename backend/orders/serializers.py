from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("total", "created_at", "updated_at")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ("line_total", "created_at", "updated_at")

    def validate(self, attrs):
        order = attrs.get("order") or getattr(self.instance, "order", None)
        if order and order.status == "confirmed":
            raise serializers.ValidationError("No se pueden modificar items de una orden confirmada.")
        return attrs

    def validate_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0.")
        return value

    def validate_unit_price(self, value):
        if value is not None and Decimal(value) < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return value
