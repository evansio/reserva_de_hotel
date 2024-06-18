from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)  # URL para la imagen de portada
    other_images = models.JSONField(blank=True, null=True)  # Campo para almacenar otras imágenes como una lista de URLs

    def update_availability(self):
        now = timezone.now()
        reservations = self.reservation_set.filter(check_out__gte=now, check_in__lte=now)
        self.is_available = not reservations.exists()
        self.save()

    def __str__(self):
        return f"{self.room_number} - {self.room_type}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.room.update_availability()
