from decimal import Decimal
from django.db import models
from django.db.models import Sum, Q
from core.models import TimeStampedModel
from customers.models import Customer
from products.models import Product


class Order(TimeStampedModel):
    STATUS_CHOICES = (
        ("draft", "draft"),
        ("confirmed", "confirmed"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ("-id",)
        constraints = [
            models.CheckConstraint(check=Q(total__gte=0), name="order_total_gte_0"),
        ]

    def recalc_total(self):
        total = self.items.aggregate(s=Sum("line_total"))["s"] or Decimal("0.00")
        self.total = total
        self.save(update_fields=["total"])


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ("-id",)
        constraints = [
            models.CheckConstraint(check=Q(quantity__gte=1), name="orderitem_qty_gte_1"),
            models.CheckConstraint(check=Q(unit_price__gte=0) | Q(unit_price__isnull=True), name="orderitem_unit_price_gte_0_or_null"),
            models.CheckConstraint(check=Q(line_total__gte=0), name="orderitem_line_total_gte_0"),
        ]

    def save(self, *args, **kwargs):
        # precio por defecto
        if self.unit_price is None:
            self.unit_price = self.product.price
        # recalcular importe de línea
        qty = int(self.quantity or 0)
        self.line_total = (self.unit_price or Decimal("0.00")) * Decimal(qty)
        super().save(*args, **kwargs)
        # actualizar total de la orden
        self.order.recalc_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.recalc_total()
