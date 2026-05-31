from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint.
    Used by Kubernetes liveness probe to determine if pod is alive.
    """
    try:
        return JsonResponse({
            'status': 'ok',
            'service': 'alfa-romeo-web'
        }, status=200)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def readiness_check(request):
    """
    Readiness check endpoint.
    Used by Kubernetes readiness probe to determine if pod is ready to receive traffic.
    Checks database connectivity.
    """
    try:
        # Try to get a database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'ready',
            'database': 'connected',
            'service': 'alfa-romeo-web'
        }, status=200)
    except OperationalError as e:
        logger.error(f"Readiness check failed - database connection issue: {str(e)}")
        return JsonResponse({
            'status': 'not_ready',
            'database': 'disconnected',
            'message': str(e)
        }, status=503)
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def liveness_check(request):
    """
    Liveness check endpoint.
    Used by Kubernetes liveness probe to determine if pod should be restarted.
    Simple check - if this responds, the pod is alive.
    """
    try:
        return JsonResponse({
            'status': 'alive',
            'service': 'alfa-romeo-web'
        }, status=200)
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        return JsonResponse({
            'status': 'dead',
            'message': str(e)
        }, status=500)
