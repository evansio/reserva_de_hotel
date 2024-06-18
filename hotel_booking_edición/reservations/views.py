from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    latest_rooms = Room.objects.order_by('-id')[:6]
    return render(request, 'reservations/home.html', {'latest_rooms': latest_rooms})

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['room_type', 'is_available']
    search_fields = ['room_number', 'room_type']
    ordering_fields = ['price']

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'reservations/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Room.objects.all()
        for room in queryset:
            room.update_availability()
        room_type = self.request.GET.get('room_type')
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        return queryset

class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'reservations/room_detail.html'
    context_object_name = 'room'

@login_required
def reserve_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        
        # Validate check-in and check-out dates
        if check_in >= check_out:
            return render(request, 'reservations/reserve_room.html', {
                'room': room,
                'error_message': 'Check-out date must be after check-in date.',
            })
        
        reservation = Reservation(user=request.user, room=room, check_in=check_in, check_out=check_out)
        reservation.save()
        room.update_availability()
        return redirect('reservation_confirmation', pk=reservation.pk)
    
    return render(request, 'reservations/reserve_room.html', {
        'room': room,
        'room_image': room.image_url,
        'room_type': room.room_type,
        'price': room.price,
    })

@login_required
def reservation_confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/reservation_confirmation.html', {'reservation': reservation})

class OccupancyStatsView(LoginRequiredMixin, ListView):
    template_name = 'reservations/occupancy_stats.html'
    context_object_name = 'stats'

    def get_queryset(self):
        return Room.objects.annotate(
            total_reservations=Count('reservation', filter=Q(reservation__is_active=True))
        )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
