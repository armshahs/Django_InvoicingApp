from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ClientSerializer, ClientPutSerializer
from .models import Client

from django.core.exceptions import PermissionDenied


# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied("User does not have access to this object")

        serializer.save()


# Rewriting the above update function using @api_view decorator
@api_view(["PATCH"])
def update_client(request, id):
    client = Client.objects.filter(created_by=request.user).get(id=id)
    # partial update in serializer for PATCH. If it is PUT, remove "partial=True" from the serializer.
    serializer = ClientPutSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
def create_client(request):
    serializer = ClientPutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
