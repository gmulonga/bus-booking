from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Payment
from .serializers import PaymentSerializer
from booking.models import Booking
from users.models import User


@api_view(['GET'])
@swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
def payment_list(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@swagger_auto_schema(responses={200: PaymentSerializer()})
def payment_detail(request, id):
    payment = get_object_or_404(Payment, id=id)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='post',
    request_body=PaymentSerializer,
    responses={201: PaymentSerializer(), 400: 'Bad Request'}
)
@api_view(['POST'])
def payment_create(request):
    data = request.data.copy()
    serializer = PaymentSerializer(data=data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    method='patch',
    request_body=PaymentSerializer,
    responses={200: PaymentSerializer(), 400: 'Bad Request'}
)
@api_view(['PATCH'])
def payment_update(request, id):
    payment = get_object_or_404(Payment, id=id)
    serializer = PaymentSerializer(payment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={204: 'Payment deleted'})
def payment_delete(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    return Response({"detail": "Payment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
