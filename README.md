# Reserva de Hotel

# Proyecto de Reserva de Habitaciones

Este proyecto es una aplicación web desarrollada en Django para la reserva de habitaciones. Los usuarios pueden registrarse, iniciar sesión, ver una lista de habitaciones disponibles y realizar reservas.

## Requisitos

- Python 3.x
- Django 3.x
- SQLite (o cualquier otra base de datos compatible con Django)
- Visual Studio Code (VSCode)

## Instalación

1. **Clona este repositorio:**
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. **Crea y activa un entorno virtual:**
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. **Instala las dependencias del proyecto:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Aplica las migraciones de la base de datos:**
    ```bash
    python manage.py migrate
    ```

5. **Crea un superusuario para acceder al panel de administración:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

7. **Abre tu navegador web y navega a `http://127.0.0.1:8000` para ver la aplicación en funcionamiento.**

## Configuración

Configura tu base de datos y otros ajustes en `settings.py` según tus necesidades. Algunos ajustes clave incluyen:

- **DATABASES**: Configuración de la base de datos.
- **INSTALLED_APPS**: Aplicaciones instaladas.
- **MIDDLEWARE**: Middleware utilizado.
- **TEMPLATES**: Configuración de las plantillas.

## Configuración en Visual Studio Code

Para un desarrollo eficiente en VSCode, se recomienda instalar las siguientes extensiones:

1. **Python**: Proporciona soporte para Python, incluyendo IntelliSense, linting y depuración.
2. **Django**: Extiende las capacidades de VSCode para soportar el desarrollo con Django.
3. **Pylint**: Para el análisis estático del código Python.
4. **Prettier**: Para formatear el código automáticamente.

## Estructura del Proyecto

```plaintext
.
├── manage.py
├── myproject
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── rooms
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── room_list.html
│   │   ├── reserve_room.html
├── static
│   ├── css
│   │   ├── styles.css
└── templates
    └── base.html

-- myproject: Contiene la configuración del proyecto Django.
-- rooms: Aplicación que maneja las funcionalidades relacionadas con las habitaciones.
-- static: Archivos estáticos como CSS.
-- templates: Plantillas HTML.

Comentarios en el Código
A continuación se incluyen ejemplos de comentarios en el código. Estos comentarios deben colocarse para mejorar la legibilidad y comprensión del código.

models.py
python
Copiar código
from django.db import models

class Room(models.Model):
    """
    Modelo que representa una habitación en el sistema.
    """
    room_number = models.CharField(max_length=10, unique=True)  # Número de habitación único
    room_type = models.CharField(max_length=50)  # Tipo de habitación (e.g., Simple, Doble)
    description = models.TextField()  # Descripción de la habitación
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Precio de la habitación

    def __str__(self):
        return self.room_number

class Reservation(models.Model):
    """
    Modelo que representa una reserva de habitación.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Habitación reservada
    check_in = models.DateField()  # Fecha de check-in
    check_out = models.DateField()  # Fecha de check-out
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Usuario que realiza la reserva

    def __str__(self):
        return f'Reserva de {self.user.username} en la habitación {self.room.room_number}'
views.py
python
Copiar código
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Reservation
from .forms import ReservationForm

def home_view(request):
    """
    Vista para la página principal.
    """
    return render(request, 'home.html')

def room_list_view(request):
    """
    Vista para mostrar la lista de habitaciones.
    """
    rooms = Room.objects.all()  # Obtener todas las habitaciones
    return render(request, 'room_list.html', {'rooms': rooms})

def reserve_room_view(request, room_id):
    """
    Vista para reservar una habitación.
    """
    room = get_object_or_404(Room, id=room_id)  # Obtener la habitación o mostrar un 404
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Guardar la reserva
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.user = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'reserve_room.html', {'room': room, 'form': form})
urls.py
python
Copiar código
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('reserve/<int:room_id>/', views.reserve_room_view, name='reserve_room'),
]
API
A continuación se detallan algunas de las principales vistas y URL:

Login: url('login', views.login_view)
Register: url('register', views.register_view)
Home: url('home', views.home_view)
Room List: url('rooms', views.room_list_view)
Reserve Room: url('reserve', views.reserve_room_view)
Contribuciones
Si deseas contribuir a este proyecto, por favor haz un fork del repositorio y envía un pull request. Todas las contribuciones son bienvenidas.

Licencia
Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo LICENSE para más detalles.

python
Copiar código

### Archivos y Comentarios

#### `models.py`

```python
from django.db import models

class Room(models.Model):
    """
    Modelo que representa una habitación en el sistema.
    """
    room_number = models.CharField(max_length=10, unique=True)  # Número de habitación único
    room_type = models.CharField(max_length=50)  # Tipo de habitación (e.g., Simple, Doble)
    description = models.TextField()  # Descripción de la habitación
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Precio de la habitación

    def __str__(self):
        return self.room_number

class Reservation(models.Model):
    """
    Modelo que representa una reserva de habitación.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Habitación reservada
    check_in = models.DateField()  # Fecha de check-in
    check_out = models.DateField()  # Fecha de check-out
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Usuario que realiza la reserva

    def __str__(self):
        return f'Reserva de {self.user.username} en la habitación {self.room.room_number}'
views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Reservation
from .forms import ReservationForm

def home_view(request):
    """
    Vista para la página principal.
    """
    return render(request, 'home.html')

def room_list_view(request):
    """
    Vista para mostrar la lista de habitaciones.
    """
    rooms = Room.objects.all()  # Obtener todas las habitaciones
    return render(request, 'room_list.html', {'rooms': rooms})

def reserve_room_view(request, room_id):
    """
    Vista para reservar una habitación.
    """
    room = get_object_or_404(Room, id=room_id)  # Obtener la habitación o mostrar un 404
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Guardar la reserva
            reservation = form.save(commit=False)
            reservation.room = room
            reservation.user = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'reserve_room.html', {'room': room, 'form': form})
urls.py
python
Copiar código
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('rooms/', views.room_list_view, name='room_list'),
    path('reserve/<int:room_id>/', views.reserve_room_view, name='reserve_room'),
]
