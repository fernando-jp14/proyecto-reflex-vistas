from django.urls import path
from .views import history, document_type, payment_type, predetermined_price

urlpatterns = [
    # Solo las rutas que existen
    path("histories/", history.histories_list, name="histories_list"),
    path("histories/create/", history.history_create, name="history_create"),
    path("histories/<int:pk>/delete/", history.history_delete, name="history_delete"),
    
    # TODO: Agregar más endpoints cuando estén implementados
]
