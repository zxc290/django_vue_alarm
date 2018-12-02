from rest_framework import viewsets
from .models import AppList, ServerTable
from .serializers import AppListSerializer, ServerTableSerializer


class AppListViewSet(viewsets.ModelViewSet):
    queryset = AppList.objects.all()
    serializer_class = AppListSerializer


class ServerTableViewSet(viewsets.ModelViewSet):
    queryset = ServerTable.objects.all()
    serializer_class = ServerTableSerializer