from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price', 'is_available')
    search_fields = ('room_number', 'room_type')
    list_filter = ('is_available', 'room_type')
    fields = ('room_number', 'room_type', 'price', 'is_available', 'image_url', 'other_images')  # Añadir los nuevos campos

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'is_active')
    search_fields = ('user__username', 'room__room_number')
    list_filter = ('is_active', 'check_in')
