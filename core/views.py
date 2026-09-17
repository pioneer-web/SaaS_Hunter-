from django.http import JsonResponse
from django.db import connection

def health(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return JsonResponse({"status": "ok", "service": "saas-hunter"})
