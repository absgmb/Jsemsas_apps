from django.db import connection
from django.http import JsonResponse


def health(request):
    """Cheap liveness probe: Django is alive and able to serve HTTP."""
    return JsonResponse({"status": "ok"})


def readiness(request):
    """Readiness probe: verify that the runtime database is reachable."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ok", "database": "ok"})
    except Exception:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
