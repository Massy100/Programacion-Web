import redis
import uuid
import json
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import time

logger = logging.getLogger(__name__)

# Redis connection with retry logic
def get_redis_connection():
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            # Test connection
            redis_client.ping()
            logger.info("Successfully connected to Redis")
            return redis_client
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("All Redis connection attempts failed")
                raise e

# Initialize Redis connection
try:
    redis_client = get_redis_connection()
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {str(e)}")
    redis_client = None

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    return Response({
        "status": "healthy", 
        "service": "Django Secret API",
        "redis": redis_status
    })

@api_view(['POST'])
def hide_secret(request):
    """
    Store a secret in Redis and return a unique key
    """
    if not redis_client:
        return Response(
            {"error": "Redis connection unavailable"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    try:
        secret_text = request.data.get('text', '').strip()
        
        if not secret_text:
            return Response(
                {"error": "Text is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate unique key
        key = str(uuid.uuid4())
        
        # Ensure key doesn't already exist (extremely rare but possible)
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
        
        # Store in Redis with expiration (24 hours)
        redis_client.setex(key, 86400, secret_text)
        
        logger.info(f"Secret stored with key: {key}")
        
        return Response({
            "key": key,
            "message": "Secret stored successfully",
            "expires_in": "24 hours"
        })
        
    except redis.ConnectionError as e:
        logger.error(f"Redis connection error while hiding secret: {str(e)}")
        return Response(
            {"error": "Storage service unavailable"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Error hiding secret: {str(e)}")
        return Response(
            {"error": "Internal server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def reveal_secret(request, key):
    """
    Retrieve and delete a secret from Redis
    """
    if not redis_client:
        return Response(
            {"error": "Redis connection unavailable"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    try:
        if not redis_client.exists(key):
            return Response(
                {"error": "Secret not found or already viewed"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get the secret
        secret_text = redis_client.get(key)
        
        if secret_text is None:
            return Response(
                {"error": "Secret not found or already viewed"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete the key immediately after retrieval
        redis_client.delete(key)
        
        logger.info(f"Secret revealed and deleted for key: {key}")
        
        return Response({
            "text": secret_text,
            "message": "Secret revealed successfully (now destroyed)"
        })
        
    except redis.ConnectionError as e:
        logger.error(f"Redis connection error while revealing secret: {str(e)}")
        return Response(
            {"error": "Storage service unavailable"}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Error revealing secret: {str(e)}")
        return Response(
            {"error": "Internal server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_redis_info(request):
    """
    Debug endpoint to check Redis connection and stats
    """
    if not redis_client:
        return Response({
            "redis_connected": False,
            "error": "Redis connection not available"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        info = redis_client.info()
        keys_count = redis_client.dbsize()
        
        return Response({
            "redis_connected": True,
            "keys_count": keys_count,
            "used_memory": info.get('used_memory_human', 'N/A'),
            "redis_host": settings.REDIS_URL
        })
    except Exception as e:
        return Response({
            "redis_connected": False,
            "error": str(e),
            "redis_host": settings.REDIS_URL
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)