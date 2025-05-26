from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "message": "A handled error occurred.",
            "errors": response.data
        }
        return response

    # Unhandled error (500)
    return Response({
        "success": False,
        "message": "Internal server error.",
        "errors": str(exc)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
