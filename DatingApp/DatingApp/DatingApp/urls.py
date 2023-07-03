"""
URL configuration for DatingApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from App.views import AppUserCreateView, SympathyCreateView, AppUserListView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/clients/create/', AppUserCreateView.as_view(), name='user-create'),
    path('api/clients/<int:id>/match/', SympathyCreateView.as_view(), name='users-sympathy'),
    path('api/list/', AppUserListView.as_view(), name='users-list'),
]
