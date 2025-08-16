from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from users.views import MeView
from customers.views import CustomerViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"products",  ProductViewSet,  basename="products")
router.register(r"orders",    OrderViewSet,    basename="orders")
router.register(r"order-items", OrderItemViewSet, basename="order-items")

urlpatterns = [
    path("", include(router.urls)),
    path("ping/", lambda r: JsonResponse({"status": "ok"})),
    path("users/me/", MeView.as_view()),
    path("auth/", include("users.auth_urls")),
]
