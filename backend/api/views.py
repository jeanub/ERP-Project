from django.http import JsonResponse
from .tasks import add

def ping(request):
    return JsonResponse({"status": "ok"})

def add_async(request):
    r = add.delay(2, 3)
    return JsonResponse({"task_id": r.id})
