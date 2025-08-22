from django.urls import path
from .views import history,document_types_list, document_type_create, document_type_delete

urlpatterns = [
    # Solo las rutas que existen
    path("histories/", history.histories_list, name="histories_list"),
    path("histories/create/", history.history_create, name="history_create"),
    path("histories/<int:pk>/delete/", history.history_delete, name="history_delete"),
    path("document_types/", document_types_list, name="document_types_list"),  # Para listar tipos de documento
    path("document_types/create/", document_type_create, name="document_type_create"),  # Para crear un tipo de documento
    path("document_types/<int:pk>/delete/", document_type_delete, name="document_type_delete"),  # Para eliminar un tipo de documento
    
    # TODO: Agregar más endpoints cuando estén implementados
]
