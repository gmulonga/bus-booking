import uuid
from django.db import models
from django.conf import settings
from booking.models import Booking
from users.models import User


class Payment(models.Model):
    payment_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_code} for Booking {self.booking.booking_id}"

