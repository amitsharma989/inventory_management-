from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from .caching import get_item_from_cache, set_item_in_cache
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("Item created successfully: %s", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error("Item creation failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, item_id):
    item = get_item_from_cache(item_id)
    if not item:
        try:
            item = Item.objects.get(id=item_id)
            set_item_in_cache(item_id, item)
        except Item.DoesNotExist:
            logger.warning("Item not found: %s", item_id)
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.warning("Attempt to update a non-existent item: %s", item_id)
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info("Item updated successfully: %s", serializer.data)
        return Response(serializer.data)
    logger.error("Item update failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        logger.info("Item deleted successfully: %s", item_id)
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        logger.warning("Attempt to delete a non-existent item: %s", item_id)
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
