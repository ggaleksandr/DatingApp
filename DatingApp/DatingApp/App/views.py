import os

import dotenv
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import AppUser
from .models import Sympathy
from .serializers import SympathySerializer, AppUserSerializer
from .utils import check_sympathy, calc_distance

# Load .env file
dotenv.load_dotenv()


class AppUserCreateView(generics.CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny]


class AppUserListView(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('gender', 'first_name', 'last_name')

    def get_queryset(self):
        queryset = AppUser.objects.all()

        if self.request.query_params.get('max_distance') is None:
            # return the queryset as is
            return queryset
        # filter the queryset
        else:
            filtered_ids = []
            max_distance = float(self.request.query_params.get('max_distance'))

            for user in queryset:
                dist = calc_distance(self.request.user.id, user.id)
                if dist > max_distance:
                    filtered_ids.append(user.id)
                queryset = AppUser.objects.exclude(id__in=filtered_ids)

            return queryset


class SympathyCreateView(generics.CreateAPIView):
    queryset = Sympathy.objects.all()
    serializer_class = SympathySerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):

        from_user = get_object_or_404(AppUser, id=request.user.id)
        to_user = get_object_or_404(AppUser, id=kwargs.get('id'))

        is_ids_exist = Sympathy.objects.filter(from_user=from_user, to_user=to_user).exists()

        if is_ids_exist:
            return JsonResponse({'message': 'Error! Duplicate IDs'})

        Sympathy.objects.create(from_user=from_user, to_user=to_user)
        is_mutual_sympathy = check_sympathy(from_user, to_user)

        if is_mutual_sympathy:
            send_mail(
                subject='Взаимная симпатия',
                message=f'Вы понравились {to_user.first_name}! Почта участника: {to_user.email}',
                from_email=os.getenv('EMAIL_HOST_USER'),
                recipient_list=[from_user.email, ],
                fail_silently=False,
            )

            send_mail(
                subject='Взаимная симпатия',
                message=f'Вы понравились {from_user.first_name}! Почта участника: {from_user.email}',
                from_email=os.getenv('EMAIL_HOST_USER'),
                recipient_list=[to_user.email, ],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Match!'})
        else:
            return JsonResponse({'message': 'No match'})
