from django.db import models


class UserWithEmailManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(emailaddress='').exclude(emailaddress=None)


class OnlineAppManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('server_management').exclude(onlinedate=None).filter(offlinedate=None)


class ServerManagementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('server_management')


class ServerMailManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('server_mail')