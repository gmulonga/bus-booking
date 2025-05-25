from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Booking
from .serializers import BookingSerializer
from buses.models import Bus


@api_view(['GET'])
@swagger_auto_schema(responses={200: BookingSerializer(many=True)})
def booking_list(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@swagger_auto_schema(responses={200: BookingSerializer()})
def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id)
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='post',
    request_body=BookingSerializer,
    responses={201: BookingSerializer(), 400: 'Bad Request'}
)
@api_view(['POST'])
def booking_create(request):
    serializer = BookingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='patch',
    request_body=BookingSerializer,
    responses={200: BookingSerializer(), 400: 'Bad Request'}
)
@api_view(['PATCH'])
def booking_update(request, id):
    booking = get_object_or_404(Booking, id=id)
    serializer = BookingSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={204: 'Booking deleted'})
def booking_delete(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    return Response({"detail": "Booking deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

