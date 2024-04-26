from django.shortcuts import render
from rest_framework import viewsets

from .models import Team
from .serializers import TeamSerializer

from django.core.exceptions import PermissionDenied


# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get_queryset(self):
        teams = self.request.user.teams.all()

        if not teams:
            Team.objects.create(name="", org_number="", created_by=self.request.user)

        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied("You are not allowed to modify this team")

        serializer.save()
