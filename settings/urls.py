"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🏗️ Módulo 1: Arquitectura y Usuarios Base
    path('architect/', include('architect.urls')),
    
    # 👤 Módulo 2: Perfiles de Usuarios
    path('profiles/', include('users_profiles.urls')),
    
    # 🩺 Módulo 3: Pacientes y Diagnósticos
    path('patients/', include('patients_diagnoses.urls')),
    
    # 👨‍⚕️ Módulo 4: Terapeutas (incluye ubicaciones)
    path('therapists/', include('therapists.urls')),
    
    # 📅 Módulo 5: Citas y Estados
    path('appointments/', include('appointments_status.urls')),
    
    # ⚙️ Módulo 6: Historiales y Configuraciones
    path('configurations/', include('histories_configurations.urls')),
]
