from django.urls import path

from .views import VaultListView, VaultDetailView

urlpatterns = [
    path("", VaultListView.as_view(), name="vault-list"),
    path("<int:pk>/", VaultDetailView.as_view(), name="vault-detail"),
]
