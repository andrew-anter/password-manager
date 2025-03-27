from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from .models import Vault
from .services import vault_create, vault_update, vault_delete


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class VaultListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        vaults = Vault.objects.filter(user=request.user)
        serializer = VaultSerializer(vaults, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VaultSerializer(data=request.data)
        if serializer.is_valid():
            vault = vault_create(
                name=serializer.validated_data.get("name"), user=request.user
            )
            return Response(VaultSerializer(vault).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VaultDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Vault.objects.get(pk=pk, user=user)
        except Vault.DoesNotExist:
            return None

    def get(self, request, pk):
        vault = self.get_object(pk, request.user)
        if not vault:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VaultSerializer(vault)
        return Response(serializer.data)

    def put(self, request, pk):
        vault = self.get_object(pk, request.user)
        if not vault:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VaultSerializer(vault, data=request.data, partial=True)
        if serializer.is_valid():
            updated_vault = vault_update(
                vault=vault, name=serializer.validated_data.get("name", vault.name)
            )
            return Response(VaultSerializer(updated_vault).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vault = self.get_object(pk, request.user)
        if not vault:
            return Response(status=status.HTTP_404_NOT_FOUND)
        vault_delete(vault=vault)
        return Response(status=status.HTTP_204_NO_CONTENT)
