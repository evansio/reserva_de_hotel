from django.urls import path, include
from .views import RoomViewSet, ReservationViewSet, RoomListView, RoomDetailView, home, reserve_room, reservation_confirmation, OccupancyStatsView, register
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<int:pk>/reserve/', reserve_room, name='reserve_room'),
    path('reservation/confirmation/<int:pk>/', reservation_confirmation, name='reservation_confirmation'),  # Nueva ruta para la confirmación de la reserva
    path('stats/', OccupancyStatsView.as_view(), name='occupancy_stats'),
    path('api/', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


