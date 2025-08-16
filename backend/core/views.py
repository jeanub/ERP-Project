from django.shortcuts import render

# Create your views here.
# core/views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class Ping(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"status": "ok"})
