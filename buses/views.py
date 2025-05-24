from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import BusSerializer
from .models import Bus

@api_view(['GET'])
@swagger_auto_schema(responses={200: BusSerializer(many=True)})
def bus_list(request):
    buses = Bus.objects.all()
    serializer = BusSerializer(buses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@swagger_auto_schema(request_body=BusSerializer, responses={200: BusSerializer()})
def bus_detail(request, id):
    bus = get_object_or_404(Bus, id=id)
    serializer = BusSerializer(bus)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='post',
    request_body=BusSerializer,
    responses={201: BusSerializer(), 400: 'Bad Request'}
)
@api_view(['POST'])
def bus_create(request):
    if request.user.role != 'admin':
        return Response({'detail': 'You do not have permission to perform this action.'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = BusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='patch',
    request_body=BusSerializer,
    responses={200: BusSerializer(), 400: 'Bad Request'}
)
@api_view(['PATCH'])
def bus_update(request, id):
    bus = get_object_or_404(Bus, id=id)
    serializer = BusSerializer(bus, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@swagger_auto_schema(responses={204: 'Bus deleted'})
@permission_classes([IsAuthenticated])
def bus_delete(request, id):
    if request.user.role != 'admin':
        return Response({'detail': 'You do not have permission to perform this action.'},
                        status=status.HTTP_403_FORBIDDEN)

    bus = get_object_or_404(Bus, id=id)
    bus.delete()
    return Response({"detail": "Bus deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
