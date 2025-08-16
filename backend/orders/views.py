from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-id")
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        order = self.get_object()

        if order.status == "confirmed":
            return Response({"detail": "Order already confirmed"}, status=status.HTTP_400_BAD_REQUEST)

        items_qs = order.items.select_related("product")
        if not items_qs.exists():
            return Response({"detail": "Order has no items"}, status=status.HTTP_400_BAD_REQUEST)

        # Validaciones previas de stock y cantidades
        for it in items_qs:
            if it.quantity <= 0:
                return Response({"detail": f"Invalid quantity for {it.product.sku}"}, status=status.HTTP_400_BAD_REQUEST)
            if it.quantity > it.product.stock:
                return Response(
                    {"detail": f"Not enough stock for {it.product.sku}", "available": it.product.stock},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        with transaction.atomic():
            total = Decimal("0.00")

            # Bloqueo de filas de items para consistencia
            for it in items_qs.select_for_update():
                # unit_price por defecto al precio actual del producto
                if not it.unit_price:
                    it.unit_price = it.product.price

                it.line_total = (it.unit_price or Decimal("0.00")) * it.quantity
                it.save(update_fields=["unit_price", "line_total", "updated_at"])

                # Descontar stock del producto
                p = it.product
                p.stock = p.stock - it.quantity
                if p.stock < 0:
                    return Response({"detail": f"Stock would go negative for {p.sku}"}, status=status.HTTP_400_BAD_REQUEST)
                p.save(update_fields=["stock", "updated_at"])

                total += it.line_total

            order.total = total
            order.status = "confirmed"
            order.save(update_fields=["total", "status", "updated_at"])

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by("-id")
    serializer_class = OrderItemSerializer
