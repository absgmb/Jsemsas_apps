from django.db import connection
from django.http import JsonResponse


def health(request):
    """Render health endpoint: verifies Django can reach PostgreSQL."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ok", "database": "ok"})
    except Exception:
        return JsonResponse({"status": "error", "database": "unavailable"}, status=503)


def readiness(request):
    """Readiness endpoint used before accepting traffic."""
    return health(request)
