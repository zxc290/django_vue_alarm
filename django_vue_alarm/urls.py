"""django_vue_alarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework import routers
from server_admin.views import UserViewSet
from server_management.views import AppListViewSet, ServerTableViewSet
from server_mail.views import MailInfoViewSet, MailRuleViewSet, MailOperationViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('apps', AppListViewSet)
router.register('servers', ServerTableViewSet)
router.register('mail_info', MailInfoViewSet)
router.register('mail_rules', MailRuleViewSet)
router.register('mail_operations', MailOperationViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
