import redis
import uuid
import json
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

@api_view(['GET'])
def health_check(request):
    return Response({"status": "healthy", "service": "Django Secret API"})

@api_view(['POST'])
def hide_secret(request):
    try:
        secret_text = request.data.get('text', '').strip()
        
        if not secret_text:
            return Response(
                {"error": "Text is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        key = str(uuid.uuid4())
        
        max_retries = 5
        for attempt in range(max_retries):
            if not redis_client.exists(key):
                break
            key = str(uuid.uuid4())
        else:
            return Response(
                {"error": "Failed to generate unique key"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        redis_client.setex(key, 86400, secret_text)
        
        logger.info(f"Secret stored with key: {key}")
        
        return Response({
            "key": key,
            "message": "Secret stored successfully",
            "expires_in": "24 hours"
        })
        
    except Exception as e:
        logger.error(f"Error hiding secret: {str(e)}")
        return Response(
            {"error": "Internal server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def reveal_secret(request, key):
    try:
        if not redis_client.exists(key):
            return Response(
                {"error": "Secret not found or already viewed"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        secret_text = redis_client.get(key)
        
        if secret_text is None:
            return Response(
                {"error": "Secret not found or already viewed"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        redis_client.delete(key)
        
        logger.info(f"Secret revealed and deleted for key: {key}")
        
        return Response({
            "text": secret_text,
            "message": "Secret revealed successfully (now destroyed)"
        })
        
    except Exception as e:
        logger.error(f"Error revealing secret: {str(e)}")
        return Response(
            {"error": "Internal server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_redis_info(request):
    try:
        info = redis_client.info()
        keys_count = redis_client.dbsize()
        
        return Response({
            "redis_connected": True,
            "keys_count": keys_count,
            "used_memory": info.get('used_memory_human', 'N/A')
        })
    except Exception as e:
        return Response({
            "redis_connected": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)